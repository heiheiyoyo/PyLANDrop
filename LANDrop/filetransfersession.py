# BSD 3-Clause License
#
# Copyright (c) 2021, LANDrop
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from abc import abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from typing import List
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtNetwork import QTcpSocket, QAbstractSocket
from typing import Optional

from LANDrop.crypto import Crypto


class State(Enum):
    HANDSHAKE1 = auto()
    HANDSHAKE2 = auto()
    TRANSFERRING = auto()
    FINISHED = auto()


class FileTransferSession(QObject):
    printMessage = pyqtSignal(str)
    updateProgress = pyqtSignal(float)
    errorOccurred = pyqtSignal(str)
    fileMetadataReady = pyqtSignal(list, int, str, str)
    ended = pyqtSignal()

    @dataclass
    class FileMetadata:
        filename: str
        size: int

    def __init__(self, parent: Optional['QObject'], socket: QTcpSocket) -> None:
        super().__init__(parent)
        self.state = State.HANDSHAKE1
        self.socket: QTcpSocket = socket
        self.totalSize = 0
        self.transferredSize = 0
        self.crypto = Crypto()
        self.readBuffer = b""
        self.transferQ: List[FileTransferSession.FileMetadata] = []

        self.socket.setParent(self)
        self.socket.setSocketOption(QAbstractSocket.SocketOption.LowDelayOption, 1)
        self.socket.readyRead.connect(self.socketReadyRead)
        self.socket.errorOccurred.connect(self.socketErrorOccurred)

    def start(self):
        self.printMessage.emit(self.tr("Handshaking..."))
        self.socket.write(self.crypto.localPublicKey())

    @abstractmethod
    def respond(self, accepted: bool):
        raise RuntimeError("respond not implemented")

    def encryptAndSend(self, data: bytes) -> None:
        sendData: bytes = self.crypto.encrypt(data)
        size = len(sendData)
        sendData = bytes([size & 0xFF]) + sendData
        sendData = bytes([(size >> 8) & 0xFF]) + sendData
        self.socket.write(sendData)

    @abstractmethod
    def handshake1Finished(self) -> None:
        pass

    @abstractmethod
    def processReceivedData(self, data: bytes) -> None:
        pass

    def socketReadyRead(self) -> None:

        self.readBuffer += bytes(self.socket.readAll())
        if self.state == State.HANDSHAKE1:
            if len(self.readBuffer) < self.crypto.publicKeySize():
                self.errorOccurred.emit(self.tr("Handshake failed."))
                return
            publicKey = self.readBuffer[:self.crypto.publicKeySize()]
            self.readBuffer = self.readBuffer[self.crypto.publicKeySize():]
            try:
                self.crypto.setRemotePublicKey(publicKey)
            except Exception as e:
                self.errorOccurred.emit(str(e))
                return
            self.printMessage.emit(self.tr("Handshaking... Code: %1"
                                           ).replace(
                "%1", self.crypto.sessionKeyDigest()
            ))
            self.state = State.HANDSHAKE2

            self.handshake1Finished()

        while self.readBuffer:
            if len(self.readBuffer) < 2:
                break

            size = self.readBuffer[0] << 8
            size |= self.readBuffer[1]
            if len(self.readBuffer) < size + 2:
                break

            data = self.readBuffer[2: size+2]
            self.readBuffer = self.readBuffer[size + 2:]

            try:
                data = self.crypto.decrypt(data)
            except RuntimeError as e:
                self.errorOccurred.emit(str(e))
                return

            self.processReceivedData(data)

    def socketErrorOccurred(self) -> None:
        if self.state != State.FINISHED:
            self.errorOccurred.emit(self.socket.errorString())

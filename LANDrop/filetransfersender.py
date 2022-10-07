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
import json
from typing import Optional, List

from PySide2.QtCore import QSysInfo, QFileInfo, QTimer, QObject, QFile
from PySide2.QtNetwork import QTcpSocket

from LANDrop.filetransfersession import FileTransferSession, State
from LANDrop.settings import Settings

TRANSFER_QUANTA = 64000


class FileTransferSender(FileTransferSession):

    def __init__(self, parent: Optional[QObject], socket: QTcpSocket, files: List[QFile]) -> None:
        super().__init__(parent, socket)
        self.files = files
        self.socket.bytesWritten.connect(self.socketBytesWritten)

        for file in self.files:
            filename = QFileInfo(file).fileName()
            size = file.size()
            self.totalSize += size
            self.transferQ.append(
                FileTransferSession.FileMetadata(filename, size))

    def handshake1Finished(self) -> None:
        jsonFiles = []
        for metadata in self.transferQ:
            jsonFile = {"filename": metadata.filename, "size": metadata.size}
            jsonFiles.append(jsonFile)

        obj = {"device_name": Settings.deviceName(
        ), "device_type": QSysInfo.productType(), "files": jsonFiles}
        self.encryptAndSend(json.dumps(
            obj, ensure_ascii=False).encode("utf-8"))

    def processReceivedData(self, data: bytes) -> None:
        if self.state == State.HANDSHAKE2:
            try:
                obj = json.loads(data)
            except:
                self.errorOccurred.emit(self.tr("Handshake failed."))
                return

            response = obj["response"]
            if not isinstance(response, (float, int)):
                self.errorOccurred.emit(self.tr("Handshake failed."))
                return

            if int(response) == 0:
                self.errorOccurred.emit(
                    self.tr("The receiving device rejected your file(s)."))
                return
            self.state = State.TRANSFERRING
            self.socketBytesWritten()

    def socketBytesWritten(self) -> None:
        if self.state != State.TRANSFERRING or self.socket.bytesToWrite() > 0:
            return

        while self.transferQ:
            curFile = self.transferQ[0]
            if curFile.size == 0:
                self.transferQ = self.transferQ[1:]
                self.files = self.files[1:]
            else:
                self.printMessage.emit(
                    self.tr("Sending file %1...").replace("%1", curFile.filename))
                break

        if not self.transferQ:
            self.state = State.FINISHED
            self.printMessage.emit(self.tr("Done!"))
            self.socket.disconnectFromHost()
            QTimer.singleShot(5000, self.ended)
            return

        curFile = self.files[0]
        curMetadata = self.transferQ[0]
        data = curFile.read(TRANSFER_QUANTA)
        self.encryptAndSend(data)
        curMetadata.size -= len(data)
        self.transferredSize += len(data)
        self.updateProgress.emit(float(self.transferredSize) / self.totalSize)

    def respond(self, accepted: bool) -> None:
        raise RuntimeError("respond not implemented")

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
from typing import Optional
from PySide2.QtCore import QDir, QFileInfo, QFile, QIODevice, QObject, QUrl, QTimer
from PySide2.QtGui import QDesktopServices
from PySide2.QtNetwork import QTcpSocket
from LANDrop.filetransfersession import FileTransferSession, State
from LANDrop.settings import Settings


class FileTransferReceiver(FileTransferSession):

    def __init__(self, parent: Optional['QObject'], socket: QTcpSocket) -> None:
        super().__init__(parent, socket)
        self.writingFile = None
        self.downloadPath = Settings.downloadPath()

    def respond(self, accepted: bool) -> None:
        obj = {
            "response": int(accepted)
        }
        self.encryptAndSend(json.dumps(
            obj, ensure_ascii=False).encode("utf-8"))

        if accepted:
            if not QDir().mkpath(self.downloadPath):
                self.errorOccurred.emit(
                    self.tr("Cannot create download path: ") + self.downloadPath)
                return

            if not QFileInfo(self.downloadPath).isWritable():
                self.errorOccurred.emit(
                    self.tr("Download path is not writable: ") + self.downloadPath)
                return

            self.state = State.TRANSFERRING
            self.createNextFile()
        else:
            self.socket.bytesWritten.connect(self.ended)

    def processReceivedData(self, data: bytes) -> None:
        if self.state == State.HANDSHAKE2:
            try:
                obj = json.loads(data)
            except json.JSONDecodeError:
                self.ended.emit()
                return

            deviceName = obj["device_name"]
            if not isinstance(deviceName, str):
                self.ended.emit()
                return

            filesJson = obj["files"]
            if not isinstance(filesJson, list):
                self.ended.emit()
                return

            filesJsonArray = filesJson
            if not filesJsonArray:
                self.ended.emit()
                return

            for v in filesJsonArray:
                if not isinstance(v, dict):
                    self.ended.emit()
                    return
                o = v

                filename = o["filename"]
                if not isinstance(filename, str):
                    self.ended.emit()
                    return

                size = o["size"]
                if not isinstance(size, (int, float)):
                    self.ended.emit()
                    return

                sizeInt = int(size)
                self.totalSize += sizeInt
                self.transferQ.append(FileTransferSession.FileMetadata(
                    filename, sizeInt))

            self.fileMetadataReady.emit(self.transferQ, self.totalSize, deviceName,
                                        self.crypto.sessionKeyDigest())
        elif self.state == State.TRANSFERRING:
            self.transferredSize += len(data)
            self.updateProgress.emit(
                float(self.transferredSize) / self.totalSize)
            tmpData = data
            while len(tmpData) > 0:
                curFile = self.transferQ[0]
                writeSize = min(curFile.size, len(tmpData))
                written = self.writingFile.write(tmpData[:writeSize])
                curFile.size -= written
                tmpData = tmpData[written:]
                if curFile.size == 0:
                    self.transferQ = self.transferQ[1:]
                    self.createNextFile()

    def createNextFile(self) -> None:
        while self.transferQ:
            curFile = self.transferQ[0]
            filename = self.downloadPath + QDir.separator() + curFile.filename
            if self.writingFile:
                self.writingFile.deleteLater()
                self.writingFile = None
            self.writingFile = QFile(filename, self)
            if not self.writingFile.open(QIODevice.WriteOnly):
                self.errorOccurred.emit(
                    self.tr("Unable to open file %1.").replace("%1", filename))
                return

            if curFile.size > 0:
                self.printMessage.emit(
                    self.tr("Receiving file %1...").replace("%1", curFile.filename))
                break

            self.transferQ = self.transferQ[1:]

        if not self.transferQ:
            if self.writingFile:
                self.writingFile.deleteLater()
                self.writingFile = None

            self.state = State.FINISHED
            QDesktopServices.openUrl(QUrl.fromLocalFile(self.downloadPath))
            self.printMessage.emit(self.tr("Done!"))
            self.socket.disconnectFromHost()
            QTimer.singleShot(5000, self.ended)

    def handshake1Finished(self):
        pass

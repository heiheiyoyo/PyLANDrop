# BSD 3-Clause License
#
# Copyright (c) 2021, LANDrop
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, self
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    self list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    self software without specific prior written permission.
#
# self SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF self SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from typing import List, Optional
from PyQt5.QtCore import Qt, QLocale
from PyQt5.QtWidgets import QWidget, QDialog, QMessageBox, QApplication
from ui_filetransferdialog import Ui_FileTransferDialog
from filetransfersession import FileTransferSession


class FileTransferDialog(QDialog):
    def __init__(self, parent: Optional[QWidget], session: FileTransferSession):
        super().__init__(parent)
        self.ui = Ui_FileTransferDialog()
        self.session = session
        self.errored = False
        self.questionBox = QMessageBox(self)

        self.ui.setupUi(self)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)

        self.questionBox.setIcon(QMessageBox.Question)
        self.questionBox.setWindowTitle(QApplication.applicationName())
        self.questionBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        self.questionBox.setDefaultButton(QMessageBox.Yes)
        self.questionBox.finished.connect(self.respond)

        self.session.setParent(self)
        self.session.printMessage.connect(self.ui.statusLabel.setText)
        self.session.updateProgress.connect(self.sessionUpdateProgress)
        self.session.errorOccurred.connect(self.sessionErrorOccurred)
        self.session.fileMetadataReady.connect(self.sessionFileMetadataReady)
        self.session.ended.connect(self.accept)
        self.session.start()

    def respond(self, result: int) -> None:
        response = result == QMessageBox.Yes
        self.session.respond(response)
        if not response:
            self.hide()

    def sessionUpdateProgress(self, progress: float) -> None:
        self.ui.progressBar.setValue(self.ui.progressBar.maximum() * progress)

    def sessionErrorOccurred(self, msg: str) -> None:
        if self.errored:
            return
        self.errored = True
        if self.isVisible():
            QMessageBox.critical(self, QApplication.applicationName(), msg)
        self.done(self.Rejected)

    def sessionFileMetadataReady(self, metadata: List[FileTransferSession.FileMetadata], totalSize: int,
                                 deviceName: str, sessionKeyDigest: str) -> None:
        self.show()

        totalSizeStr: str = self.locale().formattedDataSize(
            totalSize, 2, QLocale.DataSizeTraditionalFormat)

        if len(metadata) == 1:
            msg = self.tr("%1 would like to share a file \"%2\" of size %3.").replace("%1",
                                                                                      deviceName).replace("%2",
                                                                                                          metadata[
                                                                                                              0].filename).replace(
                "%3", totalSizeStr)
        else:
            msg = self.tr("%1 would like to share %2 files of total size %3."
                          ).replace("%1", deviceName
                                    ).replace("%2", str(len(metadata))).replace(
                "%3", totalSizeStr)

        msg += self.tr("\nConfirm that the code \"%1\" is shown on the sending device.").replace(
            "%1", sessionKeyDigest)
        msg += self.tr("\nWould you like to receive it?")

        self.questionBox.setText(msg)
        self.questionBox.show()

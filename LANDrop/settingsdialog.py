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
from PyQt5.QtCore import QVersionNumber, QUrl, Qt
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QMessageBox, QApplication, QFileDialog, QWidget
from PyQt5.QtGui import QDesktopServices, QShowEvent
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest
from LANDrop.settings import Settings
from LANDrop.ui_settingsdialog import Ui_SettingsDialog
from typing import Optional


class SettingsDialog(QDialog):

    def __init__(self, parent: Optional['QWidget'] = None) -> None:
        super().__init__(parent)
        self.ui = Ui_SettingsDialog()
        self.serverPortEdited = False

        self.ui.setupUi(self)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.ui.downloadPathSelectButton.clicked.connect(
            self.downloadPathSelectButtonClicked)
        self.ui.serverPortLineEdit.textChanged.connect(
            self.serverPortLineEditChanged)

        self.ui.buttonBox.button(QDialogButtonBox.Ok).setText(self.tr("OK"))
        self.ui.buttonBox.button(
            QDialogButtonBox.Cancel).setText(self.tr("Cancel"))

    def accept(self) -> None:

        Settings.setDeviceName(self.ui.deviceNameLineEdit.text())
        Settings.setDownloadPath(self.ui.downloadPathLineEdit.text())
        Settings.setDiscoverable(self.ui.discoverableCheckBox.isChecked())
        Settings.setServerPort(int(self.ui.serverPortLineEdit.text()))
        if self.serverPortEdited:
            QMessageBox.information(self, QApplication.applicationName(),
                                    self.tr("Server port setting will take effect after you restart the app."))
        self.done(self.Accepted)

    def downloadPathSelectButtonClicked(self) -> None:

        dir_: str = QFileDialog.getExistingDirectory(self, self.tr("Select Download Path"),
                                                     self.ui.downloadPathLineEdit.text())
        if dir_:
            self.ui.downloadPathLineEdit.setText(dir)

    def serverPortLineEditChanged(self) -> None:
        self.serverPortEdited = True

    def showEvent(self, e: QShowEvent) -> None:
        super().showEvent(e)
        self.ui.deviceNameLineEdit.setText(Settings.deviceName())
        self.ui.downloadPathLineEdit.setText(Settings.downloadPath())
        self.ui.discoverableCheckBox.setChecked(Settings.discoverable())
        self.ui.serverPortLineEdit.setText(str(Settings.serverPort()))
        self.ui.deviceNameLineEdit.setFocus()
        self.serverPortEdited = False

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
from typing import Optional

from PySide2.QtCore import QObject, QSysInfo, QTimer, QDir, QUrl, Qt
from PySide2.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PySide2.QtGui import QIcon, QDesktopServices
from PySide2.QtNetwork import QNetworkProxy
from LANDrop.settings import Settings
from LANDrop.aboutdialog import AboutDialog
from LANDrop.settingsdialog import SettingsDialog
from LANDrop.filetransferserver import FileTransferServer
from LANDrop.discoveryservice import DiscoveryService
from LANDrop.selectfilesdialog import SelectFilesDialog


class TrayIcon(QSystemTrayIcon):
    def __init__(self, parent: Optional[QObject] = None) -> None:
        super().__init__(parent)
        self._menu = QMenu()
        self._aboutDialog = AboutDialog()
        self._settingsDialog = SettingsDialog()
        self._server = FileTransferServer()
        self._discoveryService = DiscoveryService()
        self._d = None

        QNetworkProxy.setApplicationProxy(QNetworkProxy(QNetworkProxy.NoProxy))

        appIcon = QIcon(":/icons/app.png")
        appMaskIcon = QIcon(":/icons/app_mask.png")
        appMaskIcon.setIsMask(True)
        sendIcon = QIcon(":/icons/send.png")
        openDownloadFolderIcon = QIcon(":/icons/open_download_folder.png")
        settingsIcon = QIcon(":/icons/settings.png")
        aboutIcon = QIcon(":/icons/about.png")
        exitIcon = QIcon(":/icons/exit.png")
        if QSysInfo.productType() == "osx" or QSysInfo.productType() == "macos":
            self.setIcon(appMaskIcon)
        else:
            self.setIcon(appIcon)

        addrPortAction = self._menu.addAction("")
        addrPortAction.setEnabled(False)
        self._menu.addSeparator()
        action = self._menu.addAction(sendIcon, self.tr("Send File(s)..."))
        action.triggered.connect(self.sendActionTriggered)
        action = self._menu.addAction(openDownloadFolderIcon,
                                      self.tr("Open Download Folder"))
        action.triggered.connect(self.openDownloadFolderActionTriggered)
        action = self._menu.addAction(settingsIcon, self.tr("Settings..."))

        action.triggered.connect(self._settingsDialog.show)

        self._menu.addSeparator()
        action = self._menu.addAction(aboutIcon, self.tr("About..."))
        action.triggered.connect(self._aboutDialog.show)
        action = self._menu.addAction(exitIcon, self.tr("Exit"))
        action.triggered.connect(self.exitActionTriggered)
        self.setContextMenu(self._menu)

        self.setToolTip(QApplication.applicationName())
        self.activated.connect(self.trayIconActivated)
        self._server.start()
        addrPortAction.setText(self.tr("Port: ") + str(self._server.port()))

        self._discoveryService.start(self._server.port())

        QTimer.singleShot(0,
                          lambda: self.showMessage(QApplication.applicationName(),
                                                   QApplication.applicationName() + self.tr(" is launched here."))
                          )

    def sendActionTriggered(self) -> None:
        self._d = SelectFilesDialog(None, self._discoveryService)
        self._d.setAttribute(Qt.WA_DeleteOnClose)
        self._d.show()

    def openDownloadFolderActionTriggered(self) -> None:
        downloadPath = Settings.downloadPath()
        QDir().mkpath(downloadPath)
        QDesktopServices.openUrl(QUrl.fromLocalFile(downloadPath))

    def exitActionTriggered(self) -> None:
        QApplication.exit()

    def trayIconActivated(self, reason: QSystemTrayIcon.ActivationReason) -> None:
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.sendActionTriggered()

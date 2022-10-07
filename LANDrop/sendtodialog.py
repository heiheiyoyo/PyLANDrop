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
# /

# include <QMessageBox>
# include <QPushButton>

# include "filetransferdialog.h"
# include "filetransfersender.h"
# include "sendtodialog.h"
# include "ui_sendtodialog.h"

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtNetwork import *
from typing import List
from LANDrop.ui_sendtodialog import Ui_SendToDialog
from dataclasses import dataclass
from LANDrop.discoveryservice import DiscoveryService
from LANDrop.filetransfersender import FileTransferSender
from LANDrop.filetransferdialog import FileTransferDialog


class SendToDialog(QDialog):
    @dataclass
    class Endpoint:
        addr: QHostAddress
        port: int

    def __init__(self, parent: QWidget, files: List[QFile], discoveryService: DiscoveryService) -> None:
        super().__init__(parent)
        self.ui = Ui_SendToDialog()
        self.files = files
        self.hostsStringListModel = QStringListModel()
        self.endpoints: List[SendToDialog.Endpoint] = []
        self.discoveryTimer = QTimer()
        self.socket = QTcpSocket()
        self.socketTimeoutTimer = QTimer()

        self.ui.setupUi(self)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.ui.hostsListView.setModel(self.hostsStringListModel)
        self.ui.hostsListView.clicked.connect(self.hostsListViewClicked)
        self.ui.hostsListView.doubleClicked.connect(self.ui.buttonBox.accepted)

        self.ui.buttonBox.button(QDialogButtonBox.Ok).setText(self.tr("Send"))
        self.ui.buttonBox.button(
            QDialogButtonBox.Cancel).setText(self.tr("Cancel"))

        discoveryService.newHost.connect(self.newHost)
        self.discoveryTimer.timeout.connect(discoveryService.refresh)
        self.discoveryTimer.start(1000)
        discoveryService.refresh()

        self.socketTimeoutTimer.timeout.connect(self.socketTimeout)
        self.socketTimeoutTimer.setSingleShot(True)

    def newHost(self, deviceName: str, addr: QHostAddress, port: int) -> None:

        str_list = self.hostsStringListModel.stringList()
        if port == 0:
            for i in range(len(self.endpoints)):
                if self.endpoints[i].addr.isEqual(addr):
                    del self.endpoints[i]
                    del str_list[i]
                    self.hostsStringListModel.setStringList(str_list)
                    return
            return

        for i in range(len(self.endpoints)):
            if self.endpoints[i].addr.isEqual(addr):
                if str_list[i] != deviceName:
                    str_list[i] = deviceName
                    self.hostsStringListModel.setStringList(str_list)

                self.endpoints[i].port = port
                return
        self.endpoints.append(self.Endpoint(addr, port))
        str_list.append(deviceName)
        self.hostsStringListModel.setStringList(str_list)

    def hostsListViewClicked(self, index: QModelIndex) -> None:

        endpoint: SendToDialog.Endpoint = self.endpoints[index.row()]
        isV4 = True  # FIXME: 可能出错
        ipv4 = endpoint.addr.toIPv4Address()
        addr = QHostAddress(ipv4).toString(
        ) if isV4 else endpoint.addr.toString()
        self.ui.addrLineEdit.setText(addr)
        self.ui.portLineEdit.setText(str(endpoint.port))

    def accept(self) -> None:

        addr = self.ui.addrLineEdit.text()
        ok = False
        try:
            port = int(self.ui.portLineEdit.text())
            if port < 0 or port > 65535:
                raise ValueError
            ok = True
        except ValueError:
            pass

        if not ok:
            QMessageBox.critical(self, QApplication.applicationName(),
                                 self.tr("Invalid port. Please enter a number between 1 and 65535."))
            return

        self.socket = QTcpSocket(self)
        self.socket.connected.connect(self.socketConnected)
        self.socket.error.connect(self.socketErrorOccurred)

        self.socket.connectToHost(addr, port)
        self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
        self.setCursor(QCursor(Qt.WaitCursor))
        self.socketTimeoutTimer.start(5000)

    def socketConnected(self) -> None:
        self.socketTimeoutTimer.stop()
        sender = FileTransferSender(None, self.socket, self.files)
        self._d = FileTransferDialog(None, sender)
        self._d.setAttribute(Qt.WA_DeleteOnClose)
        self._d.show()
        self.done(self.Accepted)

    def socketErrorOccurred(self) -> None:
        self.socketTimeoutTimer.stop()
        self.socket.disconnectFromHost()
        self.socket.close()
        self.socket.deleteLater()
        QMessageBox.critical(
            self, QApplication.applicationName(), self.socket.errorString())
        self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
        self.setCursor(QCursor(Qt.ArrowCursor))

    def socketTimeout(self) -> None:
        self.socket.disconnectFromHost()
        self.socket.close()
        self.socket.deleteLater()
        QMessageBox.critical(
            self, QApplication.applicationName(), self.tr("Connection timed out"))
        self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
        self.setCursor(QCursor(Qt.ArrowCursor))

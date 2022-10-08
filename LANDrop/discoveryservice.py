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
from typing import List, Optional
from PyQt6.QtCore import QObject, pyqtSignal, QSysInfo
from PyQt6.QtWidgets import QMessageBox, QApplication
from PyQt6.QtNetwork import QHostAddress, QUdpSocket, QNetworkInterface
from LANDrop.settings import Settings

DISCOVERY_PORT = 52637


class DiscoveryService(QObject):
    newHost = pyqtSignal(str, QHostAddress, int)  # deviceName,addr,port

    def __init__(self, parent: Optional['QObject'] = None) -> None:
        super().__init__(parent)
        self.socket = QUdpSocket()
        self.serverPort = None
        self.socket.readyRead.connect(self.socketReadyRead)

    def start(self, serverPort: int) -> None:
        self.serverPort = serverPort
        if not self.socket.bind(QHostAddress.SpecialAddress.Any, DISCOVERY_PORT):
            QMessageBox.warning(None, QApplication.applicationName(),
                                self.tr(
                                    "Unable to bind to port %1.\nYour device won't be discoverable."
            ).replace(
                                    "%1", str(DISCOVERY_PORT)))
        for addr in self.broadcastAddresses():
            self.sendInfo(addr, DISCOVERY_PORT)

    def refresh(self) -> None:
        obj = {"request": True}
        jsond = json.dumps(obj, ensure_ascii=False).encode('utf-8')
        for addr in self.broadcastAddresses():
            self.socket.writeDatagram(jsond, addr, DISCOVERY_PORT)

    def sendInfo(self, addr: QHostAddress, port: int) -> None:
        obj = {
            "request": False,
            "device_name": Settings.deviceName(),
            "device_type": QSysInfo.productType(),
            "port": self.serverPort if Settings.discoverable() else 0
        }
        self.socket.writeDatagram(json.dumps(
            obj, ensure_ascii=False).encode('utf-8'), addr, port)

    def isLocalAddress(self, addr: QHostAddress) -> bool:
        for address in QNetworkInterface.allAddresses():
            if addr.isEqual(address):
                return True
        return False

    def broadcastAddresses(self) -> List[QHostAddress]:
        ret = [QHostAddress.SpecialAddress.Broadcast]
        for i in QNetworkInterface.allInterfaces():
            if i.flags() & QNetworkInterface.InterfaceFlag.CanBroadcast:
                for e in i.addressEntries():
                    ret.append(e.broadcast())

        return ret

    def socketReadyRead(self) -> None:
        while self.socket.hasPendingDatagrams():
            size = self.socket.pendingDatagramSize()
            data, addr, port = self.socket.readDatagram(size)

            if self.isLocalAddress(addr):
                continue
            try:
                obj = json.loads(data)
            except json.JSONDecodeError:
                continue
            request = obj["request"]
            if not isinstance(request, bool):
                continue
            if request:
                self.sendInfo(addr, port)
                continue
            deviceName = obj["device_name"]
            remotePort = obj["port"]
            if not isinstance(deviceName, str) or not isinstance(remotePort, (int, float)):
                continue
            self.newHost.emit(deviceName, addr, remotePort)

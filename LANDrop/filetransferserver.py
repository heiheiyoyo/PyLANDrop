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


from PyQt6.QtCore import QObject,Qt
from PyQt6.QtNetwork import QTcpServer, QHostAddress
from typing import Optional
from LANDrop.settings import Settings
from LANDrop.filetransferreceiver import FileTransferReceiver
from LANDrop.filetransferdialog import FileTransferDialog


class FileTransferServer(QObject):
    def __init__(self, parent: Optional['QObject'] = None) -> None:
        super().__init__(parent)
        self.server = QTcpServer()
        self._d = None

    def start(self) -> None:
        port = Settings.serverPort()
        if not self.server.listen(QHostAddress.SpecialAddress.Any, port):
            raise RuntimeError(self.tr("Unable to listen on port %1.").replace("%1", str(port)))

        self.server.newConnection.connect(self.serverNewConnection)

    def port(self) -> int:
        return self.server.serverPort()

    def serverNewConnection(self) -> None:
        while self.server.hasPendingConnections():
            receiver = FileTransferReceiver(None, self.server.nextPendingConnection())
            self._d = FileTransferDialog(None, receiver)
            self._d.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

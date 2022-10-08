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

from PyQt6.QtCore import QFile, QIODevice, QStringListModel, QFileInfo, Qt
from PyQt6.QtWidgets import QDialog, QWidget, QDialogButtonBox, QMessageBox, QApplication, QFileDialog
from PyQt6.QtGui import QDropEvent, QDragEnterEvent
from LANDrop.ui_selectfilesdialog import Ui_SelectFilesDialog
from LANDrop.discoveryservice import DiscoveryService
from LANDrop.sendtodialog import SendToDialog
from typing import List


class SelectFilesDialog(QDialog):

    def __init__(self, parent: QWidget, discoveryService: DiscoveryService) -> None:
        super().__init__(parent)
        self.ui = Ui_SelectFilesDialog()
        self.discoveryService = discoveryService
        self.files: List[QFile] = []
        self.filesStringListModel = QStringListModel()
        self._d = None

        self.ui.setupUi(self)
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        self.ui.addButton.clicked.connect(self.addButtonClicked)
        self.ui.removeButton.clicked.connect(self.removeButtonClicked)
        self.ui.filesListView.setModel(self.filesStringListModel)

        self.ui.buttonBox.button(QDialogButtonBox.StandardButton.Ok).setText(self.tr("Send"))
        self.ui.buttonBox.button(
            QDialogButtonBox.StandardButton.Cancel).setText(self.tr("Cancel"))

    def addFile(self, filename: str) -> None:
        for file in self.files:
            if file.fileName() == filename:
                return

        fp = QFile(filename)
        if not fp.open(QIODevice.OpenModeFlag.ReadOnly):
            QMessageBox.critical(self, QApplication.applicationName(),
                                 self.tr("Unable to open file %1. Skipping.")
                                 .replace("%1", filename))
            return

        if fp.isSequential():
            QMessageBox.critical(self, QApplication.applicationName(),
                                 self.tr("%1 is not a regular file. Skipping.")
                                 .replace("%1", filename))
            return

        self.files.append(fp)

    def updateFileStringListModel(self) -> None:
        l = []
        for file in self.files:
            l.append(QFileInfo(file).fileName())

        self.filesStringListModel.setStringList(l)

    def addButtonClicked(self) -> None:
        filenames, _ = QFileDialog.getOpenFileNames(
            None, self.tr("Select File(s) to be Sent"))
        if not filenames:
            return

        for filename in filenames:
            self.addFile(filename)

        self.updateFileStringListModel()

    def removeButtonClicked(self) -> None:

        indexes = self.ui.filesListView.selectionModel().selectedIndexes()
        removeList = []
        for i in indexes:
            removeList.append(self.files[i.row()])
        for fp in removeList:
            self.files.remove(fp)

        self.updateFileStringListModel()

    def accept(self) -> None:

        if not self.files:
            QMessageBox.warning(
                self, QApplication.applicationName(), self.tr("No file to be sent."))
            return

        self._d = SendToDialog(None, self.files, self.discoveryService)
        self._d.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self._d.show()

        self.done(self.DialogCode.Accepted)

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent) -> None:
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                self.addFile(url.toLocalFile())

            self.updateFileStringListModel()
            event.acceptProposedAction()

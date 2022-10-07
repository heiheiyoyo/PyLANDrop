# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'filetransferdialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_FileTransferDialog(object):
    def setupUi(self, FileTransferDialog):
        if not FileTransferDialog.objectName():
            FileTransferDialog.setObjectName(u"FileTransferDialog")
        FileTransferDialog.resize(400, 66)
        self.verticalLayout = QVBoxLayout(FileTransferDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.statusLabel = QLabel(FileTransferDialog)
        self.statusLabel.setObjectName(u"statusLabel")

        self.verticalLayout.addWidget(self.statusLabel)

        self.progressBar = QProgressBar(FileTransferDialog)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setMaximum(10000)
        self.progressBar.setValue(0)

        self.verticalLayout.addWidget(self.progressBar)


        self.retranslateUi(FileTransferDialog)

        QMetaObject.connectSlotsByName(FileTransferDialog)
    # setupUi

    def retranslateUi(self, FileTransferDialog):
        FileTransferDialog.setWindowTitle(QCoreApplication.translate("FileTransferDialog", u"Transferring", None))
        self.statusLabel.setText("")
    # retranslateUi


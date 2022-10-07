# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'sendtodialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_SendToDialog(object):
    def setupUi(self, SendToDialog):
        if not SendToDialog.objectName():
            SendToDialog.setObjectName(u"SendToDialog")
        SendToDialog.resize(218, 300)
        self.verticalLayout = QVBoxLayout(SendToDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.addrLineEdit = QLineEdit(SendToDialog)
        self.addrLineEdit.setObjectName(u"addrLineEdit")

        self.horizontalLayout.addWidget(self.addrLineEdit)

        self.colon = QLabel(SendToDialog)
        self.colon.setObjectName(u"colon")

        self.horizontalLayout.addWidget(self.colon)

        self.portLineEdit = QLineEdit(SendToDialog)
        self.portLineEdit.setObjectName(u"portLineEdit")
        self.portLineEdit.setMaxLength(5)

        self.horizontalLayout.addWidget(self.portLineEdit)

        self.horizontalLayout.setStretch(0, 3)
        self.horizontalLayout.setStretch(2, 1)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.hostsListView = QListView(SendToDialog)
        self.hostsListView.setObjectName(u"hostsListView")
        self.hostsListView.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.verticalLayout.addWidget(self.hostsListView)

        self.buttonBox = QDialogButtonBox(SendToDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(SendToDialog)
        self.buttonBox.accepted.connect(SendToDialog.accept)
        self.buttonBox.rejected.connect(SendToDialog.reject)

        QMetaObject.connectSlotsByName(SendToDialog)
    # setupUi

    def retranslateUi(self, SendToDialog):
        SendToDialog.setWindowTitle(QCoreApplication.translate("SendToDialog", u"Send to", None))
        self.addrLineEdit.setText("")
        self.addrLineEdit.setPlaceholderText(QCoreApplication.translate("SendToDialog", u"Address", None))
        self.colon.setText(QCoreApplication.translate("SendToDialog", u":", None))
        self.portLineEdit.setText("")
        self.portLineEdit.setPlaceholderText(QCoreApplication.translate("SendToDialog", u"Port", None))
    # retranslateUi


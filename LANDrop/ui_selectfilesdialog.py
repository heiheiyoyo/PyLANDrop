# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'selectfilesdialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_SelectFilesDialog(object):
    def setupUi(self, SelectFilesDialog):
        if not SelectFilesDialog.objectName():
            SelectFilesDialog.setObjectName(u"SelectFilesDialog")
        SelectFilesDialog.resize(390, 383)
        SelectFilesDialog.setAcceptDrops(True)
        self.verticalLayout = QVBoxLayout(SelectFilesDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.instructionLabel = QLabel(SelectFilesDialog)
        self.instructionLabel.setObjectName(u"instructionLabel")

        self.verticalLayout.addWidget(self.instructionLabel)

        self.filesListView = QListView(SelectFilesDialog)
        self.filesListView.setObjectName(u"filesListView")
        self.filesListView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.filesListView.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.verticalLayout.addWidget(self.filesListView)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.addButton = QPushButton(SelectFilesDialog)
        self.addButton.setObjectName(u"addButton")

        self.horizontalLayout.addWidget(self.addButton)

        self.removeButton = QPushButton(SelectFilesDialog)
        self.removeButton.setObjectName(u"removeButton")

        self.horizontalLayout.addWidget(self.removeButton)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.buttonBox = QDialogButtonBox(SelectFilesDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(SelectFilesDialog)
        self.buttonBox.accepted.connect(SelectFilesDialog.accept)
        self.buttonBox.rejected.connect(SelectFilesDialog.reject)

        QMetaObject.connectSlotsByName(SelectFilesDialog)
    # setupUi

    def retranslateUi(self, SelectFilesDialog):
        SelectFilesDialog.setWindowTitle(QCoreApplication.translate("SelectFilesDialog", u"Select File(s) to be Sent", None))
        self.instructionLabel.setText(QCoreApplication.translate("SelectFilesDialog", u"You can drag files to this window:", None))
        self.addButton.setText(QCoreApplication.translate("SelectFilesDialog", u"Add...", None))
        self.removeButton.setText(QCoreApplication.translate("SelectFilesDialog", u"Remove", None))
    # retranslateUi


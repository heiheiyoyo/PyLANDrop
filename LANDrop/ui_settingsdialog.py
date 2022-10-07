# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settingsdialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_SettingsDialog(object):
    def setupUi(self, SettingsDialog):
        if not SettingsDialog.objectName():
            SettingsDialog.setObjectName(u"SettingsDialog")
        SettingsDialog.resize(400, 242)
        self.verticalLayout = QVBoxLayout(SettingsDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.basicGroupBox = QGroupBox(SettingsDialog)
        self.basicGroupBox.setObjectName(u"basicGroupBox")
        self.formLayout_3 = QFormLayout(self.basicGroupBox)
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.deviceNameLabel = QLabel(self.basicGroupBox)
        self.deviceNameLabel.setObjectName(u"deviceNameLabel")

        self.formLayout_3.setWidget(0, QFormLayout.LabelRole, self.deviceNameLabel)

        self.deviceNameLineEdit = QLineEdit(self.basicGroupBox)
        self.deviceNameLineEdit.setObjectName(u"deviceNameLineEdit")
        self.deviceNameLineEdit.setMaxLength(64)

        self.formLayout_3.setWidget(0, QFormLayout.FieldRole, self.deviceNameLineEdit)

        self.downloadPathLabel = QLabel(self.basicGroupBox)
        self.downloadPathLabel.setObjectName(u"downloadPathLabel")

        self.formLayout_3.setWidget(1, QFormLayout.LabelRole, self.downloadPathLabel)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.downloadPathLineEdit = QLineEdit(self.basicGroupBox)
        self.downloadPathLineEdit.setObjectName(u"downloadPathLineEdit")

        self.horizontalLayout.addWidget(self.downloadPathLineEdit)

        self.downloadPathSelectButton = QToolButton(self.basicGroupBox)
        self.downloadPathSelectButton.setObjectName(u"downloadPathSelectButton")

        self.horizontalLayout.addWidget(self.downloadPathSelectButton)


        self.formLayout_3.setLayout(1, QFormLayout.FieldRole, self.horizontalLayout)

        self.discoverableLabel = QLabel(self.basicGroupBox)
        self.discoverableLabel.setObjectName(u"discoverableLabel")

        self.formLayout_3.setWidget(2, QFormLayout.LabelRole, self.discoverableLabel)

        self.discoverableCheckBox = QCheckBox(self.basicGroupBox)
        self.discoverableCheckBox.setObjectName(u"discoverableCheckBox")

        self.formLayout_3.setWidget(2, QFormLayout.FieldRole, self.discoverableCheckBox)


        self.verticalLayout.addWidget(self.basicGroupBox)

        self.advancedGroupBox = QGroupBox(SettingsDialog)
        self.advancedGroupBox.setObjectName(u"advancedGroupBox")
        self.formLayout = QFormLayout(self.advancedGroupBox)
        self.formLayout.setObjectName(u"formLayout")
        self.serverPortLabel = QLabel(self.advancedGroupBox)
        self.serverPortLabel.setObjectName(u"serverPortLabel")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.serverPortLabel)

        self.serverPortLineEdit = QLineEdit(self.advancedGroupBox)
        self.serverPortLineEdit.setObjectName(u"serverPortLineEdit")
        self.serverPortLineEdit.setMaxLength(5)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.serverPortLineEdit)


        self.verticalLayout.addWidget(self.advancedGroupBox)

        self.buttonBox = QDialogButtonBox(SettingsDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(SettingsDialog)
        self.buttonBox.accepted.connect(SettingsDialog.accept)
        self.buttonBox.rejected.connect(SettingsDialog.reject)

        QMetaObject.connectSlotsByName(SettingsDialog)
    # setupUi

    def retranslateUi(self, SettingsDialog):
        SettingsDialog.setWindowTitle(QCoreApplication.translate("SettingsDialog", u"Settings", None))
        self.basicGroupBox.setTitle(QCoreApplication.translate("SettingsDialog", u"Basic", None))
        self.deviceNameLabel.setText(QCoreApplication.translate("SettingsDialog", u"Device Name", None))
        self.downloadPathLabel.setText(QCoreApplication.translate("SettingsDialog", u"Download Path", None))
        self.downloadPathSelectButton.setText(QCoreApplication.translate("SettingsDialog", u"...", None))
        self.discoverableLabel.setText(QCoreApplication.translate("SettingsDialog", u"Discoverable", None))
        self.discoverableCheckBox.setText("")
        self.advancedGroupBox.setTitle(QCoreApplication.translate("SettingsDialog", u"Advanced", None))
        self.serverPortLabel.setText(QCoreApplication.translate("SettingsDialog", u"Server Port", None))
    # retranslateUi


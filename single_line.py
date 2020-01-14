# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'single_line.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Single_Dialog(object):
    def setupUi(self, Single_Dialog):
        Single_Dialog.setObjectName("Single_Dialog")
        Single_Dialog.resize(380, 102)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Single_Dialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.lineEdit = QtWidgets.QLineEdit(Single_Dialog)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout.addWidget(self.lineEdit)
        self.buttonBox = QtWidgets.QDialogButtonBox(Single_Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(Single_Dialog)
        self.buttonBox.accepted.connect(Single_Dialog.accept)
        self.buttonBox.rejected.connect(Single_Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Single_Dialog)

    def retranslateUi(self, Single_Dialog):
        _translate = QtCore.QCoreApplication.translate
        Single_Dialog.setWindowTitle(_translate("Single_Dialog", "Dialog"))


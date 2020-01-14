# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tab_edit.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_tabEdit_Dialog(object):
    def setupUi(self, tabEdit_Dialog):
        tabEdit_Dialog.setObjectName("tabEdit_Dialog")
        tabEdit_Dialog.resize(386, 236)
        font = QtGui.QFont()
        font.setFamily("Constantia")
        font.setPointSize(12)
        tabEdit_Dialog.setFont(font)
        self.verticalLayout = QtWidgets.QVBoxLayout(tabEdit_Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(tabEdit_Dialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.index_comboBox = QtWidgets.QComboBox(tabEdit_Dialog)
        self.index_comboBox.setObjectName("index_comboBox")
        self.gridLayout.addWidget(self.index_comboBox, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(tabEdit_Dialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.nameEdit = QtWidgets.QLineEdit(tabEdit_Dialog)
        self.nameEdit.setObjectName("nameEdit")
        self.gridLayout.addWidget(self.nameEdit, 1, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(tabEdit_Dialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.category_comboBox = QtWidgets.QComboBox(tabEdit_Dialog)
        self.category_comboBox.setObjectName("category_comboBox")
        self.gridLayout.addWidget(self.category_comboBox, 2, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(tabEdit_Dialog)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.checkBox = QtWidgets.QCheckBox(tabEdit_Dialog)
        self.checkBox.setText("")
        self.checkBox.setObjectName("checkBox")
        self.gridLayout.addWidget(self.checkBox, 3, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(tabEdit_Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(tabEdit_Dialog)
        self.buttonBox.accepted.connect(tabEdit_Dialog.accept)
        self.buttonBox.rejected.connect(tabEdit_Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(tabEdit_Dialog)

    def retranslateUi(self, tabEdit_Dialog):
        _translate = QtCore.QCoreApplication.translate
        tabEdit_Dialog.setWindowTitle(_translate("tabEdit_Dialog", "Dialog"))
        self.label_2.setText(_translate("tabEdit_Dialog", "Index"))
        self.label.setText(_translate("tabEdit_Dialog", "Name"))
        self.label_3.setText(_translate("tabEdit_Dialog", "Linked category"))
        self.label_4.setText(_translate("tabEdit_Dialog", "Active"))


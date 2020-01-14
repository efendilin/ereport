# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'conclusion_dia.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Conclusion_Dialog(object):
    def setupUi(self, Conclusion_Dialog):
        Conclusion_Dialog.setObjectName("Conclusion_Dialog")
        Conclusion_Dialog.resize(640, 480)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(12)
        Conclusion_Dialog.setFont(font)
        self.verticalLayout = QtWidgets.QVBoxLayout(Conclusion_Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableWidget = QtWidgets.QTableWidget(Conclusion_Dialog)
        self.tableWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContentsOnFirstShow)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setRowCount(0)
        self.verticalLayout.addWidget(self.tableWidget)
        self.buttonBox = QtWidgets.QDialogButtonBox(Conclusion_Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Conclusion_Dialog)
        self.buttonBox.accepted.connect(Conclusion_Dialog.accept)
        self.buttonBox.rejected.connect(Conclusion_Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Conclusion_Dialog)

    def retranslateUi(self, Conclusion_Dialog):
        _translate = QtCore.QCoreApplication.translate
        Conclusion_Dialog.setWindowTitle(_translate("Conclusion_Dialog", "Dialog"))


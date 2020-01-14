# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'importDiag.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_import_Dialog(object):
    def setupUi(self, import_Dialog):
        import_Dialog.setObjectName("import_Dialog")
        import_Dialog.resize(985, 592)
        self.verticalLayout = QtWidgets.QVBoxLayout(import_Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableWidget = QtWidgets.QTableWidget(import_Dialog)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        self.verticalLayout.addWidget(self.tableWidget)
        self.buttonBox = QtWidgets.QDialogButtonBox(import_Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(import_Dialog)
        self.buttonBox.accepted.connect(import_Dialog.accept)
        self.buttonBox.rejected.connect(import_Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(import_Dialog)

    def retranslateUi(self, import_Dialog):
        _translate = QtCore.QCoreApplication.translate
        import_Dialog.setWindowTitle(_translate("import_Dialog", "Dialog"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("import_Dialog", "Selected"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("import_Dialog", "Template"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("import_Dialog", "Shortcut"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("import_Dialog", "Category"))


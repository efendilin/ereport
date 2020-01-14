# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'simple_noted.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_simple_note_Dialog(object):
    def setupUi(self, simple_note_Dialog):
        simple_note_Dialog.setObjectName("simple_note_Dialog")
        simple_note_Dialog.resize(500, 500)
        simple_note_Dialog.setMinimumSize(QtCore.QSize(500, 500))
        simple_note_Dialog.setMaximumSize(QtCore.QSize(500, 500))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(12)
        simple_note_Dialog.setFont(font)
        self.gridLayout = QtWidgets.QGridLayout(simple_note_Dialog)
        self.gridLayout.setObjectName("gridLayout")

        self.retranslateUi(simple_note_Dialog)
        QtCore.QMetaObject.connectSlotsByName(simple_note_Dialog)

    def retranslateUi(self, simple_note_Dialog):
        _translate = QtCore.QCoreApplication.translate
        simple_note_Dialog.setWindowTitle(_translate("simple_note_Dialog", "Dialog"))


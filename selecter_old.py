# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'selecter.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Select_Dialog(object):
    def setupUi(self, Select_Dialog):
        Select_Dialog.setObjectName("Select_Dialog")
        Select_Dialog.resize(400, 440)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Select_Dialog.sizePolicy().hasHeightForWidth())
        Select_Dialog.setSizePolicy(sizePolicy)
        Select_Dialog.setMinimumSize(QtCore.QSize(400, 400))
        Select_Dialog.setMaximumSize(QtCore.QSize(1000, 1000))
        Select_Dialog.setSizeIncrement(QtCore.QSize(500, 500))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(14)
        Select_Dialog.setFont(font)
        self.verticalLayout = QtWidgets.QVBoxLayout(Select_Dialog)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scrollArea = QtWidgets.QScrollArea(Select_Dialog)
        self.scrollArea.setMinimumSize(QtCore.QSize(350, 350))
        self.scrollArea.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.scrollArea.setAutoFillBackground(False)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContentsOnFirstShow)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 380, 384))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollAreaWidgetContents.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents.setSizePolicy(sizePolicy)
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_0 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_0.setMaximumSize(QtCore.QSize(380, 60))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(14)
        self.label_0.setFont(font)
        self.label_0.setScaledContents(False)
        self.label_0.setWordWrap(True)
        self.label_0.setObjectName("label_0")
        self.gridLayout.addWidget(self.label_0, 0, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)
        self.buttonBox = QtWidgets.QDialogButtonBox(Select_Dialog)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(14)
        self.buttonBox.setFont(font)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Select_Dialog)
        self.buttonBox.accepted.connect(Select_Dialog.accept)
        self.buttonBox.rejected.connect(Select_Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Select_Dialog)

    def retranslateUi(self, Select_Dialog):
        _translate = QtCore.QCoreApplication.translate
        Select_Dialog.setWindowTitle(_translate("Select_Dialog", "Selector"))
        self.label_0.setText(_translate("Select_Dialog", "TextLabel"))


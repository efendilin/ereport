# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'checklist_o.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(640, 800)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QtCore.QSize(640, 800))
        Form.setMaximumSize(QtCore.QSize(640, 800))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(12)
        Form.setFont(font)
        Form.setFocusPolicy(QtCore.Qt.StrongFocus)
        Form.setAutoFillBackground(True)
        self.patient_id = QtWidgets.QLineEdit(Form)
        self.patient_id.setGeometry(QtCore.QRect(110, 10, 161, 21))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        self.patient_id.setFont(font)
        self.patient_id.setObjectName("patient_id")
        self.pid_lab = QtWidgets.QLabel(Form)
        self.pid_lab.setGeometry(QtCore.QRect(10, 10, 101, 21))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        self.pid_lab.setFont(font)
        self.pid_lab.setObjectName("pid_lab")
        self.addButton = QtWidgets.QPushButton(Form)
        self.addButton.setGeometry(QtCore.QRect(280, 10, 51, 23))
        self.addButton.setObjectName("addButton")
        self.patient_comboBox = QtWidgets.QComboBox(Form)
        self.patient_comboBox.setGeometry(QtCore.QRect(340, 10, 191, 22))
        self.patient_comboBox.setObjectName("patient_comboBox")
        self.cleanButton = QtWidgets.QPushButton(Form)
        self.cleanButton.setGeometry(QtCore.QRect(540, 10, 75, 23))
        self.cleanButton.setObjectName("cleanButton")
        self.layoutWidget = QtWidgets.QWidget(Form)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 760, 611, 34))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.test_Button = QtWidgets.QPushButton(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Noto Sans CJK TC Light")
        self.test_Button.setFont(font)
        self.test_Button.setObjectName("test_Button")
        self.horizontalLayout.addWidget(self.test_Button)
        self.minput_Button = QtWidgets.QPushButton(self.layoutWidget)
        self.minput_Button.setObjectName("minput_Button")
        self.horizontalLayout.addWidget(self.minput_Button)
        self.take_Button = QtWidgets.QPushButton(self.layoutWidget)
        self.take_Button.setObjectName("take_Button")
        self.horizontalLayout.addWidget(self.take_Button)
        self.clear_Button = QtWidgets.QPushButton(self.layoutWidget)
        self.clear_Button.setObjectName("clear_Button")
        self.horizontalLayout.addWidget(self.clear_Button)
        self.layoutWidget_2 = QtWidgets.QWidget(Form)
        self.layoutWidget_2.setGeometry(QtCore.QRect(10, 40, 611, 34))
        self.layoutWidget_2.setObjectName("layoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.layoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.seetingBox = QtWidgets.QComboBox(self.layoutWidget_2)
        self.seetingBox.setObjectName("seetingBox")
        self.horizontalLayout_2.addWidget(self.seetingBox)
        self.minput_Button_2 = QtWidgets.QPushButton(self.layoutWidget_2)
        self.minput_Button_2.setObjectName("minput_Button_2")
        self.horizontalLayout_2.addWidget(self.minput_Button_2)
        self.seeting_Button = QtWidgets.QPushButton(self.layoutWidget_2)
        self.seeting_Button.setObjectName("seeting_Button")
        self.horizontalLayout_2.addWidget(self.seeting_Button)
        self.save_Button = QtWidgets.QPushButton(self.layoutWidget_2)
        self.save_Button.setObjectName("save_Button")
        self.horizontalLayout_2.addWidget(self.save_Button)
        self.layoutWidget1 = QtWidgets.QWidget(Form)
        self.layoutWidget1.setGeometry(QtCore.QRect(3, 79, 631, 301))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(11)
        self.tabWidget.setFont(font)
        self.tabWidget.setObjectName("tabWidget")
        self.brain = QtWidgets.QWidget()
        self.brain.setObjectName("brain")
        self.gridLayout = QtWidgets.QGridLayout(self.brain)
        self.gridLayout.setObjectName("gridLayout")
        self.combo_brain = QtWidgets.QComboBox(self.brain)
        self.combo_brain.setObjectName("combo_brain")
        self.combo_brain.addItem("")
        self.combo_brain.addItem("")
        self.combo_brain.addItem("")
        self.combo_brain.addItem("")
        self.gridLayout.addWidget(self.combo_brain, 0, 0, 1, 1)
        self.combo_brain_check = QtWidgets.QPushButton(self.brain)
        self.combo_brain_check.setObjectName("combo_brain_check")
        self.gridLayout.addWidget(self.combo_brain_check, 0, 1, 1, 1)
        self.tabWidget.addTab(self.brain, "")
        self.head_neck = QtWidgets.QWidget()
        self.head_neck.setObjectName("head_neck")
        self.layoutWidget2 = QtWidgets.QWidget(self.head_neck)
        self.layoutWidget2.setGeometry(QtCore.QRect(10, 10, 611, 28))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.layoutWidget2)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.combo_hn = QtWidgets.QComboBox(self.layoutWidget2)
        self.combo_hn.setObjectName("combo_hn")
        self.combo_hn.addItem("")
        self.combo_hn.addItem("")
        self.combo_hn.addItem("")
        self.combo_hn.addItem("")
        self.horizontalLayout_3.addWidget(self.combo_hn)
        self.combo_hn_check = QtWidgets.QPushButton(self.layoutWidget2)
        self.combo_hn_check.setObjectName("combo_hn_check")
        self.horizontalLayout_3.addWidget(self.combo_hn_check)
        self.tabWidget.addTab(self.head_neck, "")
        self.lung = QtWidgets.QWidget()
        self.lung.setObjectName("lung")
        self.layoutWidget3 = QtWidgets.QWidget(self.lung)
        self.layoutWidget3.setGeometry(QtCore.QRect(9, 10, 611, 28))
        self.layoutWidget3.setObjectName("layoutWidget3")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.layoutWidget3)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.combo_lung = QtWidgets.QComboBox(self.layoutWidget3)
        self.combo_lung.setObjectName("combo_lung")
        self.combo_lung.addItem("")
        self.combo_lung.addItem("")
        self.combo_lung.addItem("")
        self.combo_lung.addItem("")
        self.horizontalLayout_4.addWidget(self.combo_lung)
        self.combo_lung_check = QtWidgets.QPushButton(self.layoutWidget3)
        self.combo_lung_check.setObjectName("combo_lung_check")
        self.horizontalLayout_4.addWidget(self.combo_lung_check)
        self.tabWidget.addTab(self.lung, "")
        self.med = QtWidgets.QWidget()
        self.med.setObjectName("med")
        self.layoutWidget4 = QtWidgets.QWidget(self.med)
        self.layoutWidget4.setGeometry(QtCore.QRect(9, 10, 611, 28))
        self.layoutWidget4.setObjectName("layoutWidget4")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.layoutWidget4)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.combo_med = QtWidgets.QComboBox(self.layoutWidget4)
        self.combo_med.setObjectName("combo_med")
        self.combo_med.addItem("")
        self.combo_med.addItem("")
        self.combo_med.addItem("")
        self.combo_med.addItem("")
        self.gridLayout_2.addWidget(self.combo_med, 0, 0, 1, 1)
        self.combo_med_check = QtWidgets.QPushButton(self.layoutWidget4)
        self.combo_med_check.setObjectName("combo_med_check")
        self.gridLayout_2.addWidget(self.combo_med_check, 0, 1, 1, 1)
        self.tabWidget.addTab(self.med, "")
        self.abd = QtWidgets.QWidget()
        self.abd.setObjectName("abd")
        self.layoutWidget5 = QtWidgets.QWidget(self.abd)
        self.layoutWidget5.setGeometry(QtCore.QRect(9, 10, 611, 28))
        self.layoutWidget5.setObjectName("layoutWidget5")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.layoutWidget5)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.combo_abd = QtWidgets.QComboBox(self.layoutWidget5)
        self.combo_abd.setObjectName("combo_abd")
        self.combo_abd.addItem("")
        self.combo_abd.addItem("")
        self.combo_abd.addItem("")
        self.combo_abd.addItem("")
        self.gridLayout_3.addWidget(self.combo_abd, 0, 0, 1, 1)
        self.combo_abd_check = QtWidgets.QPushButton(self.layoutWidget5)
        self.combo_abd_check.setObjectName("combo_abd_check")
        self.gridLayout_3.addWidget(self.combo_abd_check, 0, 1, 1, 1)
        self.tabWidget.addTab(self.abd, "")
        self.pelvic = QtWidgets.QWidget()
        self.pelvic.setObjectName("pelvic")
        self.layoutWidget6 = QtWidgets.QWidget(self.pelvic)
        self.layoutWidget6.setGeometry(QtCore.QRect(10, 10, 611, 28))
        self.layoutWidget6.setObjectName("layoutWidget6")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.layoutWidget6)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.combo_pelvic = QtWidgets.QComboBox(self.layoutWidget6)
        self.combo_pelvic.setObjectName("combo_pelvic")
        self.combo_pelvic.addItem("")
        self.combo_pelvic.addItem("")
        self.combo_pelvic.addItem("")
        self.combo_pelvic.addItem("")
        self.gridLayout_4.addWidget(self.combo_pelvic, 0, 0, 1, 1)
        self.combo_pelvic_check = QtWidgets.QPushButton(self.layoutWidget6)
        self.combo_pelvic_check.setObjectName("combo_pelvic_check")
        self.gridLayout_4.addWidget(self.combo_pelvic_check, 0, 1, 1, 1)
        self.tabWidget.addTab(self.pelvic, "")
        self.others = QtWidgets.QWidget()
        self.others.setObjectName("others")
        self.layoutWidget7 = QtWidgets.QWidget(self.others)
        self.layoutWidget7.setGeometry(QtCore.QRect(10, 10, 601, 28))
        self.layoutWidget7.setObjectName("layoutWidget7")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.layoutWidget7)
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.combo_others = QtWidgets.QComboBox(self.layoutWidget7)
        self.combo_others.setObjectName("combo_others")
        self.combo_others.addItem("")
        self.combo_others.addItem("")
        self.combo_others.addItem("")
        self.combo_others.addItem("")
        self.gridLayout_5.addWidget(self.combo_others, 0, 0, 1, 1)
        self.combo_others_check = QtWidgets.QPushButton(self.layoutWidget7)
        self.combo_others_check.setObjectName("combo_others_check")
        self.gridLayout_5.addWidget(self.combo_others_check, 0, 1, 1, 1)
        self.tabWidget.addTab(self.others, "")
        self.whole = QtWidgets.QWidget()
        self.whole.setObjectName("whole")
        self.layoutWidget8 = QtWidgets.QWidget(self.whole)
        self.layoutWidget8.setGeometry(QtCore.QRect(9, 10, 611, 28))
        self.layoutWidget8.setObjectName("layoutWidget8")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.layoutWidget8)
        self.gridLayout_6.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.combo_whole = QtWidgets.QComboBox(self.layoutWidget8)
        self.combo_whole.setObjectName("combo_whole")
        self.combo_whole.addItem("")
        self.combo_whole.addItem("")
        self.combo_whole.addItem("")
        self.combo_whole.addItem("")
        self.gridLayout_6.addWidget(self.combo_whole, 0, 0, 1, 1)
        self.combo_whole_check = QtWidgets.QPushButton(self.layoutWidget8)
        self.combo_whole_check.setObjectName("combo_whole_check")
        self.gridLayout_6.addWidget(self.combo_whole_check, 0, 1, 1, 1)
        self.tabWidget.addTab(self.whole, "")
        self.verticalLayout.addWidget(self.tabWidget)
        self.treeWidget = QtWidgets.QTreeWidget(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(12)
        self.treeWidget.setFont(font)
        self.treeWidget.setDragEnabled(False)
        self.treeWidget.setDragDropMode(QtWidgets.QAbstractItemView.NoDragDrop)
        self.treeWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.headerItem().setText(0, "shortcut")
        self.verticalLayout.addWidget(self.treeWidget)
        self.layoutWidget.raise_()
        self.layoutWidget.raise_()
        self.patient_id.raise_()
        self.pid_lab.raise_()
        self.addButton.raise_()
        self.patient_comboBox.raise_()
        self.cleanButton.raise_()
        self.layoutWidget_2.raise_()

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pid_lab.setText(_translate("Form", "Patient ID"))
        self.addButton.setText(_translate("Form", "Add"))
        self.cleanButton.setText(_translate("Form", "Clean"))
        self.test_Button.setText(_translate("Form", "Test"))
        self.minput_Button.setText(_translate("Form", "MInput"))
        self.take_Button.setText(_translate("Form", "TakeOut"))
        self.clear_Button.setText(_translate("Form", "Clear"))
        self.minput_Button_2.setText(_translate("Form", "MInput"))
        self.seeting_Button.setText(_translate("Form", "Seeting"))
        self.save_Button.setText(_translate("Form", "Save"))
        self.combo_brain.setCurrentText(_translate("Form", "Unchecked"))
        self.combo_brain.setItemText(0, _translate("Form", "Unchecked"))
        self.combo_brain.setItemText(1, _translate("Form", "Normal"))
        self.combo_brain.setItemText(2, _translate("Form", "Checked"))
        self.combo_brain.setItemText(3, _translate("Form", "Abnormal"))
        self.combo_brain_check.setText(_translate("Form", "Checked to next  -->"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.brain), _translate("Form", "*Brain"))
        self.combo_hn.setCurrentText(_translate("Form", "Unchecked"))
        self.combo_hn.setItemText(0, _translate("Form", "Unchecked"))
        self.combo_hn.setItemText(1, _translate("Form", "Normal"))
        self.combo_hn.setItemText(2, _translate("Form", "Checked"))
        self.combo_hn.setItemText(3, _translate("Form", "Abnormal"))
        self.combo_hn_check.setText(_translate("Form", "Checked to next  -->"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.head_neck), _translate("Form", "*H and N"))
        self.combo_lung.setCurrentText(_translate("Form", "Unchecked"))
        self.combo_lung.setItemText(0, _translate("Form", "Unchecked"))
        self.combo_lung.setItemText(1, _translate("Form", "Normal"))
        self.combo_lung.setItemText(2, _translate("Form", "Checked"))
        self.combo_lung.setItemText(3, _translate("Form", "Abnormal"))
        self.combo_lung_check.setText(_translate("Form", "Checked to next  -->"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.lung), _translate("Form", "*Lung"))
        self.combo_med.setCurrentText(_translate("Form", "Unchecked"))
        self.combo_med.setItemText(0, _translate("Form", "Unchecked"))
        self.combo_med.setItemText(1, _translate("Form", "Normal"))
        self.combo_med.setItemText(2, _translate("Form", "Checked"))
        self.combo_med.setItemText(3, _translate("Form", "Abnormal"))
        self.combo_med_check.setText(_translate("Form", "Checked to next  -->"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.med), _translate("Form", "*Med"))
        self.combo_abd.setCurrentText(_translate("Form", "Unchecked"))
        self.combo_abd.setItemText(0, _translate("Form", "Unchecked"))
        self.combo_abd.setItemText(1, _translate("Form", "Normal"))
        self.combo_abd.setItemText(2, _translate("Form", "Checked"))
        self.combo_abd.setItemText(3, _translate("Form", "Abnormal"))
        self.combo_abd_check.setText(_translate("Form", "Checked to next  -->"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.abd), _translate("Form", "*Abd"))
        self.combo_pelvic.setCurrentText(_translate("Form", "Unchecked"))
        self.combo_pelvic.setItemText(0, _translate("Form", "Unchecked"))
        self.combo_pelvic.setItemText(1, _translate("Form", "Normal"))
        self.combo_pelvic.setItemText(2, _translate("Form", "Checked"))
        self.combo_pelvic.setItemText(3, _translate("Form", "Abnormal"))
        self.combo_pelvic_check.setText(_translate("Form", "Checked to next  -->"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.pelvic), _translate("Form", "*Pelvic"))
        self.combo_others.setCurrentText(_translate("Form", "Unchecked"))
        self.combo_others.setItemText(0, _translate("Form", "Unchecked"))
        self.combo_others.setItemText(1, _translate("Form", "Normal"))
        self.combo_others.setItemText(2, _translate("Form", "Checked"))
        self.combo_others.setItemText(3, _translate("Form", "Abnormal"))
        self.combo_others_check.setText(_translate("Form", "Checked to next  -->"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.others), _translate("Form", "*Others"))
        self.combo_whole.setCurrentText(_translate("Form", "Unchecked"))
        self.combo_whole.setItemText(0, _translate("Form", "Unchecked"))
        self.combo_whole.setItemText(1, _translate("Form", "Normal"))
        self.combo_whole.setItemText(2, _translate("Form", "Checked"))
        self.combo_whole.setItemText(3, _translate("Form", "Abnormal"))
        self.combo_whole_check.setText(_translate("Form", "Checked to next  -->"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.whole), _translate("Form", "*Whole"))
        self.treeWidget.headerItem().setText(1, _translate("Form", "main"))
        self.treeWidget.headerItem().setText(2, _translate("Form", "index"))

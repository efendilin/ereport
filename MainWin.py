# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWin.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(640, 900)
        MainWindow.setMinimumSize(QtCore.QSize(640, 900))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(12)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.pid_lab = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        self.pid_lab.setFont(font)
        self.pid_lab.setObjectName("pid_lab")
        self.horizontalLayout_3.addWidget(self.pid_lab)
        self.patient_id = QtWidgets.QLineEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        self.patient_id.setFont(font)
        self.patient_id.setObjectName("patient_id")
        self.horizontalLayout_3.addWidget(self.patient_id)
        self.addButton = QtWidgets.QPushButton(self.centralwidget)
        self.addButton.setObjectName("addButton")
        self.horizontalLayout_3.addWidget(self.addButton)
        self.patient_comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.patient_comboBox.setMinimumSize(QtCore.QSize(200, 0))
        self.patient_comboBox.setAcceptDrops(False)
        self.patient_comboBox.setMaxVisibleItems(15)
        self.patient_comboBox.setInsertPolicy(QtWidgets.QComboBox.InsertAtBottom)
        self.patient_comboBox.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContentsOnFirstShow)
        self.patient_comboBox.setObjectName("patient_comboBox")
        self.horizontalLayout_3.addWidget(self.patient_comboBox)
        self.cleanButton = QtWidgets.QPushButton(self.centralwidget)
        self.cleanButton.setObjectName("cleanButton")
        self.horizontalLayout_3.addWidget(self.cleanButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.seetingBox = QtWidgets.QComboBox(self.centralwidget)
        self.seetingBox.setObjectName("seetingBox")
        self.horizontalLayout_2.addWidget(self.seetingBox)
        self.template_tool = QtWidgets.QToolButton(self.centralwidget)
        self.template_tool.setObjectName("template_tool")
        self.horizontalLayout_2.addWidget(self.template_tool)
        self.minput_Button_2 = QtWidgets.QPushButton(self.centralwidget)
        self.minput_Button_2.setObjectName("minput_Button_2")
        self.horizontalLayout_2.addWidget(self.minput_Button_2)
        self.note_Button = QtWidgets.QPushButton(self.centralwidget)
        self.note_Button.setObjectName("note_Button")
        self.horizontalLayout_2.addWidget(self.note_Button)
        self.save_Button = QtWidgets.QPushButton(self.centralwidget)
        self.save_Button.setObjectName("save_Button")
        self.horizontalLayout_2.addWidget(self.save_Button)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
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
        self.verticalLayout.addWidget(self.tabWidget)
        self.treeWidget = QtWidgets.QTreeWidget(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(12)
        self.treeWidget.setFont(font)
        self.treeWidget.setDragEnabled(False)
        self.treeWidget.setDragDropMode(QtWidgets.QAbstractItemView.NoDragDrop)
        self.treeWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.headerItem().setText(0, "Shortcut")
        font = QtGui.QFont()
        font.setFamily("Consolas")
        self.treeWidget.headerItem().setFont(0, font)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        self.treeWidget.headerItem().setFont(1, font)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        self.treeWidget.headerItem().setFont(2, font)
        self.verticalLayout.addWidget(self.treeWidget)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.report_tab = QtWidgets.QTabWidget(self.centralwidget)
        self.report_tab.setEnabled(True)
        self.report_tab.setMinimumSize(QtCore.QSize(0, 400))
        self.report_tab.setUsesScrollButtons(False)
        self.report_tab.setObjectName("report_tab")
        self.Findings = QtWidgets.QWidget()
        self.Findings.setObjectName("Findings")
        self.report_tab.addTab(self.Findings, "")
        self.verticalLayout_2.addWidget(self.report_tab)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Conculsion_Button = QtWidgets.QPushButton(self.centralwidget)
        self.Conculsion_Button.setObjectName("Conculsion_Button")
        self.horizontalLayout.addWidget(self.Conculsion_Button)
        self.take_Button = QtWidgets.QPushButton(self.centralwidget)
        self.take_Button.setObjectName("take_Button")
        self.horizontalLayout.addWidget(self.take_Button)
        self.clear_Button = QtWidgets.QPushButton(self.centralwidget)
        self.clear_Button.setObjectName("clear_Button")
        self.horizontalLayout.addWidget(self.clear_Button)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 640, 25))
        self.menubar.setObjectName("menubar")
        self.menuSeeting = QtWidgets.QMenu(self.menubar)
        self.menuSeeting.setObjectName("menuSeeting")
        self.menuDictionary = QtWidgets.QMenu(self.menubar)
        self.menuDictionary.setObjectName("menuDictionary")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionEdit_Dictionary = QtWidgets.QAction(MainWindow)
        self.actionEdit_Dictionary.setObjectName("actionEdit_Dictionary")
        self.actionReload_Disctionary = QtWidgets.QAction(MainWindow)
        self.actionReload_Disctionary.setObjectName("actionReload_Disctionary")
        self.menubar.addAction(self.menuSeeting.menuAction())
        self.menubar.addAction(self.menuDictionary.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(-1)
        self.report_tab.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pid_lab.setText(_translate("MainWindow", "Patient ID"))
        self.addButton.setText(_translate("MainWindow", "Add"))
        self.cleanButton.setText(_translate("MainWindow", "Pt Info"))
        self.template_tool.setText(_translate("MainWindow", "..."))
        self.minput_Button_2.setText(_translate("MainWindow", "MInput"))
        self.note_Button.setText(_translate("MainWindow", "Note"))
        self.save_Button.setText(_translate("MainWindow", "Save"))
        self.treeWidget.headerItem().setText(1, _translate("MainWindow", "Description"))
        self.treeWidget.headerItem().setText(2, _translate("MainWindow", "index"))
        self.treeWidget.headerItem().setText(3, _translate("MainWindow", "multirows"))
        self.treeWidget.headerItem().setText(4, _translate("MainWindow", "true_main"))
        self.treeWidget.headerItem().setText(5, _translate("MainWindow", "active"))
        self.report_tab.setTabText(self.report_tab.indexOf(self.Findings), _translate("MainWindow", "Findings"))
        self.Conculsion_Button.setText(_translate("MainWindow", "Conculsion"))
        self.take_Button.setText(_translate("MainWindow", "TakeOut"))
        self.clear_Button.setText(_translate("MainWindow", "Clear"))
        self.menuSeeting.setTitle(_translate("MainWindow", "Seeting"))
        self.menuDictionary.setTitle(_translate("MainWindow", "Dictionary"))
        self.actionEdit_Dictionary.setText(_translate("MainWindow", "Edit Dictionary"))
        self.actionReload_Disctionary.setText(_translate("MainWindow", "Reload Dictionary"))

# -*- coding: utf-8 -*-

import sys
import re
import datetime
import json
import time
import win32clipboard
import win32con
import psutil


from MainWin import Ui_MainWindow
#from checklist import Ui_Form
from selecter import Ui_Select_Dialog
from importDiag import Ui_import_Dialog
from autokeyinForm import Ui_autokeyinForm
from measurement import Ui_Dialog_measurement
from lung_nodule import Ui_Lung_nodule_Dialog
from conclusion_dia import Ui_Conclusion_Dialog
from single_line import Ui_Single_Dialog
from tab_edit import Ui_tabEdit_Dialog
from editor import Ui_Edit_Dialog

from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from os import linesep, getenv, rename, path, listdir, remove, system, popen
from functools import partial


class Iner_database():
    def __init__(self, parent, template_file, tab_file='./setting/tab.json'):
        self.parent = parent
        self.template = {}
        self.tab = {}
        self.category_list = []
        self.template_file = template_file
        self.tab_file = tab_file
        self.current_temple = 'fdg'
        self.curent_version = 1.5
        with open(self.template_file, 'r') as file_json:
            self.template = json.load(file_json)

        while not 'version' in self.template or float(self.template['version']) < self.curent_version:
            self.check_version()

        if not self.template:
            return
        self.init_seeting()
        self.init_tabwidget()
        self.init_treewidget()

        return

    def creat_new(self, file_path, copy=True):

        if not copy:

            new_template = {"version": "1.4",
                            "tab": {"TabName": {"Common": {"active": "True", "checklist": [], "connect": "Common"}},
                                    "List": ["Common"]},
                            "category_list": ["Common"], "category": {"Common": [{"shortcut": "lesion", "main": "V{+nodule|mass|lesion} with V{+mild increased|increased|intense} FDG uptake in the", "active": "True", "description": ""}]},
                            "Seeting": {"Send report by AHK": True, "Adding line number when sending": True, "Spelling check": True}}
        else:

            new_template = self.template

        with open(file_path, 'w') as file_json:
            json.dump(new_template, file_json)

        return

    def check_version(self):
        #print(self.template.keys())
        if not 'version' in self.template:
            temp_template = {}
            default_file = './setting/template/default.json'
            temp_template['version'] = '1.0'
            tab = {}
            temp = {}
            for index in self.template['fdg'].keys():
                if not self.template['fdg'][index]['category'] in list(temp.keys()):
                    temp[self.template['fdg'][index]['category']] = []
                    temp[self.template['fdg'][index]['category']].append({'shortcut': self.template['fdg'][index]['shortcut'], 'main': self.template['fdg'][index]['main'],
                                                         'active': self.template['fdg'][index]['active']})
                else:
                    temp[self.template['fdg'][index]['category']].append(
                        {'shortcut': self.template['fdg'][index]['shortcut'],
                         'main': self.template['fdg'][index]['main'],
                         'active': self.template['fdg'][index]['active']})


            with open(default_file, 'r') as file_json:
                default_json = json.load(file_json)

            tab['List'] = default_json['tab']['List']
            tab['TabName'] = default_json['tab']['TabName']
            for tab_name in tab['List']:
                tab['TabName'][tab_name]['checklist'] = []

            temp_template['tab'] = tab
            temp_template['category_list'] = list(temp.keys())
            temp_template['category'] = temp

            self.template = temp_template
            old_file = self.template_file.replace('.json','_old.json')
            rename(self.template_file, old_file)
            print('save new json')
            with open(self.template_file, 'w') as file_json:
                json.dump(self.template, file_json)

        elif float(self.template['version']) < 1.1:

            for category in self.template['category'].keys():
                for index, element in enumerate(self.template['category'][category]):
                    if not 'description' in self.template['category'][category][index]:
                        self.template['category'][category][index]['description'] = ''

            self.template['version'] = '1.1'
            self.save_json()

        elif float(self.template['version']) < 1.2:

            tab_list = self.template['tab']['List']
            if 'Common' in tab_list:
                tab_list.pop(tab_list.index('Common'))
                self.template['tab']['List'] = tab_list
            if 'Common' in self.template['tab']['TabName'].keys():
                self.template['tab']['TabName'].pop('Common')

            if 'Followup' in self.template['tab']['TabName'].keys():
                self.template['tab']['TabName']['Followup']['active'] = 'True'

            self.template['version'] = '1.2'
            self.save_json()

        elif float(self.template['version']) < 1.3:

            if not 'Seeting' in self.template.keys():
                seeting_member = {'Send report by AHK': True,
                                       'Adding line number when sending': True}
                self.template['Seeting'] = seeting_member
                self.template['version'] = '1.3'
                self.save_json()
            else:
                self.template['version'] = '1.3'
                self.save_json()

        elif float(self.template['version']) < 1.4:

            if not 'Seeting' in self.template.keys():
                seeting_member = {'Send report by AHK': True,
                                  'Adding line number when sending': True,
                                  'Spelling check':'True'}

                self.template['Seeting'] = seeting_member
                self.template['version'] = '1.4'
                self.save_json()
            elif not 'Spelling check' in self.template['Seeting'].keys():
                self.template['Seeting']['Spelling check'] = True
                self.template['version'] = '1.4'
                self.save_json()
            else:
                self.template['version'] = '1.4'
                self.save_json()

        elif float(self.template['version']) < 1.5:

            if not 'Ask checklist' in self.template['Seeting'].keys():
                self.template['Seeting']['Ask checklist'] = True
                self.template['version'] = '1.5'
                self.save_json()
            else:
                self.template['version'] = '1.5'
                self.save_json()

        return

    def init_seeting(self):
        if not 'Seeting' in self.template.keys():
            print('error tempfile without seeting')
            return
        self.parent.ui.menuSeeting.clear()

        for seeting in self.template['Seeting'].keys():
            action_obj = QtWidgets.QAction(seeting, self.parent.ui.menuSeeting)
            action_obj.setCheckable(True)
            if self.template['Seeting'][seeting]:
                action_obj.setChecked(True)
            self.parent.ui.menuSeeting.addAction(action_obj)

        action_obj = QtWidgets.QAction('Save seeting', self.parent.ui.menuSeeting)
        self.parent.ui.menuSeeting.addAction(action_obj)
        action_obj.triggered.connect(self.save_seeting)

        self.parent.ui.menuDictionary.clear()
        action_obj = QtWidgets.QAction('Edit Dictionary', self.parent.ui.menuDictionary)
        self.parent.ui.menuDictionary.addAction(action_obj)
        action_obj.triggered.connect(self.open_dict)

        action_obj = QtWidgets.QAction('Reload Dictionary', self.parent.ui.menuDictionary)
        self.parent.ui.menuDictionary.addAction(action_obj)
        action_obj.triggered.connect(self.parent.init_dictionary)


        return

    def open_dict(self):
        file_path = './setting/autocompwords.txt'
        popen('notepad ' + file_path)

        return

    def init_tabwidget(self):
        self.tabname_list = []
        self.tab_tree_connect = {}
        self.parent.ui.tabWidget.clear()
        tab_list = self.template['tab']['List']
        tab_index = 0
        combo_list = ["Unchecked","Normal","Checked","Abnormal"]
        for tab in tab_list:
            #print('the current', self.template['tab']['TabName'].keys())
            if self.template['tab']['TabName'][tab]['active'] == 'False':
                continue

            name = tab
            self.tabname_list.append(tab)
            if tab in self.template['tab']['TabName']:
                category = self.template['tab']['TabName'][tab]['connect']
            else:
                category = False
            self.parent.ui.tabWidget.tab_Temp = QtWidgets.QWidget()
            self.parent.ui.tabWidget.tab_Temp.setObjectName(tab)
            self.parent.ui.tabWidget.Layout = QtWidgets.QHBoxLayout(self.parent.ui.tabWidget.tab_Temp)
            self.parent.ui.tabWidget.Layout.setObjectName("Layout_" + name)
            self.parent.ui.tabWidget.combo_Temp = QtWidgets.QComboBox(self.parent.ui.tabWidget.tab_Temp)
            self.parent.ui.tabWidget.combo_Temp.setObjectName("combo_" + name)
            self.parent.ui.tabWidget.combo_Temp.addItems(combo_list)
            self.parent.ui.tabWidget.combo_Temp.currentIndexChanged.connect(self.parent.combo_changed)
            self.parent.ui.tabWidget.Layout.addWidget(self.parent.ui.tabWidget.combo_Temp)
            self.parent.ui.tabWidget.Temp_checked = QtWidgets.QPushButton(self.parent.ui.tabWidget.tab_Temp)
            self.parent.ui.tabWidget.Temp_checked.setObjectName("checked_" + name)
            self.parent.ui.tabWidget.Temp_checked.setText("Checked to next  -->")
            self.parent.ui.tabWidget.Temp_checked.clicked.connect(self.parent.checked_to_next)

            self.parent.ui.tabWidget.Layout.addWidget(self.parent.ui.tabWidget.Temp_checked)
            self.parent.ui.tabWidget.addTab(self.parent.ui.tabWidget.tab_Temp, name)
            self.tab_tree_connect[tab_index] = category
            tab_index = tab_index + 1
        self.parent.ui.tabWidget.setCurrentIndex(0)
        return

    def init_treewidget(self):
        count = self.parent.ui.treeWidget.topLevelItemCount()
        tree_statue = {}
        if count:
            for i in range(count):
                tree_statue[i] = self.parent.ui.treeWidget.topLevelItem(i).isExpanded()

        self.parent.ui.treeWidget.clear()

        if type(self.template['category_list']) is list:
            self.category_list = self.template['category_list']
        else:
            print('no category list found')
            return False

        #print(self.template['category'].keys())

        for category in self.category_list:
            category_root = QtWidgets.QTreeWidgetItem(self.parent.ui.treeWidget)
            category_root.setText(0, category)
            #print(category)
            for index, element in enumerate(self.template['category'][category]):
                child = QtWidgets.QTreeWidgetItem(category_root)
                child.setText(0, element['shortcut'])
                #change color if is not active
                #if element['active'] == 'True':
                #    child.setForeground(0, QtGui.QColor("black"))
                #else:
                #    child.setForeground(0, QtGui.QColor("blue"))

                main_text, isMultrow = self.check_if_multirow(element['main'])
                if not 'description' in element or not element['description']:
                    child.setText(1, main_text)
                else:
                    child.setText(1, element['description'])
                child.setText(2, str(index))
                child.setText(3, isMultrow)
                child.setText(4, element['main'])


        if tree_statue:
            for i in tree_statue.keys():
                if i < self.parent.ui.treeWidget.topLevelItemCount() and tree_statue[i]:
                    self.parent.ui.treeWidget.topLevelItem(i).setExpanded(True)
        else:
            self.settab()
        return

    def save_seeting(self):

        for obj in self.parent.ui.menuSeeting.findChildren(QtWidgets.QAction):
            if obj.isCheckable():
                self.template['Seeting'][obj.text()] = obj.isChecked()
                if obj.text() == 'Spelling check':
                    print(obj.isChecked())
                    self.parent.textSpellingCheck.set_active(obj.isChecked())

        self.save_json()

        return

    def check_seeting(self, keyword):
        find_seeting = False

        for obj in self.parent.ui.menuSeeting.findChildren(QtWidgets.QAction):
            if obj.text() == keyword:
                find_seeting = True
                return obj.isChecked()

        return -1

    def connect_by_tab(self, tab_name):
        category = self.template['tab']['TabName'][tab_name]['connect']
        return category

    def change_template(self, template_file):
        self.template_file = template_file
        with open(self.template_file, 'r') as file_json:
            self.template = json.load(file_json)
        self.check_version()

        self.init_seeting()
        self.init_treewidget()
        self.init_tabwidget()

        return

    def check_if_multirow(self, text):
        temp = text.strip().splitlines()
        text = temp[0]
        if len(temp) > 1:
            return text, 'True'
        else:
            return text, 'False'

    def settab(self):
        index = self.parent.ui.tabWidget.currentIndex()
        if not index in self.tab_tree_connect:
            return
        if not self.tab_tree_connect[index]:
            return
        self.parent.ui.treeWidget.collapseAll()
        for obj in self.parent.ui.treeWidget.findItems('Common',QtCore.Qt.MatchExactly|QtCore.Qt.MatchRecursive,0):
            obj.setExpanded(True)
        for obj in self.parent.ui.treeWidget.findItems(self.tab_tree_connect[index],QtCore.Qt.MatchExactly|QtCore.Qt.MatchRecursive,0):
            if obj:
                obj.setExpanded(True)
            self.parent.ui.treeWidget.scrollToItem(obj, QtWidgets.QAbstractItemView.PositionAtTop)

        return

    def import_template(self, results):

        for result in results:
            category = result.pop('category')
            index = len(self.template['category'][category])
            self.template['category'][category].append(result)

        self.init_treewidget()
        self.save_json()

    def get_all_shortcut(self):
        shortcuts = []
        for category in self.template['category']:
            for element in self.template['category'][category]:
                shortcut = element['shortcut']
                if shortcut and not shortcut in shortcuts:
                    shortcuts.append(shortcut)

        return shortcuts

    def rename_category(self, category, new_name):
        if not category in self.template['category']:
            print('the category is not exist')
            return False

        self.template['category'][new_name] = self.template['category'].pop(category)
        self.template['category_list'][self.template['category_list'].index(category)] = new_name
        for key in self.tab_tree_connect.keys():
            if self.tab_tree_connect[key] == category:
                self.tab_tree_connect[key] = new_name

        self.save_json()
        self.init_treewidget()

        return

    def add_category(self, category, new_name):
        if new_name in self.category_list:
            return

        self.template['category_list'].insert(self.template['category_list'].index(category) + 1, new_name)
        self.template['category'][new_name] =  []
        self.save_json()
        self.init_treewidget()


        return

    def del_category(self, category):
        if not category in self.template['category_list'] or category == 'Common':
            return

        del self.template['category_list'][self.template['category_list'].index(category)]
        del self.template['category'][category]
        self.save_json()
        self.init_treewidget()

        return

    def edit_by_index(self, index, result):
        factors = ["category", "shortcut", "main", "active"]
        index = int(index)
        for factor in factors:
            if not factor in result or not result['category'] in self.template['category']:
                print('error in return data')
                return False

        if index < len(self.template['category'][result['category']]):
            category = result.pop('category')
            self.template['category'][category][index] = result
            self.save_json()
        else:
            print('no such index')
            return False
        return True

    def insert_by_index(self, index, result):
        factors = ["category", "shortcut", "main", "active"]
        index = int(index)
        for factor in factors:
            if not factor in result:
                print('error in return data')
                return False
        category = result.pop('category')
        self.template['category'][category].insert(index, result)
        self.init_treewidget()
        self.save_json()

        return True

    def del_by_index(self, category, index):
        index = int(index)
        if index < len(self.template['category'][category]):
            del self.template['category'][category][index]

            self.init_treewidget()
            self.save_json()

        return

    def edit_tab(self, current_tab, result):
        combo_list = ["Unchecked","Normal","Checked","Abnormal"]
        tab_list = self.template['tab']['List']
        current_index = tab_list.index(current_tab)
        #print(current_index)
        #print(tab_list)
        #print(current_tab)
        if current_tab != result['name']:
            tab_list[int(current_index)] = result['name']
            self.template['tab']['List'] = tab_list
            self.template['tab']['TabName'][result['name']] = self.template['tab']['TabName'].pop(current_tab)
            #print('change to ',tab_list)
            #print('change to', self.template['tab']['TabName'].keys())

        if current_index != result['new_index']:
            tab_list.insert(int(result['new_index']) - 1, tab_list.pop(int(current_index)))
            self.template['tab']['List'] = tab_list
            #print(tab_list)

        self.template['tab']['TabName'][result['name']]['connect'] = result['connect']
        self.template['tab']['TabName'][result['name']]['active'] = result['active']

        self.save_json()
        self.init_tabwidget()

        return

    def add_tab(self, result):
        tab_list = self.template['tab']['List']
        checks = ['new_index','name','connect','active']
        for check in checks:
            if not check in result:
                return

        temp = {}
        if result['name'] in tab_list:
            return

        temp = {'active':result['active'],
                'checklist':[],
                'connect':result['connect']}

        tab_list.insert(int(result['new_index']), result['name'])
        self.template['tab']['List'] = tab_list
        self.template['tab']['TabName'][result['name']] = temp

        self.save_json()
        self.init_tabwidget()

        return

    def del_tab(self, tab_name):
        tab_list = self.template['tab']['List']
        if tab_name in tab_list:
            tab_list.remove(tab_name)
            self.template['tab']['List'] = tab_list

        if tab_name in self.template['tab']['TabName'].keys():
            del self.template['tab']['TabName'][tab_name]

        self.save_json()
        self.init_tabwidget()

        return


    def save_json(self):
        with open(self.template_file, 'w') as file_json:
            json.dump(self.template, file_json)

        return

    def main_by_index(self, category, index):
        return self.template['category'][category]['main']

class MyTabEdit(QtWidgets.QDialog):
    def __init__(self, parent, category_list, tab_count, index=-1, tab_name='', category='', active=True):
        QtWidgets.QDialog.__init__(self, parent)
        self.tabedit_diag = Ui_tabEdit_Dialog()
        self.tabedit_diag.setupUi(self)
        self.changed = False

        self.tabedit_diag.category_comboBox.addItems(category_list)
        if category:
            #print(self.tabedit_diag.category_comboBox.findText(category, QtCore.Qt.MatchExactly))
            self.tabedit_diag.category_comboBox.setCurrentIndex(self.tabedit_diag.category_comboBox.findText(category,QtCore.Qt.MatchExactly))
        if tab_name:
            self.tabedit_diag.nameEdit.setText(tab_name)

        for i in range(tab_count):
            self.tabedit_diag.index_comboBox.addItem(str(i+1))

        if not index == -1 and index < tab_count:
            self.tabedit_diag.index_comboBox.setCurrentIndex(int(index))

        if active:
            self.tabedit_diag.checkBox.setChecked(True)

    def get_date(self):
        result = {}
        result['new_index'] = self.tabedit_diag.index_comboBox.currentText()
        result['name'] = self.tabedit_diag.nameEdit.text()
        result['connect'] = self.tabedit_diag.category_comboBox.currentText()
        result['active'] = str(self.tabedit_diag.checkBox.isChecked())

        return result


class Myimport(QtWidgets.QDialog):
    def __init__(self, parent, sents, category_list=[]):
        QtWidgets.QDialog.__init__(self, parent)
        self.importdiag = Ui_import_Dialog()
        self.importdiag.setupUi(self)
        self.importdiag.tableWidget.horizontalHeader().setFixedHeight(30)
        #self.importdiag.tableWidget.horizontalHeader().setFixedWidth(0, 30)
        self.importdiag.tableWidget.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

        row = 0
        self.importdiag.tableWidget.setRowCount(len(sents))

        for sent in sents:
            checkbox = QtWidgets.QCheckBox()
            #print(sent)
            check_item = QtWidgets.QTableWidgetItem()
            check_item.setFlags(QtCore.Qt.ItemIsUserCheckable |
                          QtCore.Qt.ItemIsEnabled)
            check_item.setCheckState(QtCore.Qt.Checked)

            combo = QtWidgets.QComboBox()
            combo.addItems(category_list)

            template_item = QtWidgets.QTableWidgetItem(sent)
            self.importdiag.tableWidget.setItem(row, 0, check_item)
            self.importdiag.tableWidget.setItem(row, 1, template_item)
            self.importdiag.tableWidget.setCellWidget(row, 3, combo)

            row += 1

        return

    def get_date(self):
        total_row = self.importdiag.tableWidget.rowCount()

        results = []
        for index in range(total_row):
            if self.importdiag.tableWidget.item(index, 0).checkState() == QtCore.Qt.Checked:
                category = self.importdiag.tableWidget.cellWidget(index, 3).currentText().strip()
                if self.importdiag.tableWidget.item(index, 2):
                    shortcut = self.importdiag.tableWidget.item(index, 2).text().strip()
                else:
                    shortcut = ''
                description = ''
                if self.importdiag.tableWidget.item(index, 1):
                    main = self.importdiag.tableWidget.item(index, 1).text().strip()
                else:
                    continue
                active = 'True'

                results.append({'category':category,
                                'shortcut':shortcut,
                                'description':description,
                                'main':main,
                                'active':active})

        return results




class Mysimple_noted(QtWidgets.QDialog):
#class Mysimple_noted(QtWidgets.QMainWindow):
    update = QtCore.pyqtSignal()

    def __init__(self, parent, note='', default_dic=[]):
        QtWidgets.QDialog.__init__(self, parent)
        self.mynote = QtWidgets.QDialog()
        #self.mynote = Ui_simple_note_Dialog()
        self.setObjectName("simple_note_Dialog")
        self.setWindowTitle('')
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(12)
        self.resize(600, 600)

        self.mynote.centralwidget = QtWidgets.QVBoxLayout(self)
        self.mynote.centralwidget.setObjectName("centralwidget")
        self.mynote.note_tab = QtWidgets.QTabWidget(self)
        self.mynote.note_tab.setObjectName("note_tab")
        self.mynote.centralwidget.addWidget(self.mynote.note_tab)
        self.mynote.textEdit = QtWidgets.QTextEdit(self)
        self.mynote.textEdit.setObjectName("textEdit")
        self.mynote.textEdit.setFont(font)
        self.select_hightlight = SelectHighlighter(self.mynote.textEdit)
        self.mynote.note_tab.addTab(self.mynote.textEdit,'MyNote')


        #self.mynote.setWindowFlags(self.mynote.windowFlags() & ~QtCore.Qt.WindowStaysOnTopHint)

        if note:
            self.mynote.textEdit.setPlainText(note)

        return

    def closeEvent(self, event):
        self.update.emit()

        super(Mysimple_noted, self).closeEvent(event)
        return

    def selection(self, keyword):
        self.select_hightlight.selected_word(keyword)
        return

class Myconclusion(QtWidgets.QDialog):
    def __init__(self, parent, text=''):
        QtWidgets.QDialog.__init__(self, parent)
        self.conclusion = Ui_Conclusion_Dialog()
        self.conclusion.setupUi(self)
        self.conclusion.tableWidget.setWordWrap(True)

        each_lines = text.splitlines()
        self.conclusion.tableWidget.setHorizontalHeaderLabels(['Finding', 'Selection', 'Conclusion'])
        self.conclusion.tableWidget.setRowCount(len(each_lines))

        for i in range(len(each_lines)):
            #print(i)
            newItem = QtWidgets.QTableWidgetItem()
            newItem.setText(each_lines[i])
            self.conclusion.tableWidget.setItem(i, 0, newItem)

class NumberBar(QtWidgets.QWidget):

    def __init__(self, *args):
        QtWidgets.QWidget.__init__(self, *args)
        self.edit = None
        # This is used to update the width of the control.
        # It is the highest line that is currently visibile.
        self.highest_line = 0

    def setTextEdit(self, edit):
        self.edit = edit

    def update(self, *args):
        '''
        Updates the number bar to display the current set of numbers.
        Also, adjusts the width of the number bar if necessary.
        '''
        # The + 4 is used to compensate for the current line being bold.
        width = self.fontMetrics().width(str(self.highest_line)) + 4
        if self.width() != width:
            self.setFixedWidth(width)
        QtWidgets.QWidget.update(self, *args)

    def paintEvent(self, event):
        result = []
        contents_y = self.edit.verticalScrollBar().value()
        page_bottom = contents_y + self.edit.viewport().height()
        font_metrics = self.fontMetrics()
        current_block = self.edit.document().findBlock(self.edit.textCursor().position())
        pattern = re.compile('.\.$')
        result = pattern.findall(current_block.text())

        painter = QtGui.QPainter(self)

        line_count = 0
        # Iterate over all text blocks in the document.
        block = self.edit.document().begin()

        while block.isValid():
            line_count += 1

            # The top left position of the block in the document
            position = self.edit.document().documentLayout().blockBoundingRect(block).topLeft()

            # Check if the position of the block is out side of the visible
            # area.
            #if position.y():
            #    break
            #if result:
            #    font = painter.font()
            #    font.setItalic(True)
            #    painter.setFont(font)
            #else:
            #    font = painter.font()
            #    font.setItalic(False)
            #    painter.setFont(font)

            # We want the line number for the selected line to be bold.
            bold = False
            if block == current_block:
                bold = True
                font = painter.font()
                font.setBold(True)
                painter.setFont(font)

            # Draw the line number right justified at the y position of the
            # line. 3 is a magic padding number. drawText(x, y, text).

            painter.drawText(self.width() - font_metrics.width(str(line_count)) - 3,
                             round(position.y()) - contents_y + font_metrics.ascent(), str(line_count))

            # Remove the bold style if it was set previously.
            if bold:
                font = painter.font()
                font.setBold(False)
                painter.setFont(font)

            block = block.next()

        self.highest_line = line_count
        painter.end()

        QtWidgets.QWidget.paintEvent(self, event)


class EditHighlighter(QtGui.QSyntaxHighlighter):

    def __init__(self, parent):
        QtGui.QSyntaxHighlighter.__init__(self, parent)
        self.parent = parent
        self.highlightingRules = []

        return

    def highlightBlock(self, text):

        Block = '\S{1,2}\{.*?\}'
        inBlock = '\[.*?\]'
        seper = '\|+'

        keyword = Qt.QTextCharFormat()
        keyword.setBackground(QtGui.QColor(255, 255, 0))
        inkeyword = Qt.QTextCharFormat()
        inkeyword.setBackground(QtGui.QColor(0, 255, 0))
        sepcolor = Qt.QTextCharFormat()
        sepcolor.setForeground(QtGui.QColor(255, 0, 0))
        sepcolor.setBackground(QtGui.QColor(255, 255, 0))

        if text:
            for word_object in re.finditer(Block, text):
                test_word = word_object.group()
                if len(test_word) > 2:
                    self.setFormat(word_object.start(), word_object.end() - word_object.start(), keyword)

            for word_object in re.finditer(seper, text):
                self.setFormat(word_object.start(), word_object.end() - word_object.start(), sepcolor)

            for word_object in re.finditer(inBlock, text):
                self.setFormat(word_object.start(), word_object.end() - word_object.start(), inkeyword)


        return


class MySinpleditor(QtWidgets.QDialog):
    def __init__(self, parent, category, category_list=[]):
        QtWidgets.QDialog.__init__(self, parent)
        self.simpleditor = Ui_Single_Dialog()
        self.simpleditor.setupUi(self)
        self.category_list = category_list

        self.simpleditor.lineEdit.setText(category)

        return

    def get_date(self):

        return self.simpleditor.lineEdit.text()


    def accept(self):
        if self.simpleditor.lineEdit.text() in self.category_list:
            QtWidgets.QMessageBox.warning(self, 'Warning', 'Category is already exist!!', QtWidgets.QMessageBox.Ok)
            return
        else:
            QtWidgets.QDialog.accept(self)

        return

class Myeditor(QtWidgets.QDialog):
    def __init__(self, parent, item, list, shortcut_values, mode='e'):
        QtWidgets.QDialog.__init__(self, parent)
        self.editor = Ui_Edit_Dialog()
        self.editor.setupUi(self)
        self.check_shortcut = []


        if item:
            if mode == 'e':
                sent = item.text(4)
                category = item.parent().text(0)
                if item.text(0):
                    shortcut_values.remove(item.text(0))
                self.check_shortcut = shortcut_values + list
                self.editor.category_Box.addItem(category)
                self.editor.shortcut_Edit.setText(item.text(0))
                self.editor.description_Edit.setText(item.text(1))
                self.editor.tamplate_TextEdit.setPlainText(sent)
            elif mode == 'a':
                if not item.parent():
                    category = item.text(0)
                    index = 0
                else:
                    category = item.parent().text(0)
                    index = int(item.text(2)) + 1

                self.check_shortcut = shortcut_values + list
                self.editor.category_Box.addItem(category)

        self.editor.check_active.setChecked(True)
        self.editor.tamplate_TextEdit.modificationChanged.connect(self.textChanger)
        self.editor.shortcut_Edit.textChanged.connect(self.textChanger)
        self.editor.description_Edit.textChanged.connect(self.textChanger)
        KeyHighliter = EditHighlighter(self.editor.tamplate_TextEdit.document())
        self.editor.textChanged = False

        return

    def textChanger(self):
        self.editor.textChanged = True
        return

    def get_date(self):
        if not self.editor.textChanged:
            return False
        result = {}
        result['category'] = self.editor.category_Box.currentText()
        result['shortcut'] = self.editor.shortcut_Edit.text()
        result['main'] = self.editor.tamplate_TextEdit.toPlainText()
        result['description'] = self.editor.description_Edit.text()
        if self.editor.check_active.isChecked():
            result['active'] = True
        else:
            result['active'] = False

        return result

    def accept(self):
        shortcut = self.editor.shortcut_Edit.text()
        if not self.editor.tamplate_TextEdit.toPlainText():
            QtWidgets.QMessageBox.warning(self, 'Warning', 'The template is empty!!', QtWidgets.QMessageBox.Ok)
            return
        elif shortcut and shortcut in self.check_shortcut:
            quit_msg = "The same shortcut is already exist. Are you sure to keep it?"
            reply = QtWidgets.QMessageBox.question(self, 'Message',
                                                   quit_msg, QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)

            if reply == QtWidgets.QMessageBox.Yes:
                QtWidgets.QDialog.accept(self)
            else:
                return
            return
#        elif not self.editor.shortcut_Edit.text():
#            QtWidgets.QMessageBox.warning(self, 'Warning', 'The shortcut is empty!!', QtWidgets.QMessageBox.Ok)
#            return
        else:
            QtWidgets.QDialog.accept(self)

        return

class MyMeasure(QtWidgets.QDialog):
    #date = QtCore.pyqtSignal(str)
    def __init__(self, parent):
        QtWidgets.QDialog.__init__(self, parent)
        self.measure = Ui_Dialog_measurement()
        self.measure.setupUi(self)
        self.measure.Simple_size_x.setFocus()
        self.measure.Simple_position_IMA.setKeyboardTracking(False)
        self.measure.Simple_position_IMA.valueChanged.connect(self.accept)
        self.measure.Simple_position_image.setKeyboardTracking(False)
        self.measure.Simple_position_image.valueChanged.connect(self.accept)

        return

    def keyPressEvent(self, event):
        if event.key() in (QtCore.Qt.Key_Return,QtCore.Qt.Key_Enter):
            if 'Simple_position_image' in self.focusWidget().objectName():
                self.accept()
            self.focusNextChild()

        else:
            QtWidgets.QDialog.keyPressEvent(self, event)

        return

    def get_data(self):
        size_list = {}
        output_list =[]
        size_cross_sign = self.measure.cross_sign.currentText()
        unit = self.measure.unit.currentText()
        tracer_uptake = []
        position = []

        for spinBox in self.measure.tabWidget.currentWidget().findChildren(QtWidgets.QDoubleSpinBox):
            if spinBox.value() > 0:
                if 'size' in spinBox.objectName():
                    size_list[spinBox.objectName()] = str(spinBox.value())
                if 'uptake' in spinBox.objectName():
                    name = spinBox.objectName().split('_')[2]
                    tracer_uptake.append(name + ':' + str(spinBox.value()))
                if 'position' in spinBox.objectName():
                    name = spinBox.objectName().split('_')[2]
                    position.append(name + ':' + str(int(spinBox.value())))
        if size_list:
            size_temp = []
            list_of_size = list(size_list.keys())
            list_of_size.sort()
            if len(size_list) > 1:
                for key in list_of_size:
                    size_temp.append(size_list[key])
                output_list.append('size:' + size_cross_sign.join(size_temp) + unit)
            else:
                output_list.append(size_list[list_of_size[0]] + unit)
        if tracer_uptake:
            output_list = output_list + tracer_uptake
        if position:
            output_list = output_list + position

        return ', '.join(output_list)

class MycLabel(QtWidgets.QLabel):
    click_signal = QtCore.pyqtSignal(object)
    def __init__(self, parent=None):
        super(MycLabel, self).__init__(parent)

    def mousePressEvent(self, e):
        self.click_signal.emit(e)
        return

class MyComboBox(QtWidgets.QComboBox):
    def __init__(self, parent=None):
        super(MyComboBox, self).__init__(parent)

    def text(self):
        return self.itemText(self.currentIndex())


class MySelecter(QtWidgets.QDialog):

    #date = QtCore.pyqtSignal(str)
    def __init__(self, parent, edit_sent):
        QtWidgets.QDialog.__init__(self, parent)
        self.select = Ui_Select_Dialog()
        self.select.setupUi(self)
        self.select.match_sections = []
        self.select.object = []
        self.select.in_title_object = []
        self.select.return_sent = edit_sent
        self.default_layout = 'V'
        self.select.scrollArea.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.select.scrollArea.customContextMenuRequested.connect(self.__contextMenu)
        self.screen_width = screen_resolution.width()
        self.screen_height = screen_resolution.height()
        self.setMaximumWidth(self.screen_width)
        self.setMaximumHeight(self.screen_height)
        self.max_sent_length = 0

        #print(screen_resolution.width())
        has_in_selection = ['V','M','m','C','c']

        pattern = re.compile('G\d{.+?}|M.?{.+?}|m.?{.+?}|H{.+?}|h{.+?}|V{.+?}|v{.+?}|C{.+?}|c{.+?}')
        G_pattern = re.compile('G\d')
        in_selection_pattern = re.compile('M\[.*?\]|H\[.*?\]|LE\d*\[.*?\]')
        in_title_pattern = re.compile('C\d*\[.*?\]|L\d*\[.*?\]')
        H_pattern = re.compile('M\[.*?\]|H\[.*?\]')
        Hr_pattern = re.compile('Block\[\d+\]')
        self.select.match = pattern.findall(edit_sent)

        title_i = 0
        Layout_i = 0

        self.font = QtGui.QFont()
        self.font.setFamily("Consolas")
        self.font.setPointSize(14)

        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(14)

        if not self.select.match:
            blocks = edit_sent.splitlines()
            for sents in blocks:
                if in_title_pattern.search(sents):
                    toki_sents = self.split_into_sentences(sents)
                    for sent in toki_sents:
                        in_title_result = in_title_pattern.findall(sent)
                        if in_title_result:
                            title_i, Layout_i = self.deal_with_in_title_obj(sent, Layout_i, title_i, in_title_result)
                        else:
                            obj_name = "label_" + str(title_i)
                            self.add_free_lable(sent,
                                              self.select.verticalLayout_2,
                                              obj_name,
                                              self.font)
                            title_i += 1

                else:
                    obj_name = "label_" + str(title_i)
                    self.add_free_lable(sents,
                                           self.select.verticalLayout_2,
                                           obj_name,
                                           self.font)
                    title_i += 1

            obj_name = "label_End"
            self.add_free_lable(" ", self.select.verticalLayout_2, obj_name, self.font)
            self.adjustDialog()
            return

        Hr_result = ''
        in_selection_result = ''
        in_title_result = []
        preH_result = ''
        H_result = ''

        button_i = 0
        title_temp = ''
        selections = []
        in_selection_separator = ''
        c_count = 0
        g_layout_x = 0
        g_layout_y = 0

        for match_section in self.select.match:
            obj_temp = []
            H_temp = {}
            #print(match_section)
            select_layout = self.default_layout
            match_section = match_section.strip()
            if not title_temp:
                title_temp = edit_sent
            sent_title = title_temp.split(match_section,1)[0]
            title_temp = title_temp.split(match_section,1)[1]

            if not '{' in match_section or not '}' in match_section:
                continue

            # put H block into temp region for prevent from separation
            preH_result = H_pattern.findall(match_section)
            if preH_result:
                i = 0
                for H_block in preH_result:
                    key = 'Block' + '[{}]'.format(str(i))
                    match_section = re.sub(self.keywordlize(H_block), key, match_section, 1)
                    H_temp[str(i)] = H_block
                    i += 1

            selections = []
            if '{' in match_section and '}' in match_section:
                if '|' in match_section:
                    selections = match_section.split('{')[1].replace('}', '').split('|')
                #elif ';' in match_section:
                #    selections = match_section.split('{')[1].replace('}', '').split(';')
                else:
                    selections.append(match_section.split('{')[1].replace('}', ''))
            match_head = match_section.split('{')[0]
            select_layout = match_head[0]
            if len(match_head) > 1 and select_layout == 'M':
                in_selection_separator = match_head[-1]
            g_layout = G_pattern.match(match_head)
            if g_layout:
                c_count = int(match_head[1:])
                g_layout_x = 0
                g_layout_y = 0

            # deal with the title
            if not sent_title and Layout_i == 0:
                obj_name = "label_first"
                self.add_free_lable(" ",
                                    self.select.verticalLayout_2,
                                    obj_name,
                                    self.font)

            block = sent_title.splitlines()
            for sents in block:
                if in_title_pattern.search(sents):
                    toki_sents = self.split_into_sentences(sents)
                    for sent in toki_sents:
                        in_title_result = in_title_pattern.findall(sent)
                        if in_title_result:
                            title_i, Layout_i = self.deal_with_in_title_obj(sent, Layout_i, title_i, in_title_result)
                        else:
                            obj_name = "label_" + str(title_i)
                            self.add_free_lable(sent,
                                              self.select.verticalLayout_2,
                                              obj_name,
                                              self.font)
                            title_i += 1
                else:
                    obj_name = "label_" + str(title_i)
                    self.add_free_lable(sents,
                                           self.select.verticalLayout_2,
                                           obj_name,
                                           self.font)
                    title_i += 1

            # add layout for choices
            if select_layout == 'H':
                self.select.Layout_Temp = QtWidgets.QHBoxLayout()
            elif select_layout in has_in_selection:
                self.select.Layout_Temp = QtWidgets.QVBoxLayout()
            elif g_layout:
                self.select.Layout_Temp = QtWidgets.QGridLayout()
            else:
                self.select.Layout_Temp = QtWidgets.QHBoxLayout()

            # creating a buttonGroup
            self.select.Layout_Temp.setObjectName("Layout_" + str(Layout_i))
            self.select.verticalLayout_2.addLayout(self.select.Layout_Temp)
            self.select.buttonGroup = QtWidgets.QButtonGroup(self.select.Layout_Temp)

            #print(selections)
            for selection in selections:
                #print(selection)
                is_default = False
                if '+' in selection:
                    is_default = True

                font = QtGui.QFont()
                font.setFamily("Consolas")
                font.setPointSize(14)

                Hr_result = Hr_pattern.findall(selection)
                if Hr_result:
                    for term in Hr_result:
                        i = term.split('[',1)[1].split(']',1)[0]
                        selection = re.sub(self.keywordlize(term), H_temp[i], selection)

                if select_layout in has_in_selection:
                    in_selection_result = in_selection_pattern.findall(selection)
                    #print(in_selection_result)
                    if in_selection_result:
                        self.select.in_selection_Layout_Temp = QtWidgets.QHBoxLayout()
                        self.select.in_selection_Layout_Temp.setObjectName("in_selection_Layout_" + str(Layout_i))
                        self.select.Layout_Temp.addLayout(self.select.in_selection_Layout_Temp)

                # add button and grouped for each selection
                if select_layout == 'M' or select_layout == 'm':
                    if not in_selection_result:
                        self.select.Button_Temp = QtWidgets.QCheckBox(self.select.scrollAreaWidgetContents)
                        self.select.Button_Temp.setObjectName("Button_" + 'M' + str(Layout_i) + '_' + str(button_i))
                        self.select.buttonGroup.setExclusive(False)
                        self.select.Button_Temp.setFont(font)
                        self.select.Button_Temp.setText(selection.strip().replace('+', ''))
                        self.select.buttonGroup.addButton(self.select.Button_Temp)
                        if is_default:
                            self.select.Button_Temp.setChecked(True)
                    else:
                        self.select.Button_Temp = QtWidgets.QCheckBox(self.select.scrollAreaWidgetContents)
                        self.select.Button_Temp.setObjectName("in_Button_" + 'M' + str(Layout_i) + '_' + str(button_i))
                        self.select.buttonGroup.setExclusive(False)
                        self.select.Button_Temp.setFont(font)
                        self.select.Button_Temp.setText('')
                        self.select.Button_Temp.setMaximumWidth(20)
                        self.select.buttonGroup.addButton(self.select.Button_Temp)
                        if is_default:
                            self.select.Button_Temp.setChecked(True)

                elif g_layout:
                    if not selection.strip() == 'blank':
                        self.select.Button_Temp = QtWidgets.QCheckBox(self.select.scrollAreaWidgetContents)
                        self.select.Button_Temp.setObjectName("Button_" + 'G' + str(Layout_i) + '_' + str(button_i))
                        self.select.buttonGroup.setExclusive(False)
                        self.select.Button_Temp.setText(selection.strip().replace('+',''))
                        self.select.buttonGroup.addButton(self.select.Button_Temp)
                    else:
                        self.select.Button_Temp = QtWidgets.QLabel(self.select.scrollAreaWidgetContents)
                        self.select.Button_Temp.setObjectName("Button_" + 'Blank' + str(Layout_i))
                        self.select.Button_Temp.setText('')

                elif select_layout == 'V' or select_layout == 'v':
                    if not in_selection_result:
                        self.select.Button_Temp = QtWidgets.QRadioButton(self.select.scrollAreaWidgetContents)
                        self.select.Button_Temp.setObjectName("Button_" + 'M' + str(Layout_i) + '_' + str(button_i))
                        #self.select.buttonGroup.setExclusive(False)
                        self.select.Button_Temp.setFont(font)
                        self.select.Button_Temp.setText(selection.strip().replace('+', ''))
                        self.select.buttonGroup.addButton(self.select.Button_Temp)
                        if is_default:
                            self.select.Button_Temp.setChecked(True)
                    else:
                        self.select.Button_Temp = QtWidgets.QRadioButton(self.select.scrollAreaWidgetContents)
                        self.select.Button_Temp.setObjectName("in_Button_" + 'M' + str(Layout_i) + '_' + str(button_i))
                        #self.select.buttonGroup.setExclusive(False)
                        self.select.Button_Temp.setFont(font)
                        self.select.Button_Temp.setText('')
                        self.select.Button_Temp.setMaximumWidth(20)
                        self.select.buttonGroup.addButton(self.select.Button_Temp)
                        if is_default:
                            self.select.Button_Temp.setChecked(True)

                elif select_layout == 'C' or select_layout == 'c':
                    if not in_selection_result:
                        self.select.Button_Temp = QtWidgets.QCheckBox(self.select.scrollAreaWidgetContents)
                        self.select.Button_Temp.setObjectName("Button_" + 'M' + str(Layout_i) + '_' + str(button_i))
                        self.select.buttonGroup.setExclusive(False)
                        self.select.Button_Temp.setFont(font)
                        self.select.Button_Temp.setText(selection.strip().replace('+', ''))
                        self.select.buttonGroup.addButton(self.select.Button_Temp)
                        if is_default:
                            self.select.Button_Temp.setChecked(True)
                    else:
                        self.select.Button_Temp = QtWidgets.QCheckBox(self.select.scrollAreaWidgetContents)
                        self.select.Button_Temp.setObjectName("in_Button_" + 'M' + str(Layout_i) + '_' + str(button_i))
                        self.select.buttonGroup.setExclusive(False)
                        self.select.Button_Temp.setFont(font)
                        self.select.Button_Temp.setText('')
                        self.select.Button_Temp.setMaximumWidth(20)
                        self.select.buttonGroup.addButton(self.select.Button_Temp)
                        if is_default:
                            self.select.Button_Temp.setChecked(True)

                else:
                    self.select.Button_Temp = QtWidgets.QRadioButton(self.select.scrollAreaWidgetContents)
                    self.select.Button_Temp.setObjectName("Button_" + str(Layout_i) + '_' + str(button_i))
                    self.select.Button_Temp.setFont(font)
                    self.select.Button_Temp.setText(selection.strip().replace('+',''))
                    self.select.buttonGroup.addButton(self.select.Button_Temp)
                    if is_default:
                        self.select.Button_Temp.setChecked(True)
                if Layout_i == 0:
                    self.select.Button_Temp.setFocus()

                # add object in each layout
                if select_layout == 'H':
                    for Layout in self.select.scrollArea.findChildren(QtWidgets.QHBoxLayout,'Layout_' + str(Layout_i)):
                        Layout.addWidget(self.select.Button_Temp)
                elif g_layout:
                    for Layout in self.select.scrollArea.findChildren(QtWidgets.QGridLayout, 'Layout_' + str(Layout_i)):
                        if g_layout_x < c_count:
                            Layout.addWidget(self.select.Button_Temp, g_layout_y, g_layout_x, 1, 1)
                            g_layout_x += 1
                        else:
                            g_layout_y += 1
                            g_layout_x = 0
                            Layout.addWidget(self.select.Button_Temp, g_layout_y, g_layout_x, 1, 1)
                            g_layout_x += 1
                elif in_selection_result:
                    in_selection_i = 1
                    temp = ''
                    temp = selection
                    self.select.in_selection_Layout_Temp.addWidget(self.select.Button_Temp)
                    for in_selection_block in in_selection_result:
                        lable_text = temp.split(in_selection_block, 1)[0]
                        temp = temp.split(in_selection_block, 1)[1]
                        in_selection_select_layout =  in_selection_block.split('[',1)[0]
                        if lable_text:
                            self.select.Lable_Temp = MycLabel(self.select.scrollAreaWidgetContents)
                            self.select.Lable_Temp.setObjectName("in_selection_Lable_" + str(Layout_i) + '_' + str(button_i)
                                                                 + '_' + str(in_selection_i))
                            self.select.Lable_Temp.setMaximumSize(QtCore.QSize(self.metrics_optimize(font, lable_text,min=0)))
                            self.select.Lable_Temp.setText(lable_text)
                            self.select.Lable_Temp.click_signal.connect(self.lable_click)
                            self.select.in_selection_Layout_Temp.addWidget(self.select.Lable_Temp)
                            in_selection_i += 1

                        if in_selection_select_layout == 'LE':
                            self.select.in_selection_Temp = QtWidgets.QLineEdit(self.select.scrollAreaWidgetContents)
                            self.select.in_selection_Temp.textChanged.connect(self.autoselect)
                            self.select.in_selection_Temp.setObjectName('LE_' + str(Layout_i) + '_' + str(button_i) + '_' + str(in_selection_i))
                            self.select.in_selection_Temp.setMaximumWidth(40)
                            self.select.in_selection_Temp.setText(in_selection_block.replace('LE[','').replace(']',''))
                            self.select.in_selection_Layout_Temp.addWidget(self.select.in_selection_Temp)
                            in_selection_i += 1
                        elif in_selection_select_layout == 'H':
                            self.select.in_buttonGroup = QtWidgets.QButtonGroup(self.select.in_selection_Layout_Temp)
                            blocks = in_selection_block.split('[')[1].replace(']', '').split('|')
                            for block in blocks:
                                button_text = block.strip().replace('+', '')
                                self.select.in_selection_Button_Temp = QtWidgets.QRadioButton(self.select.scrollAreaWidgetContents)
                                self.select.in_selection_Button_Temp.setObjectName("HRB_" + str(Layout_i) + '_' + str(button_i) + '_' + str(in_selection_i))
                                self.select.in_selection_Button_Temp.setFont(font)
                                self.select.in_selection_Button_Temp.setMaximumSize(QtCore.QSize(self.metrics_optimize(font, button_text,min=40, add=40)))
                                self.select.in_selection_Button_Temp.setText(button_text)
                                self.select.in_selection_Button_Temp.setStyleSheet("background-color: rgb(0, 255, 0)")
                                self.select.in_selection_Layout_Temp.addWidget(self.select.in_selection_Button_Temp)
                                self.select.in_buttonGroup.addButton(self.select.in_selection_Button_Temp)
                                if '+' in block:
                                    self.select.in_selection_Button_Temp.setChecked(True)
                                self.select.in_selection_Button_Temp.toggled.connect(self.autoselect)
                                in_selection_i += 1
                        elif in_selection_select_layout == 'M':
                            self.select.in_buttonGroup = QtWidgets.QButtonGroup(self.select.in_selection_Layout_Temp)
                            self.select.in_buttonGroup.setExclusive(False)
                            blocks = in_selection_block.split('[')[1].replace(']', '').split('|')
                            for block in blocks:
                                button_text = block.strip().replace('+', '')
                                self.select.in_selection_Button_Temp = QtWidgets.QCheckBox(self.select.scrollAreaWidgetContents)
                                self.select.in_selection_Button_Temp.setObjectName("MCB_" + str(Layout_i) + '_' + str(button_i) + '_' + str(in_selection_i))
                                self.select.in_selection_Button_Temp.setFont(font)
                                self.select.in_selection_Button_Temp.setMaximumSize(QtCore.QSize(self.metrics_optimize(font, button_text,min=0, add=20)))
                                self.select.in_selection_Button_Temp.setText(button_text)
                                self.select.in_selection_Button_Temp.setStyleSheet("background-color: rgb(0, 255, 0)")
                                self.select.in_selection_Layout_Temp.addWidget(self.select.in_selection_Button_Temp)
                                self.select.in_buttonGroup.addButton(self.select.in_selection_Button_Temp)
                                if '+' in block:
                                    self.select.in_selection_Button_Temp.setChecked(True)
                                self.select.in_selection_Button_Temp.toggled.connect(self.autoselect)
                                in_selection_i += 1

                    if temp:
                        self.select.Lable_Temp = MycLabel(self.select.scrollAreaWidgetContents)
                        self.select.Lable_Temp.setObjectName("in_selection_Lable_" + str(Layout_i) + '_' + str(button_i) + '_' + str(in_selection_i))
                        #self.select.Lable_Temp.setMaximumSize(self.metrics_optimize(font, temp, min=0, add=40))
                        self.select.Lable_Temp.setText(temp)
                        #self.select.Lable_Temp.setMaximumSize(self.metrics_optimize(font, temp, add=40))
                        self.select.Lable_Temp.click_signal.connect(self.lable_click)
                        self.select.in_selection_Layout_Temp.addWidget(self.select.Lable_Temp)
                        in_selection_i += 1
                    else:
                        self.select.Lable_Temp = MycLabel(self.select.scrollAreaWidgetContents)
                        self.select.Lable_Temp.setObjectName("in_selection_Lable_" + str(Layout_i) + '_' + str(button_i) + '_' + str(in_selection_i))
                        #self.select.Lable_Temp.setMaximumSize(self.metrics_optimize(font, temp, min=0, add=40))
                        self.select.Lable_Temp.setText("")
                        #self.select.Lable_Temp.setMaximumSize(self.metrics_optimize(font, "", min=5))
                        self.select.Lable_Temp.click_signal.connect(self.lable_click)
                        self.select.in_selection_Layout_Temp.addWidget(self.select.Lable_Temp)
                        in_selection_i += 1


                else:
                    for Layout in self.select.scrollArea.findChildren(QtWidgets.QVBoxLayout,'Layout_' + str(Layout_i)):
                        Layout.addWidget(self.select.Button_Temp)
                    #self.select.horizontalLayout_0.addWidget(self.select.Button_Temp)
                button_i += 1

            title_i += 1
            Layout_i += 1
        #print(title_temp)
        if title_temp:
            block = title_temp.splitlines()
            for sents in block:
                if in_title_pattern.search(sents):
                    toki_sents = self.split_into_sentences(sents)
                    for sent in toki_sents:
                        in_title_result = in_title_pattern.findall(sent)
                        if in_title_result:
                            title_i, Layout_i = self.deal_with_in_title_obj(sent, Layout_i, title_i, in_title_result)
                        else:
                            obj_name = "label_" + str(title_i)
                            self.add_free_lable(sent,
                                              self.select.verticalLayout_2,
                                              obj_name,
                                              self.font)
                            title_i += 1
                else:
                    obj_name = "label_" + str(title_i)
                    self.add_free_lable(sents,
                                           self.select.verticalLayout_2,
                                           obj_name,
                                           self.font)
                    title_i += 1
        label_End = QtWidgets.QLabel(self.select.scrollAreaWidgetContents)
        label_End.setObjectName("label_End")
        label_End.setText(' ')

        self.adjustDialog()

        return

    def adjustDialog(self):
        self.adjustSize()
        width = self.sizeHint().width()
        height = self.sizeHint().height()
        if self.max_sent_length > (self.screen_width // 2):
            self.resize(self.screen_width // 2, height)


        return

    def deal_with_in_title_obj(self, sent, Layout_i, title_i, in_title_result):

        sent_longer = False
        in_title_i = 0
        Layout_Temp = ''
        for in_title_match in in_title_result:
            sent_before_match, sent = sent.split(in_title_match, 1)

            in_title_layout, in_title_block = in_title_match.split('[', 1)
            in_title_block = in_title_block.replace(']', '')
            if in_title_layout[1:]:
                length = int(in_title_layout[1:])
            else:
                length = 4
            totle_length = self.calculate_length(sent_before_match + sent) + length
            if totle_length > self.max_sent_length:
                self.max_sent_length = totle_length

            #print('totle:',totle_length)
            #print('width:',self.screen_width)

            if totle_length > (self.screen_width // 2):
                sent_longer = True
                #temp = ''
                while self.calculate_length(sent_before_match) > (self.screen_width // 2):
                    words = sent_before_match.split(' ')
                    residual_length = 0
                    temp = ''
                    while residual_length < (self.screen_width // 2) and words:
                        temp = temp + words.pop(0) + ' '
                        residual_length = self.calculate_length(temp)

                    obj_name = "label_" + str(title_i)
                    self.add_free_lable(temp, self.select.verticalLayout_2, obj_name, self.font)
                    title_i += 1
                    sent_before_match =  ' '.join(words)
                    if Layout_Temp:
                        Layout_Temp = ''

            if not Layout_Temp:
                Layout_Temp = QtWidgets.QHBoxLayout()
                Layout_Temp.setObjectName("Layout_in_title" + str(title_i))
                self.select.verticalLayout_2.addLayout(Layout_Temp)

            if sent_before_match:
                obj_name = "label_" + str(title_i) + '_' + str(in_title_i)
                self.add_simple_lable(sent_before_match,
                                      Layout_Temp,
                                      obj_name,
                                      self.font)
                in_title_i += 1

            if in_title_layout[0] == 'L':
                obj_name = 'L_' + str(Layout_i) + '_' + str(in_title_i)
                self.select.in_title_object.append(self.add_lineedit(in_title_block,
                                                                     Layout_Temp,
                                                                     obj_name,
                                                                     self.font,
                                                                     length))

                in_title_i += 1

            elif in_title_layout[0] == 'C':
                obj_name = 'C_' + str(Layout_i) + '_' + str(in_title_i)
                self.select.in_title_object.append(self.add_combobox(in_title_block,
                                                                     Layout_Temp,
                                                                     obj_name,
                                                                     self.font,
                                                                     length))
                in_title_i += 1
            else:
                self.select.in_title_object.append(False)

        #if sent_longer:
        #    if self.calculate_length(sent) > (self.screen_width // 2):

        obj_name = "label_" + str(title_i) + '_' + str(in_title_i)
        self.add_free_lable(sent,
                               Layout_Temp,
                               obj_name,
                               self.font)

        in_title_i += 1
        title_i += 1
        #Layout_i += 1

        #obj_name = "label_End"
        #self.add_simple_lable(" ",
        #                    Layout_Temp,
        #                    obj_name,
        #                    self.font)

        return title_i, Layout_i

    def add_simple_lable(self, text, layout, obj_name, font):

        label_Temp = QtWidgets.QLabel(self.select.scrollAreaWidgetContents)
        label_Temp.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        label_Temp.customContextMenuRequested.connect(self.lable_contextMenu)
        label_Temp.setFont(font)
        label_Temp.setMaximumSize(self.metrics_optimize(font, text, min=0))
        label_Temp.setObjectName(obj_name)
        label_Temp.setAlignment(QtCore.Qt.AlignLeft)
        label_Temp.setText(text)
        layout.addWidget(label_Temp)

        return label_Temp

    def add_lineedit(self, text, layout, obj_name, font, length):

        temp_object = QtWidgets.QLineEdit(self.select.scrollAreaWidgetContents)
        temp_object.setObjectName(obj_name)
        temp_object.setFont(font)
        temp_object.setMaximumSize(self.metrics_optimize(font, " " * length, min=20))
        temp_object.setText(text)
        layout.addWidget(temp_object)

        return temp_object

    def add_free_lable(self, text, layout, obj_name, font):

        temp_object = QtWidgets.QLabel(self.select.scrollAreaWidgetContents)
        temp_object.setObjectName(obj_name)
        temp_object.setFont(font)
        temp_object.setWordWrap(True)
        temp_object.setAlignment(QtCore.Qt.AlignLeft)
        # self.select.in_title_Temp.setMaximumWidth(40 * length)
        # temp_object.setMaximumSize(self.metrics_optimize(font, " " * length, min=20))
        temp_object.setText(text)
        layout.addWidget(temp_object)

        return temp_object


    def add_combobox(self, text, layout, obj_name, font, length):

        temp_object = MyComboBox(self.select.scrollAreaWidgetContents)
        temp_object.setObjectName(obj_name)
        # self.select.in_title_Temp.setMaximumWidth(40 * length)
        temp_object.setMaximumSize(self.metrics_optimize(font, " " * length, min=30))
        temp_object.addItems(text.split('|'))
        layout.addWidget(temp_object)

        return temp_object


    def split_into_sentences(self, text):

        alphabets = "([A-Za-z])"
        prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
        suffixes = "(Inc|Ltd|Jr|Sr|Co)"
        starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
        acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
        websites = "[.](com|net|org|io|gov)"
        head_number = "([1-9])[.]"
        smallnumber = "\d*[.]\d*"

        text = " " + text + "  "
        #text = text.replace("\n", " ")
        text = re.sub(prefixes, "\\1<prd>", text)
        text = re.sub(head_number, "\\1<prd>", text)
        text = re.sub(websites, "<prd>\\1", text)

        if "Ph.D" in text: text = text.replace("Ph.D.", "Ph<prd>D<prd>")
        text = re.sub("\s" + alphabets + "[.] ", " \\1<prd> ", text)
        text = re.sub(acronyms + " " + starters, "\\1<stop> \\2", text)
        text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]", "\\1<prd>\\2<prd>\\3<prd>", text)
        text = re.sub(alphabets + "[.]" + alphabets + "[.]", "\\1<prd>\\2<prd>", text)
        text = re.sub(" " + suffixes + "[.] " + starters, " \\1<stop> \\2", text)
        text = re.sub(" " + suffixes + "[.]", " \\1<prd>", text)
        text = re.sub(" " + alphabets + "[.]", " \\1<prd>", text)


        if "”" in text: text = text.replace(".”", "”.")
        if "\"" in text: text = text.replace(".\"", "\".")
        if "!" in text: text = text.replace("!\"", "\"!")
        if "?" in text: text = text.replace("?\"", "\"?")
        text = text.replace(". ", ".<stop>")
        #print(text)
        text = text.replace("?", "?<stop>")
        text = text.replace("!", "!<stop>")
        text = text.replace("<prd>", ".")
        sentences = text.split("<stop>")
        #sentences = sentences[:-1]
        #sentences = [s.strip() for s in sentences]

        #print(sentences)
        return sentences

    def calculate_length(self, text):
        metrics = QtGui.QFontMetrics(self.font)
        width = metrics.width(text)

        return width

    def metrics_optimize(self, font, text, min=200, add=0, mega=1.2):
        metrics = QtGui.QFontMetrics(font)
        height = metrics.height()
        if not text:
            return QtCore.QSize(min, height)
        multi = 1

        metrics = QtGui.QFontMetrics(font)
        height = metrics.height()
        width = metrics.width(text)
        if width > (self.screen_width // 2):
            multi = width // (self.screen_width // 2)
        if width > self.screen_width:
            width = self.screen_width
        elif width < min:
            width = min

        return QtCore.QSize((width + add) * mega, height * multi * 1.5)

    def __contextMenu(self):
        submenu = QtWidgets.QMenu()
        editmenu = submenu.addAction("Edit Template", )
        addmenu = submenu.addAction("Add Template", )
        delmenu = submenu.addAction("Del Template", )
        submenu.exec_(QtGui.QCursor.pos())
        return

    def lable_contextMenu(self):
        sender = self.sender()
        #print(sender.objectName())
        submenu = QtWidgets.QMenu()
        editmenu = submenu.addAction("Edit fixed template", partial(self.edit_template, sender))
        submenu.exec_(QtGui.QCursor.pos())

        return

    def edit_template(self, object):
        name = object.objectName()
        if 'label_' in name:
            label_index = int(name.split('_')[1])
            #print(label_index)
        edit_sent = ''
        if not self.select.match:
            pass
        elif label_index == 0:
            after_section = self.select.match[label_index]
            edit_sent = self.select.return_sent.split(after_section, 1)[0]
        elif len(self.select.match) <  label_index - 1:
            print('error when find text')
            return
        elif  len(self.select.match) == label_index:
            before_section = self.select.match[label_index - 1]
            edit_sent =  self.select.return_sent.split(before_section, 1)[1]
        else:
            before_section = self.select.match[label_index - 1]
            after_section = self.select.match[label_index]
            edit_sent = self.select.return_sent.split(before_section,1)[1].split(after_section,1)[0]
        #print(edit_sent)

        return


    def lable_click(self, event):
        obj_name = self.sender().objectName()
        Layout_i = obj_name.split('_')[3]
        button_i = obj_name.split('_')[4]
        for button in self.select.scrollArea.findChildren((QtWidgets.QRadioButton,QtWidgets.QCheckBox),"in_Button_M" + Layout_i + '_' + button_i):
            if not button.isChecked():
                button.setChecked(True)
            else:
                button.setChecked(False)
        return

    def keyPressEvent(self, event):
        if event.key() in (QtCore.Qt.Key_Return,QtCore.Qt.Key_Enter):
            self.focusNextChild()
        else:
            QtWidgets.QDialog.keyPressEvent(self, event)

        return

    def autoselect(self):
        obj_name = self.sender().objectName()
        Layout_i = obj_name.split('_')[1]
        button_i = obj_name.split('_')[2]
        if 'LE' in obj_name:
            for button in self.select.scrollArea.findChildren((QtWidgets.QRadioButton,QtWidgets.QCheckBox), "in_Button_M" + Layout_i + '_' + button_i):
                button.setChecked(True)
        elif 'HRB' in obj_name:
            if self.sender().isChecked():
                for button in self.select.scrollArea.findChildren((QtWidgets.QRadioButton,QtWidgets.QCheckBox),"in_Button_M" + Layout_i + '_' + button_i):
                    button.setChecked(True)
        elif 'MCB' in obj_name:
            if self.sender().isChecked():
                for button in self.select.scrollArea.findChildren((QtWidgets.QRadioButton,QtWidgets.QCheckBox),"in_Button_M" + Layout_i + '_' + button_i):
                    button.setChecked(True)

        return

    def blocksub(self, term, temp_dict={}):

        return

    def keywordlize(self, term):

        def _add_slash(matched):
            matched = '{}'.format(str('\\')) + matched.group()
            return matched

        term = re.sub('[\[\]\(\)\+\.\^\$\*\?\{\}\|]',_add_slash, term)
        return term

    def get_sent(self):

        def _combined_and(temp = [], seper=','):
            num = len(temp)
            seper = seper + ' '
            if seper==', ' and num > 2:
                Text = seper.join(temp[:num - 1]) + ' and ' + temp[-1]
            elif seper=='; ':
                Text = seper.join(temp)
            elif seper==', ' and num == 2:
                Text = temp[0] + ' and ' + temp[1]
            elif num == 1:
                Text = temp[0]
            else:
                Text = ''
            return Text.strip()

        i = 0
        in_selection_separator = ''

        block_pattern = re.compile('block\[\d+\]')
        conclusion = ''
        blocks = []
        for match_section in self.select.match:
            block = ''
            match_section = match_section.strip()
            seper = ','
            if not '{' in match_section or not '}' in match_section:
                return False

            if ',' in match_section:
                seper = ','
            elif ';' in match_section:
                seper = ';'
            else:
                seper = ','


            match_head = match_section.split('{')[0]
            select_layout = match_head[0]
            if len(match_head) > 1 and select_layout == 'M':
                in_selection_separator = match_head[-1]

            pattern = re.compile('G\d')
            g_layout = pattern.match(match_head)

            if select_layout == 'H':
                for Layout in self.select.scrollArea.findChildren(QtWidgets.QHBoxLayout,'Layout_' + str(i)):
                    for grouped_buttons in Layout.findChildren(QtWidgets.QButtonGroup):
                        if grouped_buttons.checkedButton():
                            block = grouped_buttons.checkedButton().text()
                            self.select.return_sent = re.sub(self.keywordlize(match_section),
                                                             block,
                                                             self.select.return_sent,
                                                             1)
                        else:
                            empty_keyword = '\s?' + self.keywordlize(match_section) + '\s?'
                            self.select.return_sent = re.sub(empty_keyword,
                                                             ' ',
                                                             self.select.return_sent,
                                                             1)

            elif select_layout == 'M' or select_layout == 'm':
                temp_list = []
                in_temp_list = []
                in_MCB_list = []
                regex = QtCore.QRegExp("(Button_M|in_Button_M)" + str(i) + "\_\d")
                for button in self.findChildren(QtWidgets.QCheckBox,regex):
                    if button.isChecked():
                        if not 'in_Button' in button.objectName():
                            temp_list.append(button.text())
                        else:
                            in_Button_empty = True
                            button_i = button.objectName().split('_')[3]
                            inkey = QtCore.QRegExp("(in_selection_Lable_|LE_|HRB_|MCB_)" + str(i) + "\_" + str(button_i) + "_")
                            in_temp_list = []
                            for obj in self.findChildren((QtWidgets.QLineEdit,QtWidgets.QRadioButton,QtWidgets.QCheckBox,QtWidgets.QLabel),inkey):
                                if 'HRB' in obj.objectName():
                                    if obj.isChecked():
                                        in_Button_empty = False
                                        in_temp_list.append(obj.text().strip())
                                elif 'MCB' in obj.objectName():
                                    if obj.isChecked():
                                        in_Button_empty = False
                                        in_MCB_list.append(obj.text().strip())
                                else:
                                    if in_MCB_list:
                                        if not in_selection_separator:
                                            in_temp_list.append(' '.join(in_MCB_list))
                                            in_MCB_list = []
                                        else:
                                            in_temp_list.append(in_selection_separator.join(in_MCB_list))
                                            in_MCB_list = []
                                    if in_Button_empty:
                                        in_temp_list.append(obj.text().lstrip())
                                    else:
                                        in_temp_list.append(obj.text())
                                        in_Button_empty = True
                            if in_MCB_list:
                                if not in_selection_separator:
                                    in_temp_list.append(' '.join(in_MCB_list))
                                    in_MCB_list = []
                                else:
                                    in_temp_list.append(in_selection_separator.join(in_MCB_list))
                                    in_MCB_list = []
                            temp_list.append(''.join(in_temp_list))
                if not temp_list:
                    empty_keyword = '\s?' + self.keywordlize(match_section) + '\s?'
                    self.select.return_sent = re.sub(empty_keyword, ' ', self.select.return_sent, 1)
                elif select_layout == 'M':
                    block = _combined_and(temp_list, seper=seper).replace('+','').replace('  ',' ')
                    self.select.return_sent = re.sub(self.keywordlize(match_section),
                                                block,
                                                self.select.return_sent,
                                                1)
                elif select_layout == 'm':
                    block = ' '.join(temp_list).replace('+','').replace('  ',' ')
                    self.select.return_sent = re.sub(self.keywordlize(match_section),
                                                block,
                                                self.select.return_sent,
                                                1)

            elif g_layout:
                temp_list = []
                for button in self.findChildren(QtWidgets.QCheckBox):
                    key = 'G' + str(i)
                    if key in button.objectName():
                        if button.isChecked():
                            temp_list.append(button.text())
                if not temp_list:
                    empty_keyword = '\s?' + self.keywordlize(match_section) + '\s?'
                    self.select.return_sent = re.sub(empty_keyword, ' ', self.select.return_sent, 1)
                else:
                    block = _combined_and(temp_list, seper=seper).replace('  ',' ').replace('+','')
                    self.select.return_sent = re.sub(self.keywordlize(match_section),
                                                     block,
                                                self.select.return_sent,
                                                1)

            elif select_layout == 'V' or select_layout == 'v':
                in_MCB_list = []
                for Layout in self.select.scrollArea.findChildren(QtWidgets.QVBoxLayout, 'Layout_' + str(i)):
                    for grouped_buttons in Layout.findChildren(QtWidgets.QButtonGroup):
                        if grouped_buttons.checkedButton():
                            if 'in_Button' in grouped_buttons.checkedButton().objectName():
                                in_Button_empty = True
                                button_i = grouped_buttons.checkedButton().objectName().split('_')[3]
                                inkey = QtCore.QRegExp("(in_selection_Lable_|LE_|HRB_|MCB_)" + str(i) + "\_" + str(button_i))
                                in_temp_list = []
                                for obj in self.findChildren((QtWidgets.QLineEdit,QtWidgets.QRadioButton, QtWidgets.QLabel), inkey):
                                    if 'HRB' in obj.objectName():
                                        if obj.isChecked():
                                            in_Button_empty = False
                                            in_temp_list.append(obj.text())
                                    elif 'MCB' in obj.objectName():
                                        if obj.isChecked():
                                            in_Button_empty = False
                                            in_MCB_list.append(obj.text())
                                    else:
                                        if in_MCB_list:
                                            if not in_selection_separator:
                                                in_temp_list.append(' '.join(in_MCB_list))
                                                in_MCB_list = []
                                            else:
                                                in_temp_list.append(in_selection_separator.join(in_MCB_list))
                                                in_MCB_list = []
                                        if in_Button_empty:
                                            in_temp_list.append(obj.text().lstrip())
                                        else:
                                            in_temp_list.append(obj.text())
                                            in_Button_empty = True
                                block = ''.join(in_temp_list).replace('  ',' ').replace('+','')
                                self.select.return_sent = re.sub(self.keywordlize(match_section),
                                                                 block,
                                                                 self.select.return_sent,
                                                                 1)

                            else:
                                block = grouped_buttons.checkedButton().text().replace('  ',' ').replace('+','')
                                self.select.return_sent = re.sub(self.keywordlize(match_section),
                                                                 block,
                                                                 self.select.return_sent,
                                                                 1)
                        else:
                            empty_keyword = '\s?' + self.keywordlize(match_section) + '\s?'
                            self.select.return_sent = re.sub(empty_keyword,' ',self.select.return_sent,1)

            elif select_layout == 'C' or select_layout == 'c':
                temp_list = []
                in_temp_list = []
                regex = QtCore.QRegExp("(Button_M|in_Button_M)" + str(i) + "\_\d")
                for button in self.findChildren(QtWidgets.QCheckBox,regex):
                    if button.isChecked():
                        if not 'in_Button' in button.objectName():
                            temp_list.append(button.text())
                        else:
                            button_i = button.objectName().split('_')[3]
                            inkey = QtCore.QRegExp("(in_selection_Lable_|LE_|HRB_)" + str(i) + "\_" + str(button_i))
                            in_temp_list = []
                            for obj in self.findChildren((QtWidgets.QLineEdit,QtWidgets.QRadioButton,QtWidgets.QLabel),inkey):
                                if 'HRB' in obj.objectName():
                                    if obj.isChecked():
                                        in_temp_list.append(obj.text())
                                else:
                                    in_temp_list.append(obj.text().strip())
                            temp_list.append(' '.join(in_temp_list))

                conclusion = ' '.join(temp_list).replace('  ',' ').replace('  ',' ')
                empty_keyword = '\s?' + self.keywordlize(match_section) + '\s?'
                self.select.return_sent = re.sub(empty_keyword,
                                                ' ',
                                                self.select.return_sent,
                                                1)

            else:
                for Layout in self.select.scrollArea.findChildren(QtWidgets.QVBoxLayout, 'Layout_' + str(i)):
                    for grouped_buttons in Layout.findChildren(QtWidgets.QButtonGroup):
                        if grouped_buttons.checkedButton():
                            block = grouped_buttons.checkedButton().text().replace('  ',' ')
                            self.select.return_sent = re.sub(self.keywordlize(match_section),
                                                             block,
                                                             self.select.return_sent,
                                                             1)
                        else:
                            empty_keyword = '\s?' + self.keywordlize(match_section) + '\s?'
                            self.select.return_sent = re.sub(empty_keyword,
                                                             ' ',
                                                             self.select.return_sent,
                                                             1)
            blocks.append(block)
            i = i + 1
        if conclusion:
            block_result = block_pattern.findall(conclusion)
            for block in block_result:
                index = int(block.replace('block[','').replace(']','')) - 1
                if index >= 0 and index < len(blocks):
                    conclusion = re.sub(self.keywordlize(block),blocks[index],conclusion,1)
        if blocks:
            block_result = block_pattern.findall(self.select.return_sent)
            for block in block_result:
                index = int(block.replace('block[', '').replace(']', '')) - 1
                if index >= 0 and index < len(blocks):
                    self.select.return_sent = re.sub(self.keywordlize(block),blocks[index],self.select.return_sent,1)

        in_title_pattern = re.compile('C\d*\[.*?\]|L\d*\[.*?\]')
        in_title_matchs = in_title_pattern.findall(self.select.return_sent)
        for index, in_title_match in enumerate(in_title_matchs):
            if index >= len(self.select.in_title_object):
                continue

            if self.select.in_title_object[index]:
                self.select.return_sent = re.sub(self.keywordlize(in_title_match),
                                                 self.select.in_title_object[index].text(),
                                                 self.select.return_sent,
                                                 1)


        if '(s)' in self.select.return_sent:
            if 'and' in self.select.return_sent:
                self.select.return_sent = self.select.return_sent.replace('(s)', 's')
            else:
                self.select.return_sent = self.select.return_sent.replace('(s)', '')
        if 'the bilateral' in self.select.return_sent:
            self.select.return_sent = self.select.return_sent.replace('the bilateral', 'bilateral')




        #self.select.return_sent = self.select.return_sent.replace('  ',' ')
        self.select.return_sent = self.select.return_sent.replace(' .', '.')
        self.select.return_sent = self.select.return_sent.replace(' ,', ',')
        return self.select.return_sent, conclusion

class SelectHighlighter(QtGui.QSyntaxHighlighter):

    def __init__(self, parent, active=True):
        QtGui.QSyntaxHighlighter.__init__(self, parent)
        self.parent = parent
        self.highlightingSelect = ''
        self.active = active

        return

    def highlightBlock(self, text):

        if not self.active or not self.highlightingSelect:
            return

        #WORDS = '\\b' + self.keywordlize(self.highlightingSelect) + '\\b'
        WORDS = self.highlightingSelect

        SelectBlock = Qt.QTextCharFormat()
        SelectBlock.setBackground(QtGui.QColor(255, 0, 0))
        conter = 0

        if text:
            result = text.find(WORDS)
            while result > -1 and conter < 100:
                self.setFormat(result, len(WORDS), SelectBlock)
                result = text.find(WORDS, result + len(WORDS))
                conter += 1

            #for word_object in re.finditer(WORDS, text):
            #    self.setFormat(word_object.start(), word_object.end() - word_object.start(), SelectBlock)

        return

    def keywordlize(self, term):

        def _add_slash(matched):
            matched = '{}'.format(str('\\')) + matched.group()
            return matched

        term = re.sub('[\[\]\(\)\+\.\^\$\*\?\{\}\|]',_add_slash, term)
        return term

    def selected_word(self, text):

        if text and len(text) > 2:
            self.highlightingSelect = text
            self.rehighlight()
        else:
            self.highlightingSelect = ''

class MyHighlighter(QtGui.QSyntaxHighlighter):

    def __init__(self, parent, active=True):
        QtGui.QSyntaxHighlighter.__init__(self, parent)
        self.parent = parent
        self.highlightingRules = []
        self.active = active

        return

    def highlightBlock(self, text):

        if not self.active:
            return

        WORDS = '\\b[a-z,A-Z]+\\b'

        wrongspell = Qt.QTextCharFormat()
        wrongspell.setUnderlineColor(QtGui.QColor(255, 0, 0))
        wrongspell.setUnderlineStyle(QtGui.QTextCharFormat.SpellCheckUnderline)

        if text:
            for word_object in re.finditer(WORDS, text):
                test_word = word_object.group()
                if len(test_word) > 2:
                    if test_word.isupper():
                        if not word_object.group() in myKeywords:
                            self.setFormat(word_object.start(), word_object.end() - word_object.start(), wrongspell)
                    elif not word_object.group().lower() in myKeywords:
                        self.setFormat(word_object.start(), word_object.end() - word_object.start(), wrongspell)

        return

    def set_active(self, action):
        self.active = action
        return

class MyDictionaryCompleter(QtWidgets.QCompleter):
#|-----------------------------------------------------------------------------|
# class Variables
#|-----------------------------------------------------------------------------|
    insertText = QtCore.pyqtSignal(str)
    #no classVariables
#|-----------------------------------------------------------------------------|
# Constructor
#|-----------------------------------------------------------------------------|
    def __init__(self, myKeywords=None,parent=None):

        QtWidgets.QCompleter.__init__(self, myKeywords, parent)
        self.activated.connect(self.changeCompletion)
        self.highlighted.connect(self.enter_completion)
        #self.connect(self, QtCore.SIGNAL("activated(const QString&)"), self.changeCompletion)
#|--------------------------End of Constructor---------------------------------|
#|-----------------------------------------------------------------------------|
# changeCompletion
#|-----------------------------------------------------------------------------|
    def enter_completion(self, completion):
        pass
        return

    def changeCompletion(self, completion):
        if completion.find("(") != -1:
            completion = completion[:completion.find("(")]
        self.insertText.emit(completion)

class MyTextEdit(QtWidgets.QTextEdit):
    shortcut = QtCore.pyqtSignal(str)
    #selected = QtCore.pyqtSignal(str)
    def __init__(self, *args, **kwargs):
        super(MyTextEdit, self).__init__(*args, **kwargs)
        #self.parent = parent
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.__contextMenu)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setBold(False)
        font.setWeight(50)
        self.setFont(font)
        self.lung_nodules = []
        self.completer = None

        return

    def highlightCurrentLine(self):
        extraSelections = []
        if not self.isReadOnly():
            selection = QtWidgets.QTextEdit.ExtraSelection()
            lineColor = QtGui.QColor(QtCore.Qt.yellow).lighter(160)
            selection.format.setBackground(lineColor)
            selection.format.setProperty(QtGui.QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)
        self.setExtraSelections(extraSelections)

    def setCompleter(self, completer):
        if self.completer:
            self.disconnect(self.completer, 0, self, 0)
        if not completer:
            return

        completer.setWidget(self)
        completer.setCompletionMode(QtWidgets.QCompleter.PopupCompletion)
        completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.completer = completer
        #        self.connect(self.completer,
        #            QtCore.SIGNAL("activated(const QString&)"), self.insertCompletion)
        self.completer.insertText.connect(self.insertCompletion)
        return

    def insertCompletion(self, completion):
        tc = self.textCursor()
        extra = (len(completion) -
            len(self.completer.completionPrefix()))
        tc.movePosition(QtGui.QTextCursor.Left)
        tc.movePosition(QtGui.QTextCursor.EndOfWord)
        tc.insertText(completion[-extra:])
        self.setTextCursor(tc)
        return

    def textUnderCursor(self):
        tc = self.textCursor()
        #print(tc.position())
        #print(tc.block().position())

        #tc.movePosition(QtGui.QTextCursor.PreviousWord)

        tc.select(QtGui.QTextCursor.WordUnderCursor)
        #print(tc.selectedText())

        #tc.movePosition(QtGui.QTextCursor.PreviousWord)
        #self.setCursor(tc)
        #tc = self.textCursor()
        #tc.select(QtGui.QTextCursor.WordUnderCursor)
        #print(tc.selectedText())

        return tc.selectedText()

    def focusInEvent(self, event):
        if self.completer:
            self.completer.setWidget(self)
        QtWidgets.QTextEdit.focusInEvent(self, event)

        return

    def keyPressEvent(self, event):
        isMoveUpper = (event.modifiers() == QtCore.Qt.ControlModifier and event.key() == QtCore.Qt.Key_Up)
        isMoveDown = (event.modifiers() == QtCore.Qt.ControlModifier and event.key() == QtCore.Qt.Key_Down)
        iskeyShutcut = (event.key() == QtCore.Qt.Key_Backslash)

        if isMoveUpper or isMoveDown:
            self.moveline(event.key())
            return

        if iskeyShutcut:
            self.shortcut.emit(self.textUnderCursor())
            return

        if not self.textUnderCursor():
            QtWidgets.QTextEdit.keyPressEvent(self, event)
            if self.completer and self.completer.popup() and self.completer.popup().isVisible():
                self.completer.popup().hide()
            return

        if self.completer and self.completer.popup() and self.completer.popup().isVisible():
            print('pop')
            if event.key() in (
                    QtCore.Qt.Key_Return,
                    QtCore.Qt.Key_Enter,
                    QtCore.Qt.Key_Escape,
                    QtCore.Qt.Key_Tab,
                    QtCore.Qt.Key_Backtab):
                event.ignore()
                return

        #isSelected = (event.key() == QtCore.Qt.Key_Enter or event.key() == QtCore.Qt.Key_Return)
        #misShortcut = (event.key() == QtCore.Qt.Key_Space)
        isShortcut = (event.key() == QtCore.Qt.Key_Tab or event.key() == QtCore.Qt.Key_Enter)
        inline = (event.modifiers() == QtCore.Qt.ControlModifier and event.key() == QtCore.Qt.Key_Right)
            # if inline completion has been chosen

        if inline:
                # set completion mode as inline
            self.completer.setCompletionMode(QtWidgets.QCompleter.InlineCompletion)
            completionPrefix = self.textUnderCursor()
            if (completionPrefix != self.completer.completionPrefix()):
                self.completer.setCompletionPrefix(completionPrefix)
            self.completer.complete()
            self.completer.insertText.emit(self.completer.currentCompletion())
            self.completer.setCompletionMode(QtWidgets.QCompleter.PopupCompletion)
            return

        if (not isShortcut):
            QtWidgets.QTextEdit.keyPressEvent(self, event)
            return
            # debug
            #        print("After controlspace")
            #        print("isShortcut is: {}".format(isShortcut))
            # debug over
            ## ctrl or shift key on it's own??
        ctrlOrShift = event.modifiers() in (QtCore.Qt.ControlModifier, \
                                                QtCore.Qt.ShiftModifier)
        #if ctrlOrShift and event.text() == '':
                #             ctrl or shift key on it's own
        #    return

        eow = "~!@#$%^&*+{}|:\"<>?,./;'[]\\-="  # end of word

        hasModifier = ((event.modifiers() != QtCore.Qt.NoModifier) and \
                           not ctrlOrShift)
        completionPrefix = self.textUnderCursor()
        #not_pop_completer = (event.key() in (QtCore.Qt.Key_Space, QtCore.Qt.Key_Left, QtCore.Qt.Key_Right, QtCore.Qt.Key_Period, QtCore.Qt.Key_Up))

        #if not self.completer or not_pop_completer:
        #    #QtWidgets.QTextEdit.keyPressEvent(self, event)
        #    if self.completer and self.completer.popup() and self.completer.popup().isVisible():
        #        self.completer.popup().hide()
        #    return

        self.completer.setCompletionPrefix(completionPrefix)
        popup = self.completer.popup()
        popup.setCurrentIndex(self.completer.completionModel().index(0, 0))
        cr = self.cursorRect()
        cr.setWidth(self.completer.popup().sizeHintForColumn(0) + self.completer.popup().verticalScrollBar().sizeHint().width())
        self.completer.complete(cr)  ## popup it up!

    def moveline(self, event_key):
        if event_key == QtCore.Qt.Key_Down:
            first_line = False
            cursor = self.textCursor()
            if cursor.blockNumber() == 0:
                first_line = True
            cursor.select(QtGui.QTextCursor.BlockUnderCursor)
            temp = cursor.selectedText()
            cursor.removeSelectedText()

            if first_line:
                cursor.deleteChar()
            else:
                cursor.movePosition(QtGui.QTextCursor.NextBlock)

            if cursor.blockNumber() == self.document().blockCount() - 1:
                cursor.movePosition(QtGui.QTextCursor.EndOfBlock)
                cursor.insertText(linesep)
            else:
                cursor.movePosition(QtGui.QTextCursor.NextBlock)
            cursor.insertText(temp.strip() + linesep)
            cursor.movePosition(QtGui.QTextCursor.PreviousBlock)

            self.setTextCursor(cursor)
        elif event_key == QtCore.Qt.Key_Up:
            cursor = self.textCursor()
            if cursor.blockNumber() == 0:
                return
            cursor.select(QtGui.QTextCursor.BlockUnderCursor)
            temp = cursor.selectedText()
            cursor.removeSelectedText()
            cursor.movePosition(QtGui.QTextCursor.StartOfBlock)
            cursor.insertText(temp.strip() + linesep)
            cursor.movePosition(QtGui.QTextCursor.PreviousBlock)
            self.setTextCursor(cursor)
        return

    def __contextMenu(self):
        modifiers = QtWidgets.QApplication.keyboardModifiers()
        if modifiers == QtCore.Qt.ControlModifier:
            #self._normalMenu = self.createStandardContextMenu()
            #self._addCustomMenuItems(self._normalMenu)
            #self._normalMenu.exec_(QtGui.QCursor.pos())
            self.phraseFunc()
        else:
            #self.phraseFunc()
            self._normalMenu = self.createStandardContextMenu()
            self._addCustomMenuItems(self._normalMenu)
            self._normalMenu.exec_(QtGui.QCursor.pos())

        return

    def _addCustomMenuItems(self, menu):
        #menu.addAction('片語', self.phraseFunc)
        menu.addSeparator()
        menu.addAction('Paste Arranged', self.paste_arranged)
        menu.addAction('Measurement', self.measurement)

        return

    def paste_arranged(self):
        win32clipboard.OpenClipboard()
        text = win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)
        win32clipboard.CloseClipboard()
        number_label = re.compile('\d+\.\s')

        temp = ''
        for sent in text.splitlines():
            sent = sent.strip()
            result = number_label.match(sent)
            if not temp:
                if result:
                    temp = sent.replace(result.group(0), "", 1)
                else:
                    temp = sent
            elif result:
                temp = temp + linesep + sent.replace(result.group(0), "", 1)
            else:
                temp = temp + ' ' + sent

        self.insertPlainText(temp)

        return

    def measurement(self):

        def _is_in_parentheses(text, pos):
            # find right paretheses
            beg = 0
            next_beg = 0
            if text.find(')',pos) == -1:
                return False

            while not next_beg == -1:
                beg = next_beg
                next_beg = text.find(')', beg + 1, pos)

            if beg == 0 and text.find('(', beg, pos) > 0:
                return True
            if text.find('(', beg + 1, pos) == -1:
                return False
            else:
                return True

        self.measure = MyMeasure(myapp)
        if self.measure.exec_():
            measure_result = self.measure.get_data()
            text = self.textCursor().block().text()
            pos = self.textCursor().positionInBlock()
            if measure_result:
                if _is_in_parentheses(text, pos):
                    self.insert_text('/' + measure_result)
                else:
                    self.insert_text('(' + measure_result + ')')

        return


    def phraseFunc(self):
        submenu = QtWidgets.QMenu()
        #lndmenu = submenu.addAction('Lung nodule', self.new_lung_nodule)
        mesmenu = submenu.addAction('Measurement', self.measurement)

        submenu.exec_(QtGui.QCursor.pos())

    def insert_text(self, Text):
        self.insertPlainText(Text)
        return

class MyautokeyinForm(QtWidgets.QMainWindow):
    date = QtCore.pyqtSignal(str)
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.autokeyin = Ui_autokeyinForm()
        self.autokeyin.setupUi(self)
        self.finaldate = ''
        #self.autokeyin.installEventFilter(self)

        return

    def eventFilter(self, qobject, qevent):
        qtype = qevent.type()
        if qtype == QtCore.Qt.QEvent.FocusOut:
            #disable the stay on top flag, by setting some other flag
            self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
            return True
        return super(MyautokeyinForm, self).eventFilter(qobject, qevent)

    def get_date(self):

        return self.finaldate

class MyWin(QtWidgets.QMainWindow):

    def __init__(self, parent=None):

        class MyTitle_ID:
            # for title management
            def __init__(self, parent, default_title=''):
                self.title = default_title
                self.current_id = ''
                self.parent = parent
                self.parent.setWindowTitle(self.title)
                return

            def to_current_id(self):
                return self.current_id

            def set_current_id(self, id):
                self.current_id = id
                self.parent.setWindowTitle(self.title + '-' + id)

        QtWidgets.QWidget.__init__(self, parent)
        # QtCore.Qt.WindowStaysOnTopHint       |
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.mytitle_id = MyTitle_ID(self, 'Report generator')
        self.init_dictionary()

        #self.seeting_member = {'Send report by AHK':True,
        #                       'Adding line number when sending':True}

        self.ui.patient_date = {}
        #self.ui.current_id = ''
        self.template_path = temp_file_path + '/default.json'
        self.init_tempfile()
        self.datebase = Iner_database(self, template_file = self.template_path)

        self.ui.clipboard = QtWidgets.QApplication.clipboard()
        self.ui.treeWidget.setColumnHidden(2, True)
        self.ui.treeWidget.setColumnHidden(3, True)
        self.ui.treeWidget.setColumnHidden(4, True)
        self.ui.treeWidget.setColumnHidden(5, True)
        self.ui.treeWidget.setColumnWidth(0, 180)
        self.ui.treeWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ui.treeWidget.customContextMenuRequested.connect(self.__contextMenu)
        self.ui.tabWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ui.tabWidget.customContextMenuRequested.connect(self.__tabcontextMenu)

        self.ui.seetingBox.currentTextChanged.connect(self.seeting_changed)
        self.ui.patient_comboBox.view().setDragDropMode(Qt.QAbstractItemView.NoDragDrop)

        self.ui.Findings_Layout = QtWidgets.QHBoxLayout(self.ui.Findings)
        self.ui.textEdit = MyTextEdit(self.ui.Findings)
        self.ui.textEdit.setObjectName("textEdit")
        self.ui.textEdit.setFrameStyle(QtWidgets.QFrame.NoFrame)
        self.ui.textEdit.setAcceptRichText(False)
        self.ui.text_number_bar = NumberBar()
        self.ui.text_number_bar.setTextEdit(self.ui.textEdit)
        self.completer = MyDictionaryCompleter(myKeywords)
        self.ui.textEdit.setCompleter(self.completer)
        self.textSpellingCheck = MyHighlighter(self.ui.textEdit)
        self.ui.textEdit.shortcut.connect(self.shortcut)
        self.ui.textEdit.selectionChanged.connect(self.selected)

        # install number bar to the text edit
        self.ui.Findings_Layout.addWidget(self.ui.text_number_bar)
        self.ui.Findings_Layout.addWidget(self.ui.textEdit)
        self.ui.Findings_Layout.setSpacing(0)
        self.ui.textEdit.installEventFilter(self)
        self.ui.textEdit.viewport().installEventFilter(self)
        self.change_count = 0
        self.ui.textEdit.textChanged.connect(self.text_changed)


        #self.ui.History_Layout = QtWidgets.QHBoxLayout(self.ui.History)
        #self.ui.HistoryEdit = MyTextEdit(self.ui.History)
        #self.ui.HistoryEdit.setAcceptRichText(False)
        #self.ui.HistoryEdit.setObjectName("HistoryEdit")
        #self.ui.HistoryEdit.setFrameStyle(QtWidgets.QFrame.NoFrame)
        ##self.Historycompleter = MyDictionaryCompleter(myKeywords)
        ##self.ui.HistoryEdit.setCompleter(self.Historycompleter)
        #self.HistorySpellingCheck = MyHighlighter(self.ui.HistoryEdit)
        #self.ui.History_Layout.addWidget(self.ui.HistoryEdit)

        #self.ui.number_bar = NumberBar()
        #self.ui.Conclusions_Layout = QtWidgets.QHBoxLayout(self.ui.Conclusions)
        #self.ui.ConclusionsEdit = MyTextEdit(self.ui.Conclusions)
        #self.ui.ConclusionsEdit.setAcceptRichText(False)
        #self.ui.ConclusionsEdit.setFrameStyle(QtWidgets.QFrame.NoFrame)
        #self.ui.ConclusionsEdit.setObjectName("ConclusionsEdit")
        #self.ConclusionsSpellingCheck = MyHighlighter(self.ui.ConclusionsEdit)
        #self.ui.number_bar.setTextEdit(self.ui.ConclusionsEdit)
        #self.ui.Conclusions_Layout.setSpacing(0)
        #self.ui.Conclusions_Layout.addWidget(self.ui.number_bar)
        #self.ui.Conclusions_Layout.addWidget(self.ui.ConclusionsEdit)

        #self.ui.ConclusionsEdit.installEventFilter(self)
        #self.ui.ConclusionsEdit.viewport().installEventFilter(self)

        self.ui.clear_Button.clicked.connect(self.clearer)
        self.ui.take_Button.clicked.connect(self.take)
        self.ui.tabWidget.currentChanged.connect(self.tabchange)
        self.ui.addButton.clicked.connect(self.add_patient)
        self.ui.patient_comboBox.currentIndexChanged.connect(self.patient_changed)
        self.ui.save_Button.clicked.connect(self.save_all)
        self.ui.patient_id.returnPressed.connect(self.enter_event)
        self.ui.note_Button.clicked.connect(self.show_note)
        self.ui.Conculsion_Button.clicked.connect(self.make_conculsion)
        self.ui.template_tool.clicked.connect(self.template_tool_menu)
        self.ui.cleanButton.clicked.connect(self.clean_patient)

        self.ui.treeWidget.itemDoubleClicked.connect(self.input)

        self.mynote = Mysimple_noted(self)

        self.mynote.update.connect(self.update_note)
        self.check_temp()

        return

    def init_dictionary(self):
        #myKeywords.append('tracer')
        global myKeywords
        myKeywords = []

        temp =''
        file_path = './setting/autocompwords.txt'
        with open(file_path, 'r', encoding='utf-8-sig') as file_text:
            temp = file_text.read()

        if temp:
            for word in temp.splitlines():
                if word.strip():
                    myKeywords.append(word.strip())
            myKeywords.sort()

        return

    def init_menubar(self):
        #seeting_member = ['Send report by AHK','Adding line number when sending']


        for seeting in self.seeting_member.keys():
            action_obj = QtWidgets.QAction(seeting, self.ui.menuSeeting)
            action_obj.setCheckable(True)
            #action_obj.toggled.connect(self.seeting_changed)
            if self.seeting_member[seeting]:
                action_obj.setChecked(True)
            self.ui.menuSeeting.addAction(action_obj)


        return


    def template_tool_menu(self):
        submenu = QtWidgets.QMenu()
        loadmenu = submenu.addAction("Load from other file", self.load_template_file)
        import_text_menu = submenu.addAction("Import from Text file", self.import_text_file)
        newmenu = submenu.addMenu("Create new file")
        newmenu.addAction("Creat from current template", self.new_file)
        newmenu.addAction("Creat an empty one", self.empty_file)


        #delmenu = submenu.addAction("Import from RTF file", self.del_template)
        submenu.exec_(QtGui.QCursor.pos())

        return

    def selected(self):
        cursor = self.ui.textEdit.textCursor()
        keyword = cursor.selectedText()
        self.mynote.selection(keyword)

        return

    def new_file(self):
        default_path = './setting/template'
        file_path, filter = QtWidgets.QFileDialog.getSaveFileName(self, 'New template', default_path,
                                                                  filter="json (*.json *.)")
        if not file_path:
            return

        self.datebase.creat_new(file_path, copy=True)
        self.init_tempfile()

        return

    def empty_file(self):
        default_path = './setting/template'
        file_path, filter = QtWidgets.QFileDialog.getSaveFileName(self, 'New template', default_path,
                                                                  filter="json (*.json *.)")
        if not file_path:
            return

        self.datebase.creat_new(file_path, copy=False)
        self.init_tempfile()

        return



    def import_text_file(self):
        def_path = getenv("HomePath")
        file_path, filter = QtWidgets.QFileDialog.getOpenFileName(self, 'Open template', def_path,
                                                                  filter="text (*.txt *.)")
        if not file_path:
            return
        text = ''
        sents = []
        with open(file_path, 'r', encoding='utf-8-sig') as file_text:
            while True:
                sent = file_text.readline()
                if sent == '': break
                if sent.strip():
                    sents.append(sent)

        self.ui.import_diag = Myimport(myapp, sents, self.datebase.category_list)
        if self.ui.import_diag.exec_():
            results = self.ui.import_diag.get_date()
            self.datebase.import_template(results)

        return

    def load_template_file(self):
        def_path = getenv("HomePath")
        file_path, filter = QtWidgets.QFileDialog.getOpenFileName(self, 'Open template', def_path,
                                                                  filter="json (*.json *.)")
        if not file_path:
            return
        self.template_path = file_path
        self.template_dict[file_path] = file_path
        self.ui.seetingBox.addItem(file_path)
        self.ui.seetingBox.setCurrentIndex(self.ui.seetingBox.findText(file_path, QtCore.Qt.MatchExactly))
        self.datebase.change_template(self.template_path)

    def closeEvent(self, event):

        quit_msg = "Are you sure you want to exit the program?"
        reply = QtWidgets.QMessageBox.question(self, 'Message',
                                           quit_msg, QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
        return

    def update_note(self):
        current_id = self.mytitle_id.to_current_id()
        self.save_patient(current_id)

        return

    def check_temp(self):
        if not path.isfile('temp.json'):
            return
        reply = QtWidgets.QMessageBox.warning(self, 'Do you want to restore last work?', 'It seems that the app is crash last time?',
                                              QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.No:
            try:
                remove('temp.json')
            except OSError as e:
                print(e)
            else:
                print("Temp File is deleted successfully")
            return
        with open('temp.json', 'r') as file_json:
            self.ui.patient_date = json.load(file_json)
        self.ui.patient_comboBox.addItems(self.ui.patient_date.keys())
        self.ui.patient_comboBox.setCurrentIndex(0)

        return

    def show_note(self):
        current_id = self.ui.patient_comboBox.currentText()
        if current_id  in self.ui.patient_date.keys():
            self.mynote.show()
            note = self.ui.patient_date[current_id]['patient_note']
            self.mynote.mynote.textEdit.setPlainText(note)
            self.mynote.setWindowTitle(str(current_id))
        else:
            self.mynote.show()
        return

    def seeting_changed(self, text):
        if not text:
            return
        if not '/' in self.template_dict[text]:
            self.template_path = temp_file_path + '/' + self.template_dict[text]
        else:
            self.template_path = self.template_dict[text]


        self.datebase.change_template(self.template_path)

        return


    def init_tempfile(self):

        def _find_csv_filenames(suffix=".json"):
            filenames = listdir(temp_file_path)
            return [filename for filename in filenames if filename.endswith(suffix)]
        self.template_dict = {}
        for template_file in _find_csv_filenames():
            self.template_dict[template_file.split('.')[0]] = template_file

        self.ui.seetingBox.clear()
        self.ui.seetingBox.addItems(self.template_dict.keys())

        if 'default' in self.template_dict.keys():
            self.ui.seetingBox.setCurrentIndex(self.ui.seetingBox.findText('default'))
            self.template_path = temp_file_path + '/' + self.template_dict[self.ui.seetingBox.currentText()]
        else:
            self.ui.seetingBox.setCurrentIndex(0)
            self.template_path = temp_file_path + '/' + self.template_dict[self.ui.seetingBox.currentText()]


        return

    def eventFilter(self, object, event):
        # Update the line numbers for all events on the text edit and the viewport.
        # This is easier than connecting all necessary singals.
        #if object in (self.ui.ConclusionsEdit,
        #              self.ui.ConclusionsEdit.viewport()):
        #    self.ui.number_bar.update()
        #    return False
        if object in (self.ui.textEdit,
                        self.ui.textEdit.viewport()):
            self.ui.text_number_bar.update()
            return False
        return QtWidgets.QFrame.eventFilter(object, event)

    def make_conculsion(self):
        text = self.ui.textEdit.toPlainText()
        self.conculsion = Myconclusion(self, text)
        self.conculsion.exec_()

        return

    def text_changed(self):

        if not self.ui.patient_date:
            return
        if self.change_count > 5:
            with open('temp.json', 'w') as file_json:
                json.dump(self.ui.patient_date, file_json)
            self.change_count = 0

        self.change_count = self.change_count + 1
        return

    def __combo_contextMenu(self):
        submenu = QtWidgets.QMenu()
        editmenu = submenu.addAction("Edit Template", self.edit_template)
        addmenu = submenu.addAction("Add Template", self.add_template)
        delmenu = submenu.addAction("Del Template", self.del_template)

        submenu.exec_(QtGui.QCursor.pos())

        return

    def __tabcontextMenu(self):
        submenu = QtWidgets.QMenu()
        edit_tab = submenu.addAction("Edit Tab", self.edit_tab)
        add_tab = submenu.addAction("Add Tab", self.add_tab)
        del_tab = submenu.addAction("Del Tab", self.del_tab)

        submenu.exec_(QtGui.QCursor.pos())


    def edit_tab(self):
        tab_index = self.ui.tabWidget.currentIndex()
        tab_name = self.ui.tabWidget.tabText(tab_index)

        category_list = self.datebase.category_list
        category = self.datebase.connect_by_tab(tab_name)
        tab_list = self.datebase.template['tab']['List']
        current_index = tab_list.index(tab_name)

        self.ui.tabedit = MyTabEdit(myapp, category_list, self.ui.tabWidget.count(), index=tab_index, category=category, tab_name=tab_name)
        if self.ui.tabedit.exec_():
            result = self.ui.tabedit.get_date()
            self.datebase.edit_tab(tab_name, result)

        return

    def add_tab(self):
        tab_index = self.ui.tabWidget.currentIndex()
        tab_name = self.ui.tabWidget.tabText(tab_index)

        category_list = self.datebase.category_list
        self.ui.tabedit = MyTabEdit(myapp, category_list, self.ui.tabWidget.count(), index=tab_index)
        if self.ui.tabedit.exec_():
            result = self.ui.tabedit.get_date()
            if not result['name']:
                return
            self.datebase.add_tab(result)

        return

    def del_tab(self):
        tab_index = self.ui.tabWidget.currentIndex()
        tab_name = self.ui.tabWidget.tabText(tab_index)

        quest = 'You are going to delete "' + tab_name + '" tab.\n Are you sure?'
        reply = QtWidgets.QMessageBox.warning(self, 'Are you sure?',
                                              quest,
                                              QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.No:
            return

        self.datebase.del_tab(tab_name)

        return

    def __contextMenu(self):
        item = self.ui.treeWidget.currentItem()
        if not item.parent():
            is_root = True
        else:
            is_root = False

        submenu = QtWidgets.QMenu()

        if not is_root:
            editmenu = submenu.addAction("Edit Template", self.edit_template)
        addmenu = submenu.addAction("Add Template", self.add_template)
        if not is_root:
            delmenu = submenu.addAction("Del Template", self.del_template)
        if is_root:
            rename_category_menu = submenu.addAction("Rename Category", self.rename_category)
            add_category_menu = submenu.addAction("Add Category", self.add_category)
            del_category_menu = submenu.addAction("Del Category", self.del_category)

        submenu.exec_(QtGui.QCursor.pos())

        return

    def rename_category(self):
        item = self.ui.treeWidget.currentItem()
        if item.parent():
            return
        category = item.text(0)
        if category == 'Common':
            QtWidgets.QMessageBox.warning(self, 'Warning!!',
                                          'Common category cannot be rename',
                                          QtWidgets.QMessageBox.Ok)
            return

        self.ui.simpledit = MySinpleditor(myapp, category)
        if self.ui.simpledit.exec_():
            result = self.ui.simpledit.get_date()
            if result == category:
                return
            else:
                self.datebase.rename_category(category, result)

        return

    def add_category(self):
        item = self.ui.treeWidget.currentItem()
        if item.parent():
            return
        category_list = self.datebase.category_list
        self.ui.simpledit = MySinpleditor(myapp, "", category_list)
        if self.ui.simpledit.exec_():
            result = self.ui.simpledit.get_date()
            if result:
                self.datebase.add_category(item.text(0), result)

        return

    def del_category(self):
        item = self.ui.treeWidget.currentItem()
        if item.parent():
            return
        category = item.text(0)
        if category == 'Common':
            QtWidgets.QMessageBox.warning(self, 'Warning!!',
                                          'Common category cannot be deleted',
                                          QtWidgets.QMessageBox.Ok)
            return
        quest = 'You are going to delete a category.\n All template in the category will be lost.\n Are you sure?'
        reply = QtWidgets.QMessageBox.warning(self, 'Are you sure?',
                                              quest,
                                              QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.No:
            return
        self.datebase.del_category(category)

        return


    def edit_template(self):
        item = self.ui.treeWidget.currentItem()
        if not item.parent():
            return

        shortcut_values = self.datebase.get_all_shortcut()
        category = item.parent().text(0)
        index = item.text(2).strip()

        self.ui.editor = Myeditor(myapp, item, self.datebase.category_list, shortcut_values)
        if self.ui.editor.exec_():
            result = self.ui.editor.get_date()
            if result:
                #print('{ is', result['description'])
                if self.datebase.edit_by_index(index, result):
                    item.setText(0, result['shortcut'])
                    if not result['description']:
                        main_text, isMultrow = self.check_if_multirow(result['main'])
                    else:
                        main_text = result['description']
                        isMultrow = 'True'

                    item.setText(1, main_text)
                    item.setText(3, isMultrow)
                    item.setText(4, result['main'])
                    self.shortcut_dict = self.datebase.get_all_shortcut()

            return

    def add_template(self):
        item = self.ui.treeWidget.currentItem()
        if not item.parent():
            category = item.text(0)
            index = 0
        else:
            category = item.parent().text(0)
            index = int(item.text(2)) + 1

        shortcut_values = self.datebase.get_all_shortcut()

        self.ui.editor = Myeditor(myapp, item, self.datebase.category_list, shortcut_values, mode='a')
        if self.ui.editor.exec_():
            result = self.ui.editor.get_date()
            if result:
                self.datebase.insert_by_index(index, result)
        return

    def del_template(self):
        item = self.ui.treeWidget.currentItem()
        if not item.parent():
            return

        reply = QtWidgets.QMessageBox.warning(self, 'Are you sure?',
                                              'You are going to delete a template. Are you sure?',
                                              QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.No:
            return
        category = item.parent().text(0)
        index = item.text(2)
        self.datebase.del_by_index(category, index)

        return

    def check_if_multirow(self, text):
        temp = text.splitlines()
        text = temp[0]
        if len(temp) > 1:
            return text, 'True'
        else:
            return text, 'False'


    def shortcut(self, key):

        items = self.ui.treeWidget.findItems(key,QtCore.Qt.MatchRecursive|QtCore.Qt.MatchExactly,0)
        if not items:
            return

        first_item = items[0]
        if not first_item.parent():
            return

        cursor = self.ui.textEdit.textCursor()
        cursor.select(QtGui.QTextCursor.WordUnderCursor)
        self.ui.textEdit.setTextCursor(cursor)
        self.input(first_item, 1)

        return

    def checked_to_next(self):
        combo_name = self.ui.tabWidget.currentWidget().objectName()
        index_next = self.ui.tabWidget.currentIndex() + 1
        if index_next >= self.ui.tabWidget.count():
            index_next = 0
        self.ui.tabWidget.setCurrentIndex(index_next)

        for obj in self.ui.tabWidget.findChildren(QtWidgets.QComboBox):
            if obj.objectName() == 'combo_' + combo_name:
                if not obj.currentIndex():
                    obj.setCurrentIndex(2)

        return

    def enter_event(self):
        self.add_patient()
        self.ui.patient_id.selectAll()

        return

    def save_all(self):
        home_path = getenv("HomePath")
        index_text = {0:'Uncheck',1:'Normal', 2:'Checked', 3:'Abnormal'}
        def_path = home_path + '\\Desktop\\' + datetime.date.today().strftime("%Y%m%d") + '.txt'
        dname = ''
        file_path, filter = QtWidgets.QFileDialog.getSaveFileName(self, 'Save report', def_path, filter ="txt (*.txt *.)")
        if not self.ui.patient_date or not file_path:
            return

        current_id = self.ui.patient_comboBox.currentText()
        if current_id == self.ui.patient_id.text():
            self.save_patient(current_id)

        Text = ''

        for id in self.ui.patient_date.keys():
            Text = Text + 'PatientID:' + id + linesep

            if 'combo_status' in self.ui.patient_date[id].keys():
                for check_list in self.ui.patient_date[id]['combo_status']:
                    check_name = check_list.replace('combo_', '').capitalize()
                    Text = Text + check_name + ':' + index_text[self.ui.patient_date[id]['combo_status'][check_list]] + linesep

            if 'Text' in self.ui.patient_date[id].keys():
                Temp = self.ui.patient_date[id]['Text']
                if Temp:
                    Text = Text + linesep
                    n = 1
                    for sent in Temp.splitlines():
                        if sent and not 'conclusion' in sent.lower():
                            sent = str(n) + '. ' + sent.strip()
                            n = n + 1
                        elif 'CONCLUSIONS' in sent:
                            n = 1
                        Text = Text + sent + linesep
            Text = Text + linesep + '-----------------END----------------' + linesep

        if Text:
            with open(file_path, 'w', encoding='utf-8-sig') as f:
                f.write(Text)

        return

    def add_patient(self):
        id = self.ui.patient_id.text()
        if not id:
            return
        if id in self.ui.patient_date.keys():
            reply = QtWidgets.QMessageBox.warning(self, 'Patient repeat', 'The '+ id + ' is already in the list!',
                                                  QtWidgets.QMessageBox.Ok )
            return
        current = self.mytitle_id.to_current_id()
        if current:
            self.save_patient(current)
            self.clearer('yes')

        combo_used = False
        combo_status = {}
        note = ""
        Text = self.ui.textEdit.toPlainText()
        note = self.mynote.mynote.textEdit.toPlainText()
        for combo in self.ui.tabWidget.findChildren(QtWidgets.QComboBox):
            combo_status[combo.objectName()] = combo.currentIndex()
            if combo.currentIndex():
                combo_used = True
        if not self.ui.patient_comboBox.currentIndex():
            if Text or combo_used or note:
                reply = QtWidgets.QMessageBox.warning(self, 'The current content',
                                                      'Dose the existing content belong to ' + id + ' or will be clear!!',
                                                      QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Cancel)
                if reply == QtWidgets.QMessageBox.Cancel:
                    return
                if reply == QtWidgets.QMessageBox.No:
                    self.clearer('yes') # clean the content
                else:
                    current_id = self.mytitle_id.to_current_id()
                    self.ui.patient_date[current_id] = {'Text': Text,
                                                        'combo_status': combo_status,
                                                        'patient_note':note}

        self.mytitle_id.set_current_id(id)
        self.mynote.setWindowTitle(id)
        #self.ui.current_id = id
        self.ui.patient_date[id] = {'Text': Text,
                                    'combo_status': combo_status,
                                    'patient_note': note}
        self.ui.patient_comboBox.addItem(id)
        self.ui.patient_comboBox.setCurrentText(id)
        self.ui.patient_comboBox.view().setDragDropMode(Qt.QAbstractItemView.NoDragDrop)
        return

    def save_patient(self, id):
        if not id:
            return
        combo_status = {}
        Text = self.ui.textEdit.toPlainText()
        note = self.mynote.mynote.textEdit.toPlainText()
        for combo in self.ui.tabWidget.findChildren(QtWidgets.QComboBox):
            combo_status[combo.objectName()] = combo.currentIndex()
        self.ui.patient_date[id] = {'Text':Text,
                                    'combo_status':combo_status,
                                    'patient_note': note}
        #print(self.ui.patient_date)

        return

    def patient_changed(self, index):
        if index == '':
            return
        current_id = self.mytitle_id.to_current_id()
        if current_id:
            self.save_patient(current_id)
        id = self.ui.patient_comboBox.itemText(index)
        if id in self.ui.patient_date.keys():
            self.ui.textEdit.setPlainText(self.ui.patient_date[id]['Text'])
            self.mynote.mynote.textEdit.setPlainText(self.ui.patient_date[id]['patient_note'])
            self.mynote.setWindowTitle(id)

            for combo in self.ui.tabWidget.findChildren(QtWidgets.QComboBox):
                combo.setCurrentIndex(self.ui.patient_date[id]['combo_status'][combo.objectName()])

            self.ui.patient_id.setText(id)
            self.mytitle_id.set_current_id(id)

        return

    def insert_keyword(self, date):
        print(date)
        return

    def tabchange(self, index):
        if not index in self.datebase.tab_tree_connect:
            return
        elif not self.datebase.tab_tree_connect[index]:
            return
        self.ui.treeWidget.collapseAll()
        for obj in self.ui.treeWidget.findItems('Common',QtCore.Qt.MatchExactly|QtCore.Qt.MatchRecursive,0):
            obj.setExpanded(True)
        for obj in self.ui.treeWidget.findItems(self.datebase.tab_tree_connect[index],QtCore.Qt.MatchExactly|QtCore.Qt.MatchRecursive,0):
            if obj:
                obj.setExpanded(True)
            self.ui.treeWidget.scrollToItem(obj, QtWidgets.QAbstractItemView.PositionAtTop)

        current_id = self.ui.patient_comboBox.currentText()
        if current_id == self.ui.patient_id.text():
            self.save_patient(current_id)

        return

    def double_clicked(self):
        sent = self.ui.listWidget.currentItem().Text()
        if re.match('(.+)', sent):
            sent = re.sub('(.+)','',sent,1)
        mydia = MyDialog(myapp, sent)
        if mydia.exec_():
            sent = mydia.getInputs()
            self.ui.listWidget.currentItem().setText(sent)
        check_status = []

        return

    def input(self, item, column):

        def _insert_position(sent):
            if not sent:
                return sent
            text = self.ui.textEdit.textCursor().block().text()
            pos = self.ui.textEdit.textCursor().positionInBlock()
            #if text:
            #    if pos < len(text):
            #        self.ui.textEdit.moveCursor(QtGui.QTextCursor.EndOfBlock)
            #        if not text[-1] == ' ':
            #            if text[-1] == '.':
            #                sent = sent.strip()
            #                sent = sent[0].upper() + sent[1:]
            #                sent = ' '+ sent
            #            else:
            #                sent = ' ' + sent
            #        else:
            #            if text.strip()[-1] == '.':
            #                sent = sent.strip()
            #                sent = sent[0].upper() + sent[1:]
            if not text:
                sent = sent[0].upper() + sent[1:]

            return sent

        def _to_conclusion(sent):
            if 'conclusion' in self.ui.textEdit.toPlainText().lower():
                self.ui.textEdit.append(sent)
            else:
                self.ui.textEdit.append('CONCLUSIONS-----------------------------')
                self.ui.textEdit.append(sent)

        if item.columnCount() < 2:
            return

        if not item.parent():
            return

        sent = item.text(4)
        text = self.ui.textEdit.textCursor().block().text()
        if re.match('\([^\s]+\)', sent):
            sent = re.sub('\([^\s]+\)','',sent,1)

        print(sent)
        if re.search('\S\d?\{.+?\}|\S\d?\[.*?\]', sent):
            print('get key word')
            self.ui.selecter = MySelecter(myapp, sent)
            if self.ui.selecter.exec_():
                sent, conclusion = self.ui.selecter.get_sent()
                self.ui.textEdit.insertPlainText(_insert_position(sent))
                if conclusion:
                    _to_conclusion(conclusion)
        else:
            self.ui.textEdit.insertPlainText(_insert_position(sent))

        #self.ui.textEdit.append(sent.strip())
        self.ui.textEdit.setFocus()

        return

    def test(self):

        def _deal_with_autokey():
            getSelected = myautokeyin.autokeyin.antukeytree.selectedItems()

            if getSelected:
                selected_list = []
                Text = ''
                for i in range(len(getSelected)):
                    if getSelected[i].text(0) == 'left' or getSelected[i].text(0) == 'right':
                        selected_list.append(getSelected[i].text(0) + ' ' + getSelected[i].parent().text(0))
                    else:
                        selected_list.append(getSelected[i].text(0))
                if len(selected_list) == 1:
                    Text = selected_list[0]
                elif len(selected_list) == 2:
                    Text = selected_list[0] + ' and ' + list[1]
                elif len(selected_list) > 2:
                    Text = ', '.join(list[:len(selected_list) - 2]) + ' and ' + selected_list[-1]
                    Text = Text.strip().lower()
                self.ui.clipboard.setText(Text)
                myautokeyin.close()

            return


        def _itemisExpanded(theitem):
            theitem.setFlags(theitem.flags() ^ QtCore.Qt.ItemIsSelectable)
            return

        myautokeyin = MyautokeyinForm(myapp)
        myautokeyin.show()
        #myautokeyin.autokeyin.antukeytree.setColumnCount(1)
        myautokeyin.autokeyin.antukeytree.setHeaderLabels(['分類'])
        myautokeyin.autokeyin.antokey_Button.clicked.connect(_deal_with_autokey)
        myautokeyin.autokeyin.antukeytree.itemExpanded.connect(_itemisExpanded)

        for category in lymphnodes.keys():
            category_autokey_root = QtWidgets.QTreeWidgetItem(myautokeyin.autokeyin.antukeytree)
            category_autokey_root.setText(0, category)
            category_autokey_root.setFlags(category_autokey_root.flags() ^ QtCore.Qt.ItemIsSelectable)
            for subgroup in lymphnodes[category].keys():
                category_autokey_subgroup = QtWidgets.QTreeWidgetItem(category_autokey_root)
                category_autokey_subgroup.setText(0, subgroup)
                category_autokey_subgroup.setFlags(category_autokey_subgroup.flags() ^ QtCore.Qt.ItemIsSelectable)
                for i in range(len(lymphnodes[category][subgroup])):
                    child = QtWidgets.QTreeWidgetItem(category_autokey_subgroup)
                    child.setText(0, lymphnodes[category][subgroup][i])
                    child_left = QtWidgets.QTreeWidgetItem(child)
                    child_left.setText(0, 'left')
                    child_right = QtWidgets.QTreeWidgetItem(child)
                    child_right.setText(0, 'right')
        return

    def clearer(self, reply=''):
        if not reply:
            reply = QtWidgets.QMessageBox.question(self, 'Asking', 'Are you sure?', QtWidgets.QMessageBox.Yes| QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes or reply == 'yes':
            for combo in self.ui.tabWidget.findChildren(QtWidgets.QComboBox):
                combo.setCurrentIndex(0)
            self.ui.tabWidget.setCurrentIndex(0)
            self.ui.textEdit.clear()
            self.ui.treeWidget.collapseAll()
            self.mynote.mynote.textEdit.clear()
            for obj in self.ui.treeWidget.findItems(self.datebase.tab_tree_connect[0],
                                                    QtCore.Qt.MatchExactly | QtCore.Qt.MatchRecursive, 0):
                if obj:
                    obj.setExpanded(True)

        return

    def combo_changed(self, index):
        sender = self.sender()
        tabname = sender.objectName().replace('combo_','')
        tabstatus = ['', '-', '+', '#']
        self.ui.tabWidget.setTabText(self.datebase.tabname_list.index(tabname), tabstatus[index] + tabname)

        return

    def take(self):
        #print(self.process_exists('clipmanger.exe'))
        n = 0
        Text = ''

        # CHecking Seeting
        has_number = self.datebase.check_seeting('Adding line number when sending')
        with_ahk = self.datebase.check_seeting('Send report by AHK')
        ask_checklist = self.datebase.check_seeting('Ask checklist')
        #if not self.ui.line_number_checkBox.isChecked():
        #    self.ui.clipboard.setText(self.ui.textEdit.toPlainText())
        #    return
        All_checked = True
        if ask_checklist:
            for combo in self.ui.tabWidget.findChildren(QtWidgets.QComboBox):
                if not combo.currentIndex():
                    All_checked = False
                    break

        if not All_checked: # and not self.ui.Not_Ask_checkBox.isChecked()
            reply = QtWidgets.QMessageBox.warning(self, 'Not all checked', 'Are you sure?',
                                                  QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            if reply == QtWidgets.QMessageBox.No:
                return
        Text = self.ui.textEdit.toPlainText()
        n = 1
        History_temp = []
        Finding_temp = []
        Conclusion_temp = []
        #with_ahk = self.ui.byAHK_checkBox.isChecked()

        if with_ahk:
            with_ahk = self.process_exists('clipmanger.exe')
        Temp = ''
        n = 1
        in_conclusion = False

        for sent in Text.splitlines():
            if 'conclusion' in sent.lower():
                in_conclusion = True
                n = 1
                if with_ahk:
                    continue
                else:
                    Conclusion_temp.append(sent)
            elif not in_conclusion:
                if sent and has_number:
                    sent = str(n) + '. ' + sent.strip()
                    n = n + 1
                    Finding_temp.append(sent)
                elif not has_number:
                    Finding_temp.append(sent)

            elif in_conclusion:
                if sent and has_number:
                    sent = str(n) + '. ' + sent.strip()
                    n = n + 1
                    Conclusion_temp.append(sent)
                elif not has_number:
                    Conclusion_temp.append(sent)

        #print(Finding_temp, Conclusion_temp)
        if with_ahk:
            if Conclusion_temp:
                Temp = linesep.join(Conclusion_temp)
                #print(Temp)
                win32clipboard.OpenClipboard()
                win32clipboard.EmptyClipboard()
                win32clipboard.SetClipboardText(Temp)
                win32clipboard.CloseClipboard()
                #self.ui.clipboard.clear(mode=self.ui.clipboard.Clipboard)
                #self.ui.clipboard.setText(Temp)
                time.sleep(1)

            if Finding_temp:
                Temp = linesep.join(Finding_temp)
                #print(Temp)
                win32clipboard.OpenClipboard()
                win32clipboard.EmptyClipboard()
                win32clipboard.SetClipboardText(Temp)
                win32clipboard.CloseClipboard()
                #self.ui.clipboard.clear(mode=self.ui.clipboard.Clipboard)
                #self.ui.clipboard.setText(Temp, mode=self.ui.clipboard.Clipboard)
                time.sleep(1)

            if History_temp:
                Temp = linesep.join(History_temp)
                #print(Temp)
                win32clipboard.OpenClipboard()
                win32clipboard.EmptyClipboard()
                win32clipboard.SetClipboardText(Temp)
                win32clipboard.CloseClipboard()
                #self.ui.clipboard.clear(mode=self.ui.clipboard.Clipboard)
                #self.ui.clipboard.setText(Temp, mode=self.ui.clipboard.Clipboard)
                time.sleep(1)
        else:
            Temp = linesep.join(Finding_temp + Conclusion_temp)
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardText(Temp)
            win32clipboard.CloseClipboard()

        return

    def minput(self, edit_text=''):
        mydia = MyDialog(myapp, edit_text)
        if mydia.exec_():
            Text = mydia.getInputs()
            #self.ui.listWidget.addItem(Text)

        return

    def clean_patient(self):


        return

    def process_exists(self, processName):
        for proc in psutil.process_iter():
            try:
                # Check if process name contains the given name string.
                if processName.lower() in proc.name().lower():
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return False


if __name__ == '__main__':

    def __to_quit():

        if not path.isfile('temp.json'):
            return
        try:
            remove('temp.json')
        except OSError as e:
            print(e)
        else:
            print("Temp File is deleted successfully")

        return

    #myKeywords = []

    # ------------- old segment for read myKeywords -----------------
    #try:
    #    f = open('./setting/autocompwords.txt', 'r', encoding='utf-8-sig')
    #except UnicodeDecodeError:
    #    f = open('./setting/autocompwords.txt', 'r', encoding='cp950')
    #while True:
    #    t = f.readline()
    #    if t == '': break
    #    if t.strip():
    #        if not t.strip() in myKeywords:
    #            myKeywords.append(t.strip())

    template_keypair = {}
    seeting_path = './setting'
    temp_file_path = './setting/template'
    # template_path = seeting_path + '/template.xlsx'

    lymphnodes = {}
    category = ''
    subgroup = ''
    temp_category = {}
    temp = []
    try:
        f = open('./setting/keywords/lymphnodes.txt', 'r', encoding='utf-8-sig')
    except UnicodeDecodeError:
        f = open('./setting/keywords/lymphnodes.txt', 'r', encoding='cp950')
    while True:
        t = f.readline()
        if t == '':
            temp_category[subgroup] = temp
            lymphnodes[category] = temp_category
            break
        if '{' in  t and '}' in t:
            if temp_category and category:
                lymphnodes[category] = temp_category
                temp_category = {}
            category = t.split('{',1)[1].split('}',1)[0].strip()
        elif '[' in t and ']' in t:
            if temp and subgroup:
                temp_category[subgroup] = temp
                temp = []
            subgroup = t.split('[',1)[1].split(']',1)[0].strip()
        else:
            temp.append(t.strip())

    app = QtWidgets.QApplication(sys.argv)
    screen_resolution = app.desktop().screenGeometry()
    app.aboutToQuit.connect(__to_quit)
    myapp = MyWin()
    myapp.show()
    sys.exit(app.exec_())

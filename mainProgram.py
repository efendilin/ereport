

import sys
import win32clipboard
import win32con
import re
import ereport
import pandas as pd
import datetime

from RepSearch import MyRQS_Searcher
from nmainUI import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from os import linesep

class MyForm(QtWidgets.QMainWindow):
    pass


class Worker(QtCore.QThread):
    statue = QtCore.pyqtSignal(int, str)
    date = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.rqs_connect = MyRQS_Searcher() #proxy = '10.1.12.163:8888'
        self.pid = ''
        self.tabbyrepkind = {}
        self.tabbykeyword = {}
        self.results = {}
        self.pdate = {}
        self.notother = []

        return

    def run(self):
        print('start working')
        others_done = False
        if not self.pid:
            return
        self.results = {}
        self.pdate = {}
        self.pdate['name'] = ''
        self.pdate['sex'] = ''
        others_temp = []
        num_temp = []
        for tabname in self.tabbyrepkind.keys():
            print('start', tabname)
            dpkind = self.tabbyrepkind[tabname][0]
            dpDate = self.tabbyrepkind[tabname][2]
            tabtext = self.tabbyrepkind[tabname][3]
            result_temp = []
            replinks = self.rqs_connect.getlistquary(pid=self.pid, dpDate=dpDate, dpKind=dpkind)
            if not replinks:
                continue
            for replink in replinks:
                link = replink['replink']
                results = self.rqs_connect.getdatabylink(link)
                #Debug print('result:', results)
                if not 'result' in results:
                    continue
                if 'name' in results and not self.pdate['name']:
                    self.pdate['name'] = results['name']
                if 'sex' in results and not self.pdate['sex']:
                    self.pdate['sex'] = results['sex']
                result_temp.append(results['result'])
            self.results[tabname] = result_temp
        #Debug print('by repkind done')
            # search by key word
        keyword = {}
        for tabname in self.tabbykeyword.keys():
            keyword[self.tabbykeyword[tabname][1]] = tabname
            self.results[tabname] = []
        
        dpkind = '所有檢查單'
        dpDate = '二年內'
        result_temp = []
        print('others before ask links')
        replinks = self.rqs_connect.getlistquary(pid=self.pid, dpDate=dpDate, dpKind=dpkind)
        if not replinks:
            return
        print('get links')
        for replink in replinks:
            if replink['repkind'] in keyword.keys():
                #Debug print('start by keyword')
                links = replink['replink']
                results = self.rqs_connect.getdatabylink(links)
                if not 'result' in results:
                    continue
                self.results[keyword[replink['repkind']]].append(results['result'])
            elif not replink['repkind'] in notothers:
                print('start other')
                links = replink['replink']
                print(links)
                results = self.rqs_connect.getdatabylink(links)
                print('get from', links)
                if not 'result' in results:
                    continue
                others_temp.append(results['result'])

        if others_temp:
            self.results['othersrep'] = others_temp.copy()

        if results['name'] and not self.pdate['name']:
            self.pdate['name'] = results['name']
        if results['sex'] and not self.pdate['sex']:
            self.pdate['sex'] = results['sex']
        print('work done')
        self.date.emit()

        return

class MyHighlighter( QtGui.QSyntaxHighlighter ):

    def __init__(self, parent):
        QtGui.QSyntaxHighlighter.__init__(self, parent)
        self.parent = parent
        self.highlightingRules = []

        keyword = Qt.QTextCharFormat()
        #keyword.setBackground(QtGui.QColor('darkYellow'))
        keyword.setBackground(QtGui.QColor(255, 229, 25))
        keyword.setFontWeight(Qt.QFont.Bold)

        warmword = Qt.QTextCharFormat()
        warmword.setForeground(QtGui.QColor(255, 85, 0))
        warmword.setFontWeight(Qt.QFont.Bold)

        malword = Qt.QTextCharFormat()
        malword.setForeground(QtGui.QColor(255, 0, 0))
        malword.setFontWeight(Qt.QFont.Bold)

        keywords = ["Diagnosis", "Brains:", "Whole Body:", "CONCLUSIONS", "Impression：", "Comment :"]
        warmwords = ['Fatty liver', 'Polyp', 'Polyps', 'cyst', 'cysts', 'stone', 'stones', 'adenoma', 'polyp']
        malwords = ['cancer', 'malignancy', 'malignant','carcinoma', 'adenocarcinoma', 'sacroma', 'lymphoma', 'metastastic']

        for word in keywords:
            pattern = Qt.QRegExp("\\b" + word)
            self.highlightingRules.append((pattern, keyword))

        for word in warmwords:
            pattern = Qt.QRegExp("\\b" + word + "\\b")
            self.highlightingRules.append((pattern, warmword))

        for word in malwords:
            pattern = Qt.QRegExp("\\b" + word + "\\b")
            self.highlightingRules.append((pattern, malword))

        self.highlightingRules.append((Qt.QRegExp("\\b^[0-9]{1,2}.\s\\b"), keyword))
        return

    def highlightBlock(self, text):
        if text:
            for pattern, keyword in self.highlightingRules:
                i = pattern.indexIn(text, 0)
                while i >= 0:
                    length = pattern.matchedLength()
                    self.setFormat(i, length, keyword)
                    i = pattern.indexIn(text, i + length)
        return


class MyWin(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.pid = ''
        self.work = Worker()
        self.work.date.connect(self.date_procress)
        #self.work.statue.connect(worker_status)
        self.ui.tabEReport.setCurrentIndex(0)

        self.save_date = {}

        #nmohighlight = MyHighlighter(self.ui.nmreps)
        #pathhighlight = MyHighlighter(self.ui.pathreps)
        #radhighlight = MyHighlighter(self.ui.radiorep)
        #scopyhighlight = MyHighlighter(self.ui.scopyrep)
        #othhighlight = MyHighlighter(self.ui.othersrep)

        self.ui.search.clicked.connect(self.searchF)
        self.ui.saveOnly.clicked.connect(self.run_worker)
        self.ui.patient_list.currentTextChanged.connect(self.list_changed)

    def datechanger(self, thedate):
        if not re.match('\d+',thedate):
            bcdate = datetime.datetime(1992, 9, 2)
            print(bcdate)
            return bcdate
        if len(thedate) == 7:
            bcdate = datetime.datetime((int(thedate[:3]) + 1911), int(thedate[3:5]), int(thedate[5:7]))
        elif len(thedate) == 8:
            bcdate = datetime.datetime((int(thedate[:4])), int(thedate[4:6]), int(thedate[6:8]))
        else:
            bcdate = datetime.datetime(1992,9,2)
        print(bcdate)
        return bcdate

    def date_procress(self, pid=''):
        #Debug print(self.work.results)

        def _remove_html(value):
            if 'DarkRed' in value:
                color = 'DarkRed'
                value = re.sub('<span style="font-weight:800; color:(Red|DarkRed)">', '', value).replace('</span>',
                                                                                                         '').strip()
            elif 'Red' in value:
                color = 'Red'
                value = re.sub('<span style="font-weight:800; color:Red" >', '', value).replace('</span>',
                                                                                                         '').strip()
            elif 'Blue' in value:
                color = 'Blue'
                value = re.sub('<span style="font-weight:800; color:Blue" >', '', value).replace('</span>', '').strip()
            else:
                value = re.sub('<span style="font-weight:800" >', '', value).replace('</span>', '').strip()
                color = ''
            return value, color


        for obj in self.ui.tabEReport.findChildren(QtWidgets.QTreeWidget):
            obj.clear()
        if not pid:
            result = self.work.results
            self.save_date[self.pid] = self.work.results.copy()
        else:
            result = self.save_date[pid]
            self.pid = pid
        save_temp = {}
        nums_column = {}
        rep_date_list = []
        rep_kind_list = []
        sub_kind_list = []
        name_list = []
        value_list = []
        color_list = []
        unit_list = []
        lowref_list = []
        highref_list = []
        HiLo_list = []

        for tabname in result:
            if result[tabname]:
                print('for :' + tabname)
                for reports in result[tabname]:
                    for report in reports:
                        if 'text' in report:
                            if not report['text']:
                                continue
                            for obj in self.ui.tabEReport.findChildren(QtWidgets.QTreeWidget, tabname):
                                if obj.objectName() == tabname:
                                    print('for text in' + tabname)
                                    rep_root = QtWidgets.QTreeWidgetItem(obj)
                                    rep_date = self.datechanger(report['repdate']).strftime("%Y/%m/%d")
                                    rep_root.setText(0, '{} on {} by {} at {}歲'.format(report['repkind'],rep_date,report['drname'],report['age']))
                                    child = QtWidgets.QTreeWidgetItem(rep_root)
                                    text_widget = QtWidgets.QTextEdit()
                                    text_hilight = MyHighlighter(text_widget)
                                    text_widget.append(report['text'])
                                    obj.setItemWidget(child, 0, text_widget)
                                    print('finish text in ' + tabname)
                                    break

                        elif 'nums' in report:
                            print('for nums in ' + tabname)
                            date = self.datechanger(report['repdate'])
                            repkind = report['repkind'].strip()
                            row = len(report['nums']) - 1
                            temp_sub_kind = ''
                            for r in range(row):
                                color = ''
                                if '**********' in report['nums'][r + 1][1]:
                                    temp_sub_kind = report['nums'][r + 1][0].strip()
                                    continue
                                rep_date_list.append(date)
                                rep_kind_list.append(repkind)
                                sub_kind_list.append(temp_sub_kind)
                                name_list.append(report['nums'][r + 1][0].strip())
                                value, color = _remove_html(report['nums'][r + 1][1])
                                value_list.append(value)
                                color_list.append(color)
                                unit_list.append(report['nums'][r + 1][2].strip())
                                lowref_list.append(report['nums'][r + 1][3].strip())
                                highref_list.append(report['nums'][r + 1][4].strip())
                                HiLo, co = _remove_html(report['nums'][r + 1][5].strip())
                                HiLo_list.append(HiLo)
                            print('finish nums in ' + tabname)


        nums_column = {'rep_date':rep_date_list,
                       'rep_kind':rep_kind_list,
                       'sub_kind':sub_kind_list,
                       'name':name_list,
                       'value':value_list,
                       'color':color_list,
                       'unit':unit_list,
                       'lowref':lowref_list,
                       'highref':highref_list,
                       'HiLo':HiLo_list
                       }

        print(nums_column)
        num_df = pd.DataFrame(nums_column)
        print('put on nums')


        for kindname, group in num_df.groupby(by = 'rep_kind'):
            rep_root = QtWidgets.QTreeWidgetItem(self.ui.numrep)
            rep_root.setText(0, kindname)
            group = group.sort_values(by = 'rep_date', ascending=False)
            for subkind, sub_group in group.groupby(by='sub_kind'):
                if subkind:
                    sub_kind = QtWidgets.QTreeWidgetItem(rep_root)
                    sub_kind.setText(0, subkind)
                for repname, name_group in group.groupby(by='name'):
                    if subkind:
                        name_child = QtWidgets.QTreeWidgetItem(sub_kind)
                    else:
                        name_child = QtWidgets.QTreeWidgetItem(rep_root)
                    #max_index = name_group['rep_date'].idxmax()
                    #print(name_group)
                    #temp_date = name_group.iloc[max_index]['rep_date']

                    #temp_color = name_group.iloc[max_index]['color']
                    #name_with_value = '{}: {} {} normal range:[{} - {}] on {}'.format(repname,
                    #                                                                  name_group.iloc[max_index]['value'],
                    #                                                                  name_group.iloc[max_index]['unit'],
                    #                                                                  name_group.iloc[max_index]['lowref'],
                    #                                                                  name_group.iloc[max_index]['highref'],
                    #                                                                  temp_date)
                    #print(name_with_value)
                    #if name_with_value:
                    #    name_child.setText(0, name_with_value)
                    #    if temp_color:
                    #        name_child.setForeground(0, QtGui.QBrush(QtGui.QColor(dic['color'][row])))
                    #else:
                    name_child.setText(0, repname)
                    dic = name_group.set_index('name').to_dict('list')
                    for row in range(len(dic['rep_date'])):
                        child = QtWidgets.QTreeWidgetItem(name_child)
                        child.setText(0, '{}:  {}  ({})'.format(dic['rep_date'][row].strftime("%Y/%m/%d"),dic['value'][row],dic['unit'][row]))
                        if dic['color'][row]:
                            child.setForeground(0, QtGui.QBrush(QtGui.QColor(dic['color'][row])))



            #for date, each_date in group.groupby(by = 'rep_date'):
            #    sub_child = QtWidgets.QTreeWidgetItem(rep_root)
            #    sub_child.setText(0, date.strftime("%Y/%m/%d"))
            #    for subkind, subkind_date in each_date.groupby(by='sub_kind'):
            #        if subkind:
            #            sub_kind = QtWidgets.QTreeWidgetItem(sub_child)
            #            sub_kind.setText(0, subkind)
            #            dic = subkind_date.set_index('rep_date').to_dict('list')
            #            for row in range(len(dic['name'])):
            #                child = QtWidgets.QTreeWidgetItem(sub_kind)
            #                child.setText(0, '{}   {}   ({})'.format(dic['name'][row],dic['value'][row],dic['unit'][row]))
            #                if dic['color'][row]:
            #                    child.setForeground(0,QtGui.QBrush(QtGui.QColor(dic['color'][row])))
            #                child.setWhatsThis(0, 'test')
            #        else:
            #            dic = subkind_date.set_index('rep_date').to_dict('list')
            #            for row in range(len(dic['name'])):
            #                child = QtWidgets.QTreeWidgetItem(sub_child)
            #                child.setText(0, '{}   {}   ({})'.format(dic['name'][row],dic['value'][row],dic['unit'][row]))
            #                if dic['color'][row]:
            #                    child.setForeground(0,QtGui.QBrush(QtGui.QColor(dic['color'][row])))
            #                child.setWhatsThis(0, 'test')

        self.ui.numrep.sortItems(0,QtCore.Qt.DescendingOrder)


        index = self.ui.patient_list.findText(self.pid, QtCore.Qt.MatchContains)
        if index == -1:
            pdate = "{}[{}][{}]".format(self.pid, self.work.pdate['name'], self.work.pdate['sex'])
            self.ui.patient_list.addItem(pdate)
            self.ui.pName.setText(pdate)
            self.ui.patient_list.setCurrentText(pdate)
        else:
            self.ui.patient_list.setCurrentIndex(index)
            self.ui.pName.setText(self.ui.patient_list.currentText())
        self.ui.pID.clear()


        return
    def list_changed(self, pdate):
        pid = pdate.split('[',1)[0]
        if pid == self.pid:
            return
        if not pid in self.save_date:
            return
        self.date_procress(pid)

        return

    def searchF(self):
        self.pid = self.ui.pID.text().strip()
        if not self.pid:
            self.statusBar().showMessage("No ID input!!!!!!")
            return
        self.work.pid = self.pid
        self.work.tabbyrepkind = tabbyrepkind.copy()
        self.work.tabbykeyword = tabbykeyword.copy()
        self.work.notother = notothers
        self.work.start()

        return

    def run_worker(self):

        self.work.start()
        return


if __name__ == '__main__':
    tabbyrepkind = {'nmreps':['741 核子醫學檢查','','不限日期','NM',0],'pathreps':['459 病理組織及細胞檢驗','','不限日期','病理',0],'radiorep':['742 放射診斷科','','二年內','放射',0]}
    tabbykeyword = {'scopyrep':['others','內視鏡','二年內','內視鏡',0]}
    notothers = ['核醫','病理細胞','放射科','內視鏡']


    app = QtWidgets.QApplication(sys.argv)
    clipboard = QtWidgets.QApplication.clipboard()
    myapp = MyWin()
    myapp.show()
    sys.exit(app.exec_())
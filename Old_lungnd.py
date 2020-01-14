

class QLineNumberArea(QtWidgets.QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.codeEditor = editor

    def sizeHint(self):
        return QSize(self.editor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.codeEditor.lineNumberAreaPaintEvent(event)


class OldTextEdit(QtWidgets.QPlainTextEdit):
    shortcut = QtCore.pyqtSignal(str)
    def __init__(self, *args, **kwargs):
        super(OldTextEdit, self).__init__(*args, **kwargs)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.__contextMenu)
        self.lineNumberArea = QLineNumberArea(self)
        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)
        self.updateLineNumberAreaWidth(0)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setBold(False)
        font.setWeight(50)
        self.setFont(font)
        self.lung_nodules = []
        self.completer = None

        return

    def lineNumberAreaWidth(self):
        digits = 1
        max_value = max(1, self.blockCount())
        while max_value >= 10:
            max_value /= 10
            digits += 1
        space = 3 + self.fontMetrics().width('9') * digits
        return space

    def updateLineNumberAreaWidth(self, _):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QtCore.QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))

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

    def lineNumberAreaPaintEvent(self, event):
        painter = QtGui.QPainter(self.lineNumberArea)

        painter.fillRect(event.rect(), QtCore.Qt.lightGray)

        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        # Just to make sure I use the right font
        height = self.fontMetrics().height()
        while block.isValid() and (top <= event.rect().bottom()):
            if block.isVisible() and (bottom >= event.rect().top()):
                number = str(blockNumber + 1)
                painter.setPen(QtCore.Qt.black)
                painter.drawText(0, top, self.lineNumberArea.width(), height, QtCore.Qt.AlignRight, number)

            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            blockNumber += 1

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
        tc.select(QtGui.QTextCursor.WordUnderCursor)
        return tc.selectedText()

    def focusInEvent(self, event):
        if self.completer:
            self.completer.setWidget(self)
        QtWidgets.QPlainTextEdit.focusInEvent(self, event)
        return

    def keyPressEvent(self, event):
        if not self.textUnderCursor():
            QtWidgets.QPlainTextEdit.keyPressEvent(self, event)
            if self.completer and self.completer.popup() and self.completer.popup().isVisible():
                self.completer.popup().hide()
            return
        if self.completer and self.completer.popup() and self.completer.popup().isVisible():
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
        isShortcut = (event.modifiers() == QtCore.Qt.ControlModifier and event.key() == QtCore.Qt.Key_Down)
        iskeyShutcut = (event.key() == QtCore.Qt.Key_Backslash)
        inline = (event.modifiers() == QtCore.Qt.ControlModifier and event.key() == QtCore.Qt.Key_Right)
            # if inline completion has been chosen

        if iskeyShutcut:
            self.shortcut.emit(self.textUnderCursor())

            return


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
            QtWidgets.QPlainTextEdit.keyPressEvent(self, event)
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
        menu.addAction('Lung nodule', self.new_lung_nodule)
        menu.addAction('Measurement', self.measurement)

        return

    def new_lung_nodule(self):
        lung_nodule = Mylung_nodules(myapp)
        lung_nodule.show()

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
        lndmenu = submenu.addAction('Lung nodule', self.new_lung_nodule)
        mesmenu = submenu.addAction('Measurement', self.measurement)

        submenu.exec_(QtGui.QCursor.pos())

    def insert_text(self, Text):
        self.insertPlainText(Text)
        return


def lung_nodule(self, short=False):
    def _combined_and(temp=[], short=False):
        print(temp)
        num = len(temp)
        if num > 2:
            Text = ', '.join(temp[:num - 1]) + ' and ' + temp[-1]
        elif num == 2:
            Text = temp[0] + ' and ' + temp[1]
        else:
            Text = temp[0]
        return Text

    def _send_nodules():
        cal = {}
        temp = {}
        for nodule in self.lung_nodules:
            if nodule['fdg']:
                self.insert_text(_output_nodules(nodule))
                continue
            elif not nodule['pre'] and not nodule['post'] and not nodule['preloc'] and nodule['cal']:
                for location in nodule['location']:
                    cal[location] = []
                    cal[location].append(nodule)
                continue
            else:
                for location in nodule['location']:
                    temp[location] = []
                    temp[location].append(nodule)
        if cal:
            nd_size = []
            nd_location = []
            nd_cal = []
            num = 0
            nd_text = ' nodule'
            for location in cal.keys():
                num = num + len(cal[location])
                for nodule in cal[location]:
                    if nd_size:
                        nd_size = [i for i in nd_cal if i in nodule['size']]
                    else:
                        nd_size = nodule['size']
                    if nd_cal:
                        nd_cal = [i for i in nd_cal if i in nodule['cal']]
                    else:
                        nd_cal = nodule['cal']
                nd_location.append(location)
            if num > 1:
                nd_text = nd_text + 's'
            if num <= len(number_pair) and num > 0:
                num_text = number_pair[num]
            else:
                num_text = 'several'
            Text = num_text + ' ' + ' '.join(nd_cal) + ' ' + ' '.join(nd_size) + nd_text + ' in the ' + _combined_and(
                nd_location)
            print(Text)
        if temp:
            combine = True
            for location in temp.keys():
                nd_cal = []
                nd_size = []
                num = len(temp[location])
                nd_cal = temp[location][0]['cal']
                nd_size = temp[location][0]['size']
                if num > 1:
                    for i in range(num - 1):
                        for key in check_list:
                            if not temp[location][0][key] == temp[location][i + 1][key]:
                                combine = False
                                break
                        if not combine:
                            break
                        if combine:
                            nd_cal = [i for i in nd_cal if i in temp[location][i + 1]['cal']]
                            nd_size = [i for i in nd_cal if i in temp[location][i + 1]['size']]
                    if num < 5 and num > 0:
                        num_text = number_pair[num]
                    else:
                        num_text = 'several'
                    Text = num_text + ' ' + ' '.join(temp[location][0]['pre']) + ' ' \
                           + ' '.join(temp[location][0]['pre']) + ' '.join(temp[location][0]['cal'])
                    Text = Text + ' with ' + temp[location][0]['post']
                    Text = Text + ' nodule in the ' + location
                    print(Text)
                else:
                    for nodule in temp[location]:
                        Text = _output_nodules(nodule)
                        Text = 'a ' + Text
                        print(Text)

        return

    def _list_changed(index):
        if index == 0:
            myautokeyin.autokeyin.add_nodule.setText('add nodule')
            return
        myautokeyin.autokeyin.add_nodule.setText('change nodule')
        temp = self.lung_nodules[index - 1]
        for cat in temp.keys():
            for key in temp[cat]:
                print(key)
                for item in myautokeyin.autokeyin.antukeytree.findItems(key,
                                                                        QtCore.Qt.MatchExactly | QtCore.Qt.MatchRecursive,
                                                                        0):
                    item.parent().setExpanded(True)
                    item.setSelected(True)
        for para in temp['para'].keys():
            for obj in myautokeyin.autokeyin.antukeytree.findChildren(QtWidgets.QLineEdit, para):
                obj.setText(temp['para'][para])

        return

    def _output_nodules(temp, short=False):
        para_temp = []
        para_text = ''
        Text = ''
        unit = 'cm'  # 預設單位 = cm
        for obj in myautokeyin.findChildren(QtWidgets.QRadioButton):  # 決定單位
            if obj.isChecked():
                unit = obj.text()
        for para in temp['para'].keys():
            if temp['para'][para]:
                if para == 'size:':
                    para_temp.append(para + temp['para'][para] + unit)
                else:
                    para_temp.append(para + temp['para'][para])
        if para_temp:
            para_text = '(' + ', '.join(para_temp) + ')'
        if short:
            short_location = []
            for location in temp['location']:
                short_location.append(location_short[location])
            Text = ','.join(short_location) + para_text
            return Text

        if temp['size']:
            Text = ' '.join(temp['size']) + ' '
        if temp['cal']:
            Text = Text + ' '.join(temp['cal'])
        if temp['pre']:
            Text = Text + ' '.join(temp['pre']) + ' '
        Text = Text + 'nodule'
        if temp['fdg']:
            Text = Text + ' with ' + ' to '.join(temp['fdg']) + ' FDG uptake'
            if temp['post']:
                Text = Text + ', ' + ', '.join(temp['post'])
        elif temp['post']:
            Text = Text + ' with ' + ', '.join(temp['post'])
        num = len(temp['location'])
        if num > 1:
            if num > 2:
                Text = Text + ' in the ' + ', '.join(temp['location'][:num - 2]) + ' and ' + temp['location'][:num - 1]
            else:
                Text = Text + ' in the ' + ' and '.join(temp['location'])
        else:
            Text = Text + ' in the ' + temp['location'][0]
        if para_text:
            Text = Text + para_text

        return Text

    def _add_nodule():
        temp = {}
        Text = ''
        for cat in cat_dic.values():
            temp[cat] = []
        getSelected = myautokeyin.autokeyin.antukeytree.selectedItems()
        if getSelected:
            for i in range(len(getSelected)):
                getSelected[i].setSelected(False)
                if getSelected[i].parent().text(0) in cat_dic.keys():
                    temp[cat_dic[getSelected[i].parent().text(0)]].append(getSelected[i].text(0))
        for para in parameter.keys():
            for obj in myautokeyin.autokeyin.antukeytree.findChildren(QtWidgets.QLineEdit, para):
                num = obj.text()
                obj.clear()
                if re.match('\.', num):
                    # print(num)
                    num = '0' + num
                parameter[para] = num
        if not temp['location'] or len(temp['location']) > 1:
            reply = QtWidgets.QMessageBox.warning(self, 'Warning', 'Select "One" location is accepted',
                                                  QtWidgets.QMessageBox.Ok)
            return
        temp['para'] = parameter
        short = _output_nodules(temp, short=True)
        index = myautokeyin.autokeyin.Cate_comboBox.currentIndex()
        if index:
            myautokeyin.autokeyin.Cate_comboBox.setCurrentIndex(0)
            self.lung_nodules[index - 1] = temp
            myautokeyin.autokeyin.Cate_comboBox.setItemText(index, short)
        else:
            self.lung_nodules.append(temp)
            myautokeyin.autokeyin.Cate_comboBox.addItem(short)
        myautokeyin.autokeyin.Cate_comboBox.setCurrentIndex(0)

        myautokeyin.date.emit(_output_nodules(temp))
        # myautokeyin.autokeyin.date.emit(Text + para_text)

        return

    parameter = {}
    lung_nodule_phrase = {}
    cat_dic = {}
    cat = ''
    cat_expend = ['Size', 'location']
    location_short = {'right upper lung': 'RUL',
                      'right middle lung': 'RML',
                      'right lower lung': 'RLL',
                      'left upper lung': 'LUL',
                      'left lower lung': 'LLL'}
    check_list = ['pre', 'cal']
    number_pair = {1: 'a', 2: 'two', 3: 'three', 4: 'four', 5: 'five'}
    myautokeyin = MyautokeyinForm(self)
    myautokeyin.autokeyin.add_nodule.clicked.connect(_add_nodule)
    myautokeyin.autokeyin.antukeytree.setColumnCount(2)
    myautokeyin.autokeyin.antukeytree.setColumnWidth(0, 250)
    myautokeyin.autokeyin.antukeytree.setColumnWidth(1, 50)
    myautokeyin.autokeyin.Cate_comboBox.addItem(' ')
    myautokeyin.date.connect(self.insert_text)
    myautokeyin.autokeyin.Cate_comboBox.currentIndexChanged.connect(_list_changed)
    myautokeyin.autokeyin.antokey_Button.clicked.connect(_send_nodules)
    # lung_nodule
    if self.lung_nodules:
        for nodule in self.lung_nodules:
            short = _output_nodules(nodule, short=True)
            myautokeyin.autokeyin.Cate_comboBox.addItem(short)
    myautokeyin.show()
    with (open('./setting/keywords/lungnodules.txt', 'r', encoding='utf-8-sig')) as f:
        while True:
            t = f.readline()
            t = t.strip()
            if t == '': break
            if '[' in t and ']' in t:
                t = t.replace('[', '').replace(']', '')
                if ':' in t:
                    cat = t.split(':', 1)[0]
                    cat_dic[cat] = t.split(':', 1)[1]
                    lung_nodule_phrase[cat] = []
                else:
                    print('a "[]" line error')
            else:
                if cat:
                    lung_nodule_phrase[cat].append(t)
                else:
                    print('no cat')
    if not lung_nodule_phrase:
        return
    for category in lung_nodule_phrase.keys():
        expend = False
        if category in cat_expend:
            expend = True
        category_autokey_root = QtWidgets.QTreeWidgetItem(myautokeyin.autokeyin.antukeytree)
        category_autokey_root.setText(0, category)
        category_autokey_root.setFlags(category_autokey_root.flags() ^ QtCore.Qt.ItemIsSelectable)
        category_autokey_root.setExpanded(expend)
        for subgroup in lung_nodule_phrase[category]:

            if 'linedit' in subgroup:
                subgroup = subgroup.replace('linedit', '')
                parameter[subgroup] = ''
                child = QtWidgets.QTreeWidgetItem(category_autokey_root)
                child.setText(0, subgroup)
                child.setFlags(child.flags() ^ QtCore.Qt.ItemIsSelectable)
                line_widget = QtWidgets.QLineEdit()
                line_widget.setObjectName(subgroup)
                myautokeyin.autokeyin.antukeytree.setItemWidget(child, 1, line_widget)
            else:
                child = QtWidgets.QTreeWidgetItem(category_autokey_root)
                child.setText(0, subgroup)
                child.setFlags(child.flags() | QtCore.Qt.ItemIsSelectable)
    return
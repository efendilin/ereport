def read_treewidget_data(self):
    count = self.ui.treeWidget.topLevelItemCount()
    for i in range(count):
        item = self.ui.treeWidget.topLevelItem(i)
        child_count = item.childCount()
        for j in range(child_count):
            child_item = item.child(j)
            print(child_item.text(0))

    return


def init_tabwidget(self):
    tab_list = self.tab_structer[self.tab_structer['active'] == True].index.tolist()
    self.tabname_list = []
    tab_index = 0
    self.tab_tree_connect = {}
    combo_list = ["Unchecked", "Normal", "Checked", "Abnormal"]
    for index in tab_list:
        name = self.tab_structer.loc[index].TabName
        self.tabname_list.append(name)
        category = self.tab_structer.loc[index].category
        self.ui.tabWidget.tab_Temp = QtWidgets.QWidget()
        self.ui.tabWidget.tab_Temp.setObjectName(name)
        self.ui.tabWidget.Layout = QtWidgets.QHBoxLayout(self.ui.tabWidget.tab_Temp)
        self.ui.tabWidget.Layout.setObjectName("Layout_" + name)
        self.ui.tabWidget.combo_Temp = QtWidgets.QComboBox(self.ui.tabWidget.tab_Temp)
        self.ui.tabWidget.combo_Temp.setObjectName("combo_" + name)
        self.ui.tabWidget.combo_Temp.addItems(combo_list)
        self.ui.tabWidget.combo_Temp.currentIndexChanged.connect(self.combo_changed)
        self.ui.tabWidget.Layout.addWidget(self.ui.tabWidget.combo_Temp)
        self.ui.tabWidget.Temp_checked = QtWidgets.QPushButton(self.ui.tabWidget.tab_Temp)
        self.ui.tabWidget.Temp_checked.setObjectName("checked_" + name)
        self.ui.tabWidget.Temp_checked.setText("Checked to next  -->")
        self.ui.tabWidget.Temp_checked.clicked.connect(self.checked_to_next)

        self.ui.tabWidget.Layout.addWidget(self.ui.tabWidget.Temp_checked)
        self.ui.tabWidget.addTab(self.ui.tabWidget.tab_Temp, name)
        self.tab_tree_connect[tab_index] = category
        tab_index = tab_index + 1
    self.ui.tabWidget.setCurrentIndex(0)
    return


def init_treewidget(self):
    count = self.ui.treeWidget.topLevelItemCount()
    tree_statue = {}
    if count:
        for i in range(count):
            tree_statue[i] = self.ui.treeWidget.topLevelItem(i).isExpanded()

    self.ui.treeWidget.clear()
    self.category_list = self.datebase.category_list

    for category in self.category_list:
        fliter = (self.fdg_template['category'] == category)
        category_dict = self.fdg_template[fliter].to_dict()
        index_list = list(self.fdg_template[fliter].index)
        category_root = QtWidgets.QTreeWidgetItem(self.ui.treeWidget)
        category_root.setText(0, category)

        for i in index_list:
            child = QtWidgets.QTreeWidgetItem(category_root)
            # child.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsDragEnabled)
            child.setText(0, category_dict['shortcut'][i])
            main_text, isMultrow = self.check_if_multirow(category_dict['main'][i])
            child.setText(1, main_text)
            child.setText(2, str(i))
            child.setText(3, isMultrow)

    if tree_statue:
        for i in tree_statue.keys():
            if tree_statue[i]:
                self.ui.treeWidget.topLevelItem(i).setExpanded(True)
    else:
        self.tabchange(self.ui.tabWidget.currentIndex())

    return


def edit_template(self):
    item = self.ui.treeWidget.currentItem()
    shortcut_values = self.datebase.get_all_shortcut()
    isMultrow = item.text(3).strip()
    index = int(item.text(2).strip())
    if isMultrow == 'True':
        sent = self.fdg_template.loc[index].main
    else:
        sent = ''
    self.ui.editor = Myeditor(myapp, item, self.datebase.category_list, shortcut_values,sent=sent)
    if self.ui.editor.exec_():
        result = self.ui.editor.get_date()
        if result:
            index = item.text(2)
            if self.datebase.edit_by_index(index, result):
                item.setText(0, result['shortcut'])
                main_text, isMultrow = self.check_if_multirow(result['main'])
                item.setText(1, main_text)
                item.setText(3, isMultrow)
                self.shortcut_dict = self.datebase.get_all_shortcut()

        return

    def edit_template(self):
        item = self.ui.treeWidget.currentItem()
        shortcut_values = self.datebase.get_all_shortcut()
        isMultrow = item.text(3).strip()
        index = int(item.text(2).strip())
        if isMultrow == 'True':
            sent = self.fdg_template.loc[index].main
        else:
            sent = ''
        self.ui.editor = Myeditor(myapp, item, self.datebase.category_list, shortcut_values,sent=sent)
        if self.ui.editor.exec_():
            result = self.ui.editor.get_date()
            if result:
                index = item.text(2)
                if self.datebase.edit_by_index(index, result):
                    item.setText(0, result['shortcut'])
                    main_text, isMultrow = self.check_if_multirow(result['main'])
                    item.setText(1, main_text)
                    item.setText(3, isMultrow)
                    self.shortcut_dict = self.datebase.get_all_shortcut()

        return


def add_template(self):
    item = self.ui.treeWidget.currentItem()
    shortcut_values = list(self.fdg_template.shortcut.to_dict().values())
    self.ui.editor = Myeditor(myapp, item, self.datebase.category_list, shortcut_values, mode='a')
    if self.ui.editor.exec_():
        result = self.ui.editor.get_date()
        if result:
            index = item.text(2)
            index_of_parent = item.parent().indexOfChild(item)
            self.datebase.insert_by_index(index, result)

    return

def del_template(self):
    reply = QtWidgets.QMessageBox.warning(self, 'Are you sure?', 'You are going to delete a template. Are you sure?',
                                              QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
    if reply == QtWidgets.QMessageBox.No:
        return
    item = self.ui.treeWidget.currentItem()
    index = item.text(2)
    self.datebase.del_by_index(index)

    return

def insert_template(self, index_of_df, insert_list):
    insertRow = pd.DataFrame([insert_list] ,columns=['category','shortcut','main','active'])
    above = self.fdg_template.loc[:index_of_df]
    below = self.fdg_template.loc[index_of_df+1:]
    self.fdg_template = above.append(insertRow,ignore_index=True).append(below,ignore_index=True)
    self.fdg_template = self.fdg_template.reset_index(drop=True)
    self.shortcut_dict = self.fdg_template.shortcut.to_dict()
    shortcut_list = self.shortcut_dict.values()

    for shortcut in shortcut_list:
        for item in self.ui.treeWidget.findItems(shortcut, QtCore.Qt.MatchExactly | QtCore.Qt.MatchRecursive, 0):
            item.setText(2, str(self.fdg_template[self.fdg_template['shortcut'] == item.text(0)].index.tolist()[0]))

    return True

def del_template_df(self, index):
    self.fdg_template.drop(self.fdg_template.index[[index]], inplace=True)
    self.fdg_template = self.fdg_template.reset_index(drop=True)

def read_template(self):
    self.fdg_template = ''
    with pd.ExcelFile(self.template_path) as xlsx:
        self.fdg_template = pd.read_excel(xlsx, 'fdg')
        self.tab_structer = pd.read_excel(xlsx, 'tab')
    self.fdg_template = self.fdg_template.reset_index(drop=True)

    self.shortcut_dict = self.fdg_template.shortcut.to_dict()

    return

elif LE_result:
temp = ''
temp = selection
self.select.LE_Layout_Temp.addWidget(self.select.Button_Temp)
for LE_block in LE_result:
    lable_text = temp.split(LE_block, 1)[0]
    temp = temp.split(LE_block, 1)[1]
    self.select.Lable_Temp = QtWidgets.QLabel(self.select.scrollAreaWidgetContents)
    self.select.Lable_Temp.setObjectName("LE_" + str(Layout_i) + '_' + str(button_i) + '_' + str(LE_i))
    # print("LE_" + str(Layout_i) + '_' + str(button_i) + '_' + str(LE_i))
    LE_i += 1
    self.select.Lable_Temp.setText(lable_text)
    self.select.LE_Layout_Temp.addWidget(self.select.Lable_Temp)
    self.select.LE_Temp = QtWidgets.QLineEdit(self.select.scrollAreaWidgetContents)
    self.select.LE_Temp.textChanged.connect(self.autoselect)
    self.select.LE_Temp.setObjectName(
        'LE_' + str(Layout_i) + '_' + str(button_i) + '_' + str(LE_i) + '_' + LE_block.replace('LE[', '').replace(']',
                                                                                                                  ''))
    LE_i += 1
    self.select.LE_Temp.setMaximumWidth(40)
    self.select.LE_Layout_Temp.addWidget(self.select.LE_Temp)
if temp:
    self.select.Lable_Temp = QtWidgets.QLabel(self.select.scrollAreaWidgetContents)
    self.select.Lable_Temp.setObjectName("LE_" + str(Layout_i) + '_' + str(button_i) + '_' + str(LE_i))
    self.select.Lable_Temp.setText(temp)
    self.select.LE_Layout_Temp.addWidget(self.select.Lable_Temp)
in_selection += 1

elif H_result:
temp = ''
temp = selection
self.select.H_Layout_Temp.addWidget(self.select.Button_Temp)
for H_block in H_result:
    if '|' in H_block:
        blocks = H_block.split('[')[1].replace(']', '').split('|')
    lable_text = temp.split(H_block, 1)[0]
    temp = temp.split(H_block, 1)[1]
    if lable_text:
        self.select.Lable_Temp = MycLabel(self.select.scrollAreaWidgetContents)
        self.select.Lable_Temp.setObjectName("inH_" + str(Layout_i) + '_' + str(button_i) + '_' + str(LE_i) + '_LA')
        self.select.Lable_Temp.setText(lable_text)
        self.select.Lable_Temp.click_signal.connect(self.lable_click)
        self.select.H_Layout_Temp.addWidget(self.select.Lable_Temp)
        LE_i += 1
    self.select.inH_Layout_Temp = QtWidgets.QHBoxLayout()
    self.select.inH_Layout_Temp.setObjectName("inH_" + str(Layout_i) + '_' + str(button_i) + '_Layout')
    self.select.H_Layout_Temp.addLayout(self.select.inH_Layout_Temp)
    self.select.inH_buttonGroup = QtWidgets.QButtonGroup(self.select.inH_Layout_Temp)
    for block in blocks:
        self.select.block_Button_Temp = QtWidgets.QRadioButton(self.select.scrollAreaWidgetContents)
        self.select.block_Button_Temp.setObjectName(
            "inH_" + str(Layout_i) + '_' + str(button_i) + '_' + str(LE_i) + '_RB')
        self.select.block_Button_Temp.setFont(font)
        self.select.block_Button_Temp.setText(block.strip().replace('+', ''))
        self.select.block_Button_Temp.setStyleSheet("background-color: rgb(0, 255, 0)")
        self.select.block_Button_Temp.toggled.connect(self.autoselect)
        # self.select.frame_Temp = CentralWidget(self.select.block_Button_Temp)
        self.select.inH_Layout_Temp.addWidget(self.select.block_Button_Temp)
        self.select.inH_buttonGroup.addButton(self.select.block_Button_Temp)
        if '+' in selection:
            self.select.block_Button_Temp.setChecked(True)
        LE_i += 1
if temp:
    self.select.Lable_Temp = MycLabel(self.select.scrollAreaWidgetContents)
    self.select.Lable_Temp.setObjectName("inH_" + str(Layout_i) + '_' + str(button_i) + '_' + str(LE_i) + '_LA')
    self.select.Lable_Temp.setText(temp)
    self.select.Lable_Temp.click_signal.connect(self.lable_click)
    self.select.H_Layout_Temp.addWidget(self.select.Lable_Temp)
    LE_i += 1
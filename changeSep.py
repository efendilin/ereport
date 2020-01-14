
import json
import re
import os,sys
from PyQt5 import QtCore, QtGui, QtWidgets, Qt


def keywordlize(term):
    def _add_slash(matched):
        matched = '{}'.format(str('\\')) + matched.group()
        return matched

    term = re.sub('[\[\]\(\)\+\.\^\$\*\?\{\}\|]', _add_slash, term)
    return term

def change_sep(matched):
    return matched.group().replace(',', '|')

app = QtWidgets.QApplication(sys.argv)

home_path = os.getenv("HomePath")
file_path = ''
save_file = ''

file_path, filter = QtWidgets.QFileDialog.getOpenFileName(None, 'Choice json file', home_path, filter ="json (*.json *.)")

if not file_path:
    exit()

with open(file_path, 'r') as file_json:
    template = json.load(file_json)

pattern = re.compile('\{.+?\}')
P_pattern = re.compile('\(.*?\)')
parentheses_temp = {}

for key in template['fdg'].keys():
    main = template['fdg'][key]['main']
    P_result = P_pattern.findall(main)
    if P_result:
        i = 0
        for parentheses in P_result:
            sign = 'parentheses' + '[{}]'.format(str(i))
            main = re.sub(keywordlize(parentheses), sign, main, 1)
            parentheses_temp[str(i)] = parentheses
            i += 1

    if pattern.findall(main):
        main = pattern.sub(change_sep, main)

    if parentheses_temp:
        for index in parentheses_temp.keys():
            main = main.replace('parentheses' + '[{}]'.format(str(index)), parentheses_temp[index])
    template['fdg'][key]['main'] = main

print(template)
os.rename(file_path, file_path.replace('.json','_old.json'))

with open(file_path, 'w') as file_json:
    json.dump(template, file_json)
# -*- coding: utf-8 -*-

from os import linesep
import sys
import re

sents = []
allwords = []
temp = ''
try:
    f = open('myreport.txt', 'r', encoding='utf-8-sig')
except UnicodeDecodeError:
    f = open('myreport.txt', 'r', encoding='cp950')
while True:
    t = f.readline()
    if t.strip():
        if re.match('\d\.', t.strip()):
            if temp:
                sents.append(temp)
                temp = t.strip()
            else:
                temp = t.strip()
        else:
            temp = temp + ' ' + t.strip()

    if t == '':
        if temp:
            sents.append(temp)
        break

for sent in sents:
    print(sent)
print(len(sents))

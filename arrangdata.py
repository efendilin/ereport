from os import linesep
import sys
import re

sents = []
allwords = []
temp = ''
try:
    f = open('words.txt', 'r', encoding='utf-8-sig')
except UnicodeDecodeError:
    f = open('words.txt', 'r', encoding='cp950')
while True:
    t = f.readline()
    if t == '':break
    if t.strip():
        if not t.strip() in allwords:
            allwords.append(t.strip())

try:
    f = open('words1.txt', 'w', encoding='utf-8-sig')
except:
    sys.exit()
for word in allwords:
    f.writelines(word + linesep)
f.close()

sys.exit()
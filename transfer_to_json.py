

import pandas as pd
import json


xlsx_file = ''
seeting_path = './setting/'
template = {}
fdg = {}

with pd.ExcelFile(seeting_path + xlsx_file) as xlsx:
    fdg_template = pd.read_excel(xlsx, 'fdg')

r_count, c_count = fdg_template.shape



for i in range(r_count):
    fdg[str(i)] = {'category':fdg_template.iloc[i].category,'shortcut':,'main':,'active':}


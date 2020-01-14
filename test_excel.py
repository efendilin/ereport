
import pandas as pd

template_keypair = {}

template = pd.read_excel('./setting/template.xlsx')

print(template.icol(0))
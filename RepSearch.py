# -*- coding: utf-8 -*-

import sys
import requests
import datetime
from bs4 import BeautifulSoup
from os import linesep


class MyRQS_Searcher():

    def __init__(self, proxy='', url='http://10.1.150.73/RQS/webRQS.aspx', headers={'User-Agent': 'Mozilla/5.0'}):

        self.url = url
        self.headers = headers
        if proxy:
            self.proxy = {"http": "http://{}".format(proxy),"https": "https://{}".format(proxy)}
        else:
            self.proxy = {}
        self.payload = {}
        self.link_payload = {}
        self.init = ''
        self.status = ''
        self.cat_dict = []
        self.s = requests.Session()
        self.init_connect()

        self.reptemp = '''
        ----{} at {} by {}----\n
        {}\n
        ------------END------------------\n
        '''
        self.reptitle = '----{} at {} by {}----\n'
        self.tempchcolor = " <span style=\"font-weight:800; color:{}\" > {} </span> "
        self.tempchsize = " <span style=\"font-weight:800\" > {} </span> "
        self.colorneedch = ['Red', 'Blue']

        return

    def init_connect(self):
        self.init = False
        try:
            r = self.s.post(self.url, proxies=self.proxy, headers=self.headers, timeout=6.1)
        except:
            self.init = False
        else:
            self.soup = BeautifulSoup(r.text, 'lxml')
            for i in range(4):
                self.payload[self.soup.find_all('input')[i]['name']] = self.soup.find_all('input')[i]['value']
            self.status = r.status_code
            self.init = True

        return

    def datechanger(self, thedate):
        bcdate = datetime.datetime((int(thedate[:3]) + 1911), int(thedate[3:5]), int(thedate[5:7]))
        return bcdate

    def query(self, page=''):
        result = False
        if page:
            self.payload['__EVENTTARGET'] = page
        try:
            r = self.s.post(self.url, headers=self.headers, data=self.payload, proxies=self.proxy, timeout=6.1)
        except ConnectTimeout:
            result = False
        except:
            result = False
        else:
            self.soup = BeautifulSoup(r.text, 'lxml')
            self.payload[self.soup.find_all('input')[2]['name']] = self.soup.find_all('input')[2]['value']
            #self.status = r.status_code
            result = True
            if 'btnQuery' in self.payload:
                self.prog = 0
                del self.payload['btnQuery']

        return result

    #def numPrinter(self, numlist):
    #    numitem = ""
    #    numitem = "{:^8} : {:^6}".format(numlist[0], numlist[1])
    #    if numlist[5]:
    #        numitem = numitem + " ({}) {}".format(numlist[5], numlist[2])
    #    else:
    #        numitem = numitem + " {}".format(numlist[2])
    #    if numlist[3]:
    #        numitem = numitem + ", 參考值( {:^5} - {:^5} )".format(numlist[3], numlist[4])
    #    if numlist[6]:
    #        numitem = numitem + ", 前次數值: {:^6} at {:^6}".format(numlist[6], numlist[7]
    #    return numitem

    def progress(self, percent):

        return

    def getlistquary(self,  pid, txtASTR='', dpDate='一月內', dpKind='所有檢查單', btnQuery='查  詢'):
        print('start get link')
        if not self.init:
            return False
        self.payload['__EVENTTARGET'] = ''
        self.payload['txtASTR'] = txtASTR
        self.payload['txtCHRT'] = pid
        self.payload['dpDate'] = dpDate
        self.payload['dpKind'] = dpKind
        self.payload['btnQuery'] = btnQuery
        self.link_payload = self.payload
        self.pdata = {}
        self.linkresult = []


        if self.query():
            pages = ['']
            repspect = {}
            allreplinks = []
            firspage = ''
            pagenum = len(self.soup.find_all('table')[2].find_all('a')) - 15
            if pagenum > 0:
                for i in range(pagenum):
                    pages.append(":".join(self.soup.find_all('table')[2].find_all('a')[15 + i]['href'].split("'")[1].split("$")))
            for page in pages:
                if page:
                    self.query(page=page)
                    if not firspage:
                        p = len(self.soup.find_all('table')[2].find_all('a'))
                        if pagenum > 2:
                            firspage = ":".join(self.soup.find_all('table')[2].find_all('a')[15]['href'].split("'")[1].split("$"))
                        else:
                            firspage = ":".join(self.soup.find_all('table')[2].find_all('a')[p-1]['href'].split("'")[1].split("$"))
                        
                repnum = (len(self.soup.find_all('table')[3].find_all('td')) - 4) // 3
                for i in range(repnum):
                    replink = []
                    repspect = {}
                    repspect['repkind'] = self.soup.find_all('table')[3].find_all('td')[(i + 1) * 3 + 2].text.strip()
                    repspect['repdate'] = self.datechanger(self.soup.find_all('table')[3].find_all('td')[(i + 1) * 3 + 1].text.strip())
                    replink.append(page)
                    replink.append(":".join(self.soup.find_all('table')[3].find_all('td')[(i + 1) * 3].a['href'].split("'")[1].split("$")))
                    repspect['replink'] = replink
                    allreplinks.append(repspect)
            for repspect in allreplinks:
                if firspage:
                    if not repspect['replink'][0]:
                        repspect['replink'][0] = firspage
        print('get links done')

        return allreplinks
    
    def getdatabylink(self, links, word_color=True):
        #Debug print('start get date')
        if self.link_payload:
            self.payload = self.link_payload
            self.pdata = {}
            self.represult = []
            repdict = {}
            #self.payload['__EVENTTARGET'] = ''
            
            for link in links:
                self.query (page=link)
            if not self.pdata:
                self.pdata['name'] = self.soup.find_all('span', id="lblPnam")[0].text.strip()
                self.pdata['sex'] = self.soup.find_all('span', id="lblSex")[0].text.strip()
            repdict['age'] = self.soup.find_all('span', id="lblAge")[0].text.strip()
            repdict['drname'] = self.soup.find_all('span', id="lblDtid")[0].text.strip()
            if self.soup.find_all('table')[2].find_all('tr', bgcolor="#FFCC66"):
                repdict['repkind'] = self.soup.find_all('table')[2].find_all('tr', bgcolor="#FFCC66")[0].find_all('td')[2].text.strip()
                repdict['repdate'] = self.soup.find_all('table')[2].find_all('tr', bgcolor="#FFCC66")[0].find_all('td')[1].text.strip()
            elif self.soup.find_all('table')[2].find_all('tr', bgcolor=":#663399"):
                repdict['repkind'] = self.soup.find_all('table')[2].find_all('tr', bgcolor="#FFCC66")[0].find_all('td')[2].text.strip()
                repdict['repdate'] = self.soup.find_all('table')[2].find_all('tr', bgcolor="#FFCC66")[0].find_all('td')[1].text.strip()
            else:
                repdict['repkind'] = ''
                repdict['repdate'] = ''

            if len(self.soup.find_all('table')) == 5:
                repdict['text'] = self.soup.textarea.text
            elif len(self.soup.find_all('table')) == 6:
                datalines = []
                tpages = []
                tpages.append('')
                npage = len(self.soup.find_all('table')[4].find_all('a'))
                if npage:
                    for i in range(npage):
                        tpages.append(":".join(self.soup.find_all('table')[4].find_all('a')[i]['href'].split("'")[1].split("$")))
                starin = 0
                for tpage in tpages:
                    if tpage:
                        starin = 1
                    if self.query(page=tpage):
                        tnum = (len(self.soup.find_all('table')[4].find_all('td')) - 1) // 8
                        print(tnum)
                        for l in range(starin, tnum):
                            dataline = []
                            for j in range(8):
                                if self.soup.find_all('table')[4].find_all('td')[l * 8 + j]:
                                    color = self.soup.find_all('table')[4].find_all('td')[l * 8 + j].font['color'].strip()
                                else:
                                    color = ''
                                if self.soup.find_all('table')[4].find_all('td')[l * 8 + j]:
                                    word = self.soup.find_all('table')[4].find_all('td')[l * 8 + j].text.strip()
                                else:
                                    word = ''
                                if word:
                                    if word_color:
                                        if color in self.colorneedch:
                                            if '<' in word: word = word.replace('<', '&lt;')
                                            dataline.append(self.tempchcolor.format(color, word))
                                        elif j == 1:
                                            dataline.append(self.tempchsize.format(word))
                                        else:
                                            dataline.append(word)
                                    else:
                                        dataline.append(word)
                                else:
                                    dataline.append(word)
                            datalines.append(dataline)
                repdict['nums'] = datalines
            self.represult.append(repdict)
            self.pdata['result'] = self.represult
            print('get date done')
            return self.pdata
        else:
            return False
            
        return 

    def search(self, pid, txtASTR='', dpDate='一月內', dpKind='所有檢查單', btnQuery='查  詢', numtotext=False, word_color=True):

        if not self.init:
            return False
        self.payload['__EVENTTARGET'] = ''
        self.payload['txtASTR'] = txtASTR
        self.payload['txtCHRT'] = pid
        self.payload['dpDate'] = dpDate
        self.payload['dpKind'] = dpKind
        self.payload['btnQuery'] = btnQuery
        #self.cat_dict = cat_dict
        self.numtotext = numtotext
        self.word_color = word_color
        self.pdata = {}
        self.represult = []


        if self.query():
            repnums = len(self.soup.find_all('a', text='內容'))
            if repnums:
                pages = []
                pages.append('')             # get main page numbers and links
                pagenum = len(self.soup.find_all('table')[2].find_all('a')) - 15
                if pagenum > 0:
                    for i in range(pagenum):
                        pages.append(":".join(self.soup.find_all('table')[2].find_all('a')[15+i]['href'].split("'")[1].split("$")))
                progperpage = 100 / len(pages)
                for page in pages:
                    replink = []
                    if self.query(page=page):
                        repnums = len(self.soup.find_all('a', text='內容'))
                        progperrep = progperpage / repnums
                        for n in range(repnums):
                            replink.append(":".join(self.soup.find_all('a', text='內容')[n]['href'].split("'")[1].split("$")))
                        if replink:
                            for link in replink:
                                repdict = {}
                                if self.query(page=link):
                                    if not self.pdata:
                                        self.pdata['name'] = self.soup.find_all('span', id="lblPnam")[0].text.strip()
                                        self.pdata['sex'] = self.soup.find_all('span', id="lblSex")[0].text.strip()
                                    repdict['age'] = self.soup.find_all('span', id="lblAge")[0].text.strip()
                                    repdict['drname'] = self.soup.find_all('span', id="lblDtid")[0].text.strip()
                                    if self.soup.find_all('table')[2].find_all('tr', bgcolor="#FFCC66"):
                                        repdict['repkind'] = self.soup.find_all('table')[2].find_all('tr', bgcolor="#FFCC66")[0].find_all('td')[2].text.strip()
                                        repdict['repdate'] = self.soup.find_all('table')[2].find_all('tr', bgcolor="#FFCC66")[0].find_all('td')[1].text.strip()
                                    elif self.soup.find_all('table')[2].find_all('tr', bgcolor=":#663399"):
                                        repdict['repkind'] = self.soup.find_all('table')[2].find_all('tr', bgcolor="#FFCC66")[0].find_all('td')[2].text.strip()
                                        repdict['repdate'] = self.soup.find_all('table')[2].find_all('tr', bgcolor="#FFCC66")[0].find_all('td')[1].text.strip()
                                    else:
                                        repdict['repkind'] = ''
                                        repdict['repkind'] = ''
                                    
                                    if len(self.soup.find_all('table')) == 5:
                                        repdict['text'] = self.soup.textarea.text
                                    elif len(self.soup.find_all('table')) == 6:
                                        datalines = []
                                        tpages = []
                                        tpages.append('')
                                        npage = len(self.soup.find_all('table')[4].find_all('a'))
                                        if npage:
                                            for i in range(npage):
                                                tpages.append(":".join(self.soup.find_all('table')[4].find_all('a')[i]['href'].split("'")[1].split("$")))
                                        starin = 0
                                        for tpage in tpages:
                                            if tpage:
                                                starin = 1
                                            if self.query(page=tpage):
                                                tnum = (len(self.soup.find_all('table')[4].find_all('td')) - 1) // 8
                                                for l in range(starin, tnum):
                                                    dataline = []
                                                    for j in range(8):
                                                        color = self.soup.find_all('table')[4].find_all('td')[l * 8 + j].font['color'].strip()
                                                        word = self.soup.find_all('table')[4].find_all('td')[l * 8 + j].text.strip()
                                                        if word:
                                                            if self.word_color:
                                                                if color in self.colorneedch:
                                                                    if '<' in word: word = word.replace('<', '&lt;')
                                                                    dataline.append(self.tempchcolor.format(color, word))
                                                                elif j == 1:
                                                                    dataline.append(self.tempchsize.format(word))
                                                                else:
                                                                    dataline.append(word)
                                                            else:
                                                                dataline.append(word)
                                                        else:
                                                            dataline.append(word)
                                                    datalines.append(dataline)
                                        repdict['nums'] = datalines
                                self.represult.append(repdict)
                                self.progress(progperrep)
                            self.pdata['result'] = self.represult
                        return self.pdata
        return False

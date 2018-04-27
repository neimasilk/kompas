import xml.etree.ElementTree as etree
import codecs
import csv
import nltk
import time
import os
from unidecode import unidecode
from urllib import request
from bs4 import BeautifulSoup as BS
import string
import re
# given your html as the variable 'html'

import sys
sys.stdout = open('thefile.txt', 'w')
# http://www.ibm.com/developerworks/xml/library/x-hiperfparse/

PATH_WIKI_XML = '.\\'
FILENAME_WIKI_ID = 'idwiki-latest-pages-articles.xml'
FILENAME_WIKI_ZH = 'idwiki-latest-pages-articles.xml'
FILENAME_ARTICLES = 'articles.csv'
FILENAME_REDIRECT = 'articles_redirect.csv'
FILENAME_TEMPLATE = 'articles_template.csv'
ENCODING = "utf-8"


# Nicely formatted time string
def hms_string(sec_elapsed):
    h = int(sec_elapsed / (60 * 60))
    m = int((sec_elapsed % (60 * 60)) / 60)
    s = sec_elapsed % 60
    return "{}:{:>02}:{:>05.2f}".format(h, m, s)


def strip_tag_name(t):
    t = elem.tag
    idx = k = t.rfind("}")
    if idx != -1:
        t = t[idx + 1:]
    return t

def remove_non_ascii(text):
    return unidecode(str(text))
def token_saja(teks,no_punct=True):
    teksToken = nltk.word_tokenize(teks)
    teks = nltk.Text(teksToken)
    kecil = [w.lower() for w in teks]
    no_ascii = [remove_non_ascii(huruf) for huruf in kecil]
    if no_punct:
        nopuncnonumber1 = [x for x in no_ascii if not re.search('[' + string.punctuation.replace("-","") + ']+', x)]
        nopuncnonumber2 = [x for x in nopuncnonumber1 if not re.search(r'\d+', x)]
        nopuncnonumber3 = [x for x in nopuncnonumber2 if not re.search(r'\=', x)]
        nopuncnonumber = [x for x in nopuncnonumber3 if not re.search(r'\/', x)]
        isi = "".join([" " + i for i in nopuncnonumber]).strip()
    else:
        isi = "".join([" " + i for i in no_ascii]).strip()
    return isi
pathWikiXML = os.path.join(PATH_WIKI_XML, FILENAME_WIKI_ID)
pathArticles = os.path.join(PATH_WIKI_XML, FILENAME_ARTICLES)
pathArticlesRedirect = os.path.join(PATH_WIKI_XML, FILENAME_REDIRECT)
pathTemplateRedirect = os.path.join(PATH_WIKI_XML, FILENAME_TEMPLATE)

totalCount = 0
articleCount = 0
redirectCount = 0
templateCount = 0
title = None
start_time = time.time()
isi = ''

for event, elem in etree.iterparse(pathWikiXML, events=('start', 'end')):
    tname = strip_tag_name(elem.tag)
    if event == 'start':
        if tname == 'page':
            title = ''
            id = -1
            redirect = ''
            inrevision = False
            ns = 0
        elif tname == 'revision':
            # Do not pick up on revision id's
            inrevision = True
    else:
        if tname == 'title':
            title = elem.text
        elif tname == 'id' and not inrevision:
            id = int(elem.text)
        elif tname == 'redirect':
            redirect = elem.attrib['title']
        elif tname == 'ns':
            ns = int(elem.text)
        elif tname == 'text':
            # if 88000 < id <89000:
            # print(id)
            teks = elem.text
            pages = BS(str(teks), "html.parser")
            isi_teks = token_saja(pages.text.strip())
            print(isi_teks)
            teks = ""

        elif tname == 'page':
            totalCount += 1

            if ns == 10:
                templateCount += 1
            elif len(redirect) > 0:
                articleCount += 1
            else:
                redirectCount += 1

            # if totalCount > 100000:
            #  break

            # if totalCount > 1 and (totalCount % 100000) == 0:
            #     print("{:,}".format(totalCount))

        elem.clear()
#
# saveFile = open('wikipedia.txt', 'w')
# saveFile.write(isi)
# saveFile.close()

# soup = BS(open(pathWikiXML).read(), "xml")

# pages = 'berkas dna structure+key+labelled.pn heliks ganda dna atom -atom pada struktur tersebut diwarnai sesuai dengan unsur kimia nya dan struktur detail dua pasangan basa ditunjukkan oleh gambar kanan bawah berkas adn animation.gif|jmpl|gambaran tiga dimensi'
# print(token_saja(pages.text.strip()))
# print(pages.text.strip())

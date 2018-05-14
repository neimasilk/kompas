from stanford_segmenter import Segmenter
import xml.etree.ElementTree as etree
import codecs
import csv
import nltk
import time
import os
from urllib import request
from bs4 import BeautifulSoup as BS
import string
import re
from stanford_segmenter import Segmenter


# baca isi wikipedia
# token saja:
#   segmentasi kata
#   hilangkan tanda baca
#   join seluruh isinya menjadi urutan kata

# baca wikipedia:
#   copy wikipedia zh xml
#
pathWikiXML = './zhwiki-latest-pages-articles.xml'

seg = Segmenter()

def strip_tag_name(t):
    t = elem.tag
    idx = k = t.rfind("}")
    if idx != -1:
        t = t[idx + 1:]
    return t

def token_cn(teks,no_punct=True):
    teksToken = seg.cn_segment(teks)
    kecil = [w.lower() for w in teksToken]
    no_ascii = kecil
    if no_punct:
        nopuncnonumber1 = [x for x in no_ascii if not re.search('[' + string.punctuation.replace("-","") + ']+', x)]
        nopuncnonumber2 = [x for x in nopuncnonumber1 if not re.search(r'^[a-zA-Z0-9_]*$', x)]
        nopuncnonumber3 = [x for x in nopuncnonumber2 if not re.search(r'\=', x)]
        nopuncnonumber = [x for x in nopuncnonumber3 if not re.search(r'\/', x)]
        isi = "".join([" " + i for i in nopuncnonumber]).strip()
    else:
        isi = "".join([" " + i for i in no_ascii]).strip()
    return isi

totalCount = 0
articleCount = 0
redirectCount = 0
templateCount = 0
title = None
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
            teks = elem.text
            pages = BS(str(teks), "html.parser")
            print(teks)
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
            if 0 < id < 100:
                print(id)
                # teks = elem.text
                # pages = BS(str(teks), "html.parser")
                # print(teks)
                # isi_teks = token_cn(pages.text.strip())
                # # print(isi_teks)
                # teks = ""
            else:
                break

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

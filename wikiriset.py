import xml.etree.ElementTree as etree
import codecs
import csv
import time
import os
from urllib import request
from bs4 import BeautifulSoup as BS
# given your html as the variable 'html'


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
            if id==769:
                teks = elem.text
                # print(teks)
                print(id)
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

            if totalCount > 1 and (totalCount % 100000) == 0:
                print("{:,}".format(totalCount))

        elem.clear()


# soup = BS(open(pathWikiXML).read(), "xml")
pages = BS(teks,"html5lib")
print(pages.text.strip(''))

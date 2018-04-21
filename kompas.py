# buat kompas leecher
# GITHUB VCS
# buat testcase

import nltk
import string
import re
from urllib import request
from bs4 import BeautifulSoup


class Kompas:
    def tokenSaja(self, teks):
        teksToken = nltk.word_tokenize(teks)
        teks = nltk.Text(teksToken)
        kecil = [w.lower() for w in teks]
        nokompas = [w for w in kecil if w != "kompas.com"]
        nopuncnonumber1 = [x for x in nokompas if not re.fullmatch('[' + string.punctuation + ']+', x)]
        nopuncnonumber2 = [x for x in nopuncnonumber1 if not re.search(r'\d+', x)]
        nopuncnonumber3 = [x for x in nopuncnonumber2 if not re.search(r'\=', x)]
        nopuncnonumber = [x for x in nopuncnonumber3 if not re.search(r'\/', x)]
        isi = "".join([" " + i for i in nopuncnonumber]).strip()
        return isi

    def getContent(self, url):
        html = request.urlopen(url).read().decode('utf-8')
        rawhtml = BeautifulSoup(html, "html5lib")
        for script in rawhtml(["script", "style"]):
            script.extract()  # rip it out
        rawheadline = rawhtml.select("[class^=read__title]")
        headline = rawheadline[0].get_text()
        rawnewsbody = rawhtml.select("[class^=read__content]")
        newsbody = rawnewsbody[0].get_text()
        isi = self.tokenSaja(newsbody)
        return headline, isi

    def kompasIndex(self,tgl):
        urltemp = "http://indeks.kompas.com/news/"
        tanggal = tgl
        indexPages = ""
        url = urltemp + tanggal + indexPages
        listurl = []
        link = []

        html = request.urlopen(url).read().decode('utf-8')
        rawhtml = BeautifulSoup(html, "html5lib")
        for script in rawhtml(["script", "style"]):
            script.extract()  # rip it out
        rawindex = rawhtml.select("a[class^=article__link]")
        # indexpertama = rawindex[0]
        for link1 in rawindex:
            link.append(link1['href'])

        maxind = rawhtml.select("a[class^=paging__link]")
        tempmax = maxind[len(maxind) - 1]
        maxindex = tempmax['data-ci-pagination-page']

        for i in range(int(maxindex) + 1):
            if i > 1:
                listurl.append(url + "/" + str(i))

        for i in range(len(listurl)):
            html = request.urlopen(listurl[i]).read().decode('utf8')
            rawhtml = BeautifulSoup(html, "html5lib")
            for script in rawhtml(["script", "style"]):
                script.extract()  # rip it out
            rawindex = rawhtml.select("a[class^=article__link]")
            for link1 in rawindex:
                link.append(link1['href'])
        return link


if __name__ == "__main__":
    kompas = Kompas()
    tanggal = "2014-01-01"
    daftar = kompas.kompasIndex(tanggal)
    print(daftar)

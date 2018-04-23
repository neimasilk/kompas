# buat kompas leecher
# GITHUB VCS
# buat testcase

import nltk
import string
import re
from urllib import request
from bs4 import BeautifulSoup
# import _pickle as pickle
from unidecode import unidecode


class Kompas:
    def token_saja(self, teks):
        teksToken = nltk.word_tokenize(teks)
        teks = nltk.Text(teksToken)
        kecil = [w.lower() for w in teks]
        no_ascii = [self.remove_non_ascii(huruf) for huruf in kecil]
        nokompas = [w for w in no_ascii if w != "kompas.com"]
        nopuncnonumber1 = [x for x in nokompas if not re.fullmatch('[' + string.punctuation + ']+', x)]
        nopuncnonumber2 = [x for x in nopuncnonumber1 if not re.search(r'\d+', x)]
        nopuncnonumber3 = [x for x in nopuncnonumber2 if not re.search(r'\=', x)]
        nopuncnonumber = [x for x in nopuncnonumber3 if not re.search(r'\/', x)]
        isi = "".join([" " + i for i in nopuncnonumber]).strip()
        return isi

    def get_content(self, url):
        html = request.urlopen(url).read().decode('utf-8')
        rawhtml = BeautifulSoup(html, "html5lib")
        for script in rawhtml(["script", "style"]):
            script.extract()  # rip it out
        rawheadline = rawhtml.select("[class^=read__title]")
        headline = rawheadline[0].get_text()
        rawnewsbody = rawhtml.select("[class^=read__content]")
        newsbody = rawnewsbody[0].get_text()
        isi = self.token_saja(newsbody)
        return headline, isi

    def kompas_index(self, tgl):
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

    def remove_non_ascii(self, text):
        return unidecode(str(text))

    def save_token(self, tokens, namafile):
        # mengembalikan text dari token
        join_seluruh = ""
        for i in tokens:
            joinIsi = "".join(" " + j for j in i)
            join_seluruh = join_seluruh + " " + joinIsi
        saveFile = open(namafile, 'w')
        join_seluruh = self.remove_non_ascii(join_seluruh)
        saveFile.write(join_seluruh)
        saveFile.close()
        # f = open(namafile + ".pkl", 'wb')
        # pickle.dump(tokens, f)
        # f.close()
        return join_seluruh

    def kompas_leech(self, daftar, namafile, save=True, tampil=False):
        tokens = []
        for i in daftar:
            if tampil:
                print(i)
            try:
                header, isi = self.get_content(i)
                token = nltk.word_tokenize(isi)
                # print(token[1:])
                # hilangkan kata kompas.com dan kota dimana diberitakan
                tokens.append(token[1:])
            except:
                pass
        if save:
            self.save_token(tokens, namafile)
        return tokens


if __name__ == "__main__":
    kompas = Kompas()
    tanggal = "2015-04-21"
    daftar = kompas.kompas_index(tanggal)
    kompas.kompas_leech(daftar, "save.txt", True, True)




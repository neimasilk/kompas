from bs4 import BeautifulSoup as bs
import sqlite3
import os
import random
import nltk
import re
import string
from stanford_segmenter import Segmenter

def generate_list_id(tabel, ukuran, max_count):
    ukur = 0
    daftar_id = []
    while ukur <= ukuran:
        acak = random.randint(1, max_count)
        c.execute("select id,ukuran from {df_tabel} limit 1 OFFSET {df_acak}".format(df_tabel=tabel,df_acak=acak))
        (id_nya, ukuran_data) = c.fetchone()
        # select limit 1 offset acak
        # ambil id dan ukuran_data
        if not(id_nya in daftar_id):
            daftar_id.append(id_nya)
        ukur = ukur + ukuran_data
    return daftar_id


def token_saja(teks, zh= False):
    if zh:
        seg = Segmenter()
        isi = seg.cn_segment(teks)
        nopuncnonumber1 = [x for x in isi if not re.search('[' + string.punctuation.replace("-","") + ']+', x)]
        nopuncnonumber2 = [x for x in nopuncnonumber1 if not re.search(r'\d+', x)]
        nopuncnonumber3 = [x for x in nopuncnonumber2 if not re.search(r'\=', x)]
        nopuncnonumber = [x for x in nopuncnonumber3 if not re.search(r'\/', x)]
        isi = "".join([" " + i for i in nopuncnonumber]).strip()

    else:
        teksToken = nltk.word_tokenize(teks)
        teks = nltk.Text(teksToken)
        kecil = [w.lower() for w in teks]
        nopuncnonumber1 = [x for x in kecil if not re.search('[' + string.punctuation.replace("-","") + ']+', x)]
        nopuncnonumber2 = [x for x in nopuncnonumber1 if not re.search(r'\d+', x)]
        nopuncnonumber3 = [x for x in nopuncnonumber2 if not re.search(r'\=', x)]
        nopuncnonumber = [x for x in nopuncnonumber3 if not re.search(r'\/', x)]
        isi = "".join([" " + i for i in nopuncnonumber]).strip()
    return isi

if __name__ == '__main__':


    count_zh = 993061
    count_id = 408734


    sqlite_file = '/home/mukhlis/machine_learning_nlp'
    table_name = 'wiki_id'
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    daftarnya = generate_list_id('wiki_zh', 5000, count_zh)
    print(daftarnya)
    args = daftarnya
    sql = "select dokumen from wiki_zh where id in ({seq}) order by random()".format(seq=','.join(['?'] * len(args)))
    c.execute(sql, args)

    rows = c.fetchall()
    a = ""
    for row in rows:
        a = a + row[0]
    b = token_saja(a, True)
    saveFile = open('wikipedia.txt', 'w')
    saveFile.write(b)
    saveFile.close()
    print(len(b))



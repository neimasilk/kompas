from bs4 import BeautifulSoup as bs
import sqlite3
import os
import random
import nltk
import re
import string
from stanford_segmenter import Segmenter
import _pickle as pickle


sqlite_file = '/home/mukhlis/machine_learning_nlp'
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()


def generate_list(tabel, ukuran, max_count):
    ukur = 0
    daftar_id = []
    l = list(range(max_count))
    random.shuffle(l)
    print("randomize...")
    a = ""
    indeks = 0
    while ((indeks < max_count) and (ukur <= ukuran)):
        c.execute("select id,dokumen, ukuran from {df_tabel} where id = {df_acak}+1".format(df_tabel=tabel,df_acak=l[indeks]))
        (id_nya, dokumen, ukuran_data) = c.fetchone()
        # select limit 1 offset acak
        # ambil id dan ukuran_data
        daftar_id.append(id_nya)
        toks = dokumen.encode('utf-8', 'replace').decode('utf-8')
        a = a + (token_saja(toks, False) if tabel == 'wiki_id' else token_saja(toks, True))
        ukur = ukur + ukuran_data
        indeks = indeks+1
        if indeks%2000==0:
            print("Suffeling {0:.2f}%".format((ukur/ukuran)*100))
    return a, daftar_id


def token_saja(teks, zh= False):
    if zh:
        isi = seg.cn_segment(teks)
        nopuncnonumber1 = [x for x in isi if not re.search('[' + string.punctuation.replace("-","") + "。（），《 》、〈〉；：「」"+ ']+', x)]
        nopuncnonumber2 = [x for x in nopuncnonumber1 if not re.search(r'\d+', x)]
        nopuncnonumber3 = [x for x in nopuncnonumber2 if not re.search(r'\=', x)]
        nopuncnonumber = [x for x in nopuncnonumber3 if not re.search(r'\/', x)]
        isi = "".join([" " + i for i in nopuncnonumber]).strip()

    else:
        teksToken = nltk.word_tokenize(teks)
        teks = nltk.Text(teksToken)
        kecil = [w.lower() for w in teks]
        nopuncnonumber1 = [x for x in kecil if not re.search('[' + string.punctuation.replace("-","") +  ']+', x)]
        nopuncnonumber2 = [x for x in nopuncnonumber1 if not re.search(r'\d+', x)]
        nopuncnonumber3 = [x for x in nopuncnonumber2 if not re.search(r'\=', x)]
        nopuncnonumber = [x for x in nopuncnonumber3 if not re.search(r'\/', x)]
        isi = "".join([" " + i for i in nopuncnonumber]).strip()
    return isi

# def generate_token(daftar, sumber):
#     l = daftar
#     n =500
#     daft = [l[i:i + n] for i in range(0, len(l), n)]
#     a = ""
#     toks=""
#     prs =0
#     for args in daft:
#         sql = "select dokumen from {tf_table} where id in ({seq}) order by random()".format(tf_table=sumber, seq=','.join(['?'] * len(args)))
#         c.execute(sql, args)
#         rows = c.fetchall()
#         for row in rows:
#             toks = row[0].encode().decode('utf-8','surrogateescape' )
#             a = a + (token_saja(toks ,False) if sumber=='wiki_id' else token_saja(toks,True))
#         prs=prs+1
#         print('proses ' + str(prs))
#     return a


def generate_word2vec_data(sumber,ukuran):
    count_zh = 993061
    count_id = 408734
    if sumber.lower()=='wiki_id':
        print(str(sumber) + ' ' + str(ukuran) + ' ' + str(count_id))
        b, daftarnya = generate_list(sumber, ukuran, count_id)
        # b= generate_token(daftarnya,sumber)
    elif sumber.lower()=='wiki_zh':
        global seg
        seg = Segmenter()
        print(str(sumber) + ' ' + str(ukuran) + ' ' + str(count_zh))
        b, daftarnya = generate_list(sumber, ukuran, count_zh)
        # print(daftarnya)
        # b = generate_token(daftarnya,sumber)
    # print(b)
    return b

def total_wiki_id():
    sql = "select count(id) from wiki_id"
    c.execute(sql)
    rows = c.fetchone()
    tot = 0
    # for row in rows:
    #     tot = tot + row[0]
    return rows[0]

def total_wiki_zh():
    sql = "select count(id) from wiki_zh"
    c.execute(sql)
    rows = c.fetchone()
    tot = 0
    # for row in rows:
    #     tot = tot + row[0]
    return rows[0]

if __name__ == '__main__':




    b = generate_word2vec_data('wiki_zh',350000000)
    f = open("pikle_word2vec_zh" + ".pkl", 'wb')
    pickle.dump(b, f)
    f.close()
    try:
        saveFile = open('wikipedia_zh.txt', 'w')
        saveFile.write(b)
        saveFile.close()
    except:
        pass

    b = generate_word2vec_data('wiki_id',350000000)
    f = open("pikle_word2vec_id" + ".pkl", 'wb')
    pickle.dump(b, f)
    f.close()
    try:
        saveFile = open('wikipedia_id.txt', 'w')
        saveFile.write(b)
        saveFile.close()
    except:
        pass
    # print(total_wiki_id())
    # print(total_wiki_zh())





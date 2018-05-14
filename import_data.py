# buka file wiki indo
from bs4 import BeautifulSoup as bs
import sqlite3
import os

root_dir= '/home/mukhlis/wiki_txt/zhwiki'
sqlite_file = '/home/mukhlis/machine_learning_nlp'
table_name = 'wiki_zh'
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()
c.execute('DELETE FROM {ft_tablename}'.format(ft_tablename=table_name))
c.execute('VACUUM ')


def buka_file_teks(namafile):
    f=open(namafile,'r')
    teks = f.read()
    f.close()
    return teks


# Connecting to the database file

# A) Inserts an ID with a specific value in a second column
def input_data(namafile):
    list_data =[]
    dokumen = bs(buka_file_teks(namafile), 'lxml')
    for link in dokumen.find_all('doc'):
        id = link.get('id')
        situs = link.get('url')
        judul = link.get('title')
        dokumen = link.text
        ukuran = len(dokumen)
        # print(perintah)
        try:
            c.execute("INSERT INTO wiki_zh(situs, judul, dokumen, ukuran) VALUES (?,?,?,?)",(situs,judul,dokumen,ukuran))
        except sqlite3.IntegrityError:
            print('ERROR: ID already exists in PRIMARY KEY column {}'.format(id_column))


for root, subdirs, files in os.walk(root_dir):
    for filename in files:
        nama_file = os.path.join(root,filename)
        input_data(nama_file)


conn.commit()
conn.close()

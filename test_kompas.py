import unittest
from unittest import TestCase
from kompas import Kompas


class TestKompas(TestCase):
    def test_tokenSaja(self):
        # membersihkan token dan menghapus angka dan punctuasi kecuali -
        kompas = Kompas()
        test_kata_aneh = 'Terbayang-bayang @amien "percobaan" "/a" link=abcd SdAC 1234 1/2/3 '
        hasil_kata_aneh = 'terbayang-bayang amien percobaan sdac'
        self.assertEqual(kompas.tokenSaja(test_kata_aneh), hasil_kata_aneh)

    def test_getContent(self):
        # mengambil isi url dan membersihkannya serta dikembalikan dalam bentuk teks
        # nilai kembalian adalah, headline dan isi berita
        url = "http://internasional.kompas.com/read/2014/01/01/2254577/Perangkat.Keamanan.Meledak.Dubes.Palestina.untuk.Czech.Meninggal"
        kompas = Kompas()
        headline, isi = kompas.getContent(url)
        headline_diharapkan = 'Perangkat Keamanan Meledak, Dubes Palestina untuk Czech Meninggal'
        isi_diharapkan = 'praha duta besar palestina untuk republik czech jamal al jamal terbunuh saat sebuah perangkat keamanan meledak di kediamannya pada rabu pihak berwenang menyebutkan bahwa kejadian itu kemungkinan adalah sebuah insiden biasa.menteri luar negeri palestina menyebutkan jamal sebelumnya pindah ke rumah yang baru saat itu dia mencoba membuka sebuah lemari besi di rumahnya diperkirakan ledakan itu berasal dari perangkat keamanan rumah.namun sejauh ini belum jelas mengenai penyebab kejadian beberapa lemari besi terkadang bisa dilengkapi dengan perangkat yang memungkinkan penggunanya menghancurkan dokumen rahasia pihak keamanan czech juga menyebutkan bahwa itu bukanlah serangan teroris keterangan resmi dari kepolisian czech menyebutkan duta besar palestina meninggal dalam keadaan terluka saat dibawa ke rumah sakit pada pagi hari setelah malam tahun baru'
        self.assertEqual(headline, headline_diharapkan)
        self.assertEqual(isi, isi_diharapkan)

    def test_kompasIndex(self):
        kompas = Kompas()
        tanggal = "2014-01-01"
        daftar = kompas.kompasIndex(tanggal)
        self.assertEqual(len(daftar),100)
        self.assertEqual(daftar[0],'http://internasional.kompas.com/read/2014/01/01/2254577/Perangkat.Keamanan.Meledak.Dubes.Palestina.untuk.Czech.Meninggal')
        self.assertEqual(daftar[55],'http://megapolitan.kompas.com/read/2014/01/01/1208453/.Jokowi.Akan.Gandengkan.KJS.dengan.JKN')
        self.assertEqual(daftar[99],'http://olahraga.kompas.com/read/2014/01/01/0006207/Murray.dan.Nadal.Lewati.Babak.Pertama.Qatar.Open')


if __name__ == '__main__':
    unittest.main()



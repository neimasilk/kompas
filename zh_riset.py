# # Simple usage
# from stanfordcorenlp import StanfordCoreNLP
#
#
sentence = "是北加州围绕旧金山湾和圣帕布罗湾河口的一片城市群aremania halo, - halo ditepi 134134314."
# with StanfordCoreNLP(r'./',lang='zh') as nlp:
#     print(nlp.word_tokenize(sentence))
#     print(nlp.pos_tag(sentence))
#     print(nlp.ner(sentence))
#     print(nlp.parse(sentence))
#     print(nlp.dependency_parse(sentence))

from stanford_segmenter import Segmenter
import re
import string
# seg = Segmenter()
# print(seg.cn_segment(sentence))
seg = Segmenter()


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

print(token_cn(sentence))
print(token_cn(sentence))
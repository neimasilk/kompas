# Simple usage
from stanfordcorenlp import StanfordCoreNLP


sentence = "是北加州围绕旧金山湾和圣帕布罗湾河口的一片城市群"
with StanfordCoreNLP(r'C:/Users/amien_lab/PycharmProjects/kompas',lang='zh') as nlp:
    print(nlp.word_tokenize(sentence))
    print(nlp.pos_tag(sentence))
    print(nlp.ner(sentence))
    print(nlp.parse(sentence))
    print(nlp.dependency_parse(sentence))
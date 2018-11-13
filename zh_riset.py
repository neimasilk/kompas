# Simple usage
from stanford_segmenter import Segmenter


# some python file
seg = Segmenter()
sentence = "是北加州围绕旧金山湾和圣帕布罗湾河口的一片城市群"
print(seg.cn_segment(sentence))
# hasil segmenter : ['是', '北', '加州', '围绕', '旧金山湾', '和', '圣帕布罗湾', '河口', '的', '一', '片', '城市群']

# https: // github.com / moses - smt / mosesdecoder / blob / master / scripts / tokenizer / tokenizer.perl
#
# >> > tokenizer = MosesTokenizer()
# >> > text = u'This, is a sentence with weird\xbb symbols\u2026 appearing everywhere\xbf'
# >> > expected_tokenized = u'This , is a sentence with weird \xbb symbols \u2026 appearing everywhere \xbf'
# >> > tokenized_text = tokenizer.tokenize(text, return_str=True)
# >> > tokenized_text == expected_tokenized
# True
# >> > tokenizer.tokenize(text) == [u'This', u',', u'is', u'a', u'sentence', u'with', u'weird', u'\xbb', u'symbols',
#                                   u'\u2026', u'appearing', u'everywhere', u'\xbf']
# True
#
#
# >> > m = MosesTokenizer()
# >> > m.tokenize('abc def.')
# [u'abc', u'def', u'.']
#
# >> > m = MosesTokenizer()
# >> > m.tokenize('2016, pp.')
# [u'2016', u',', u'pp', u'.']
# 
# >> > sent = "This ain't funny. It's actually hillarious, yet double Ls. | [] < > [ ] & You're gonna shake it off? Don't?"
# >> > m.tokenize(sent, escape=True)
# ['This', 'ain', '&apos;t', 'funny', '.', 'It', '&apos;s', 'actually', 'hillarious', ',', 'yet', 'double', 'Ls', '.',
#  '&#124;', '&#91;', '&#93;', '&lt;', '&gt;', '&#91;', '&#93;', '&amp;', 'You', '&apos;re', 'gonna', 'shake', 'it',
#  'off', '?', 'Don', '&apos;t', '?']
# >> > m.tokenize(sent, escape=False)
# ['This', 'ain', "'t", 'funny', '.', 'It', "'s", 'actually', 'hillarious', ',', 'yet', 'double', 'Ls', '.', '|', '[',
#  ']', '<', '>', '[', ']', '&', 'You', "'re", 'gonna', 'shake', 'it', 'off', '?', 'Don', "'t", '?']
# """
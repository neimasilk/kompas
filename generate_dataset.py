# generate dataset baru bisa jalan kalau ada file wikipedia.txt yang harus digenerate dulu dari generator xxx


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import pickle

# import math
# import os
# import random
# import zipfile
#
# import numpy as np
# from six.moves import urllib
# from six.moves import xrange  # pylint: disable=redefined-builtin

filename = 'wikipedia.txt'


# Read the data into a list of strings.
def read_data(filename):
    """Extract the first file enclosed in a zip file as a list of words"""
    f = open(filename, 'rb')
    data = f.read().split()
    return data


words = read_data(filename)
print('Data size', len(words))

# Step 2: Build the dictionary and replace rare words with UNK token.
vocabulary_size = 100000


def build_dataset(words, vocabulary_size):
    count = [['UNK', -1]]
    count.extend(collections.Counter(words).most_common(vocabulary_size - 1))
    dictionary = dict()
    for word, _ in count:
        dictionary[word] = len(dictionary)
    data = list()
    unk_count = 0
    for word in words:
        if word in dictionary:
            index = dictionary[word]
        else:
            index = 0  # dictionary['UNK']
            unk_count += 1
        data.append(index)
    count[0][1] = unk_count
    reverse_dictionary = dict(zip(dictionary.values(), dictionary.keys()))
    return data, count, dictionary, reverse_dictionary


data, count, dictionary, reverse_dictionary = build_dataset(words, vocabulary_size)
del words  # Hint to reduce memory.
print('Most common words (+UNK)', count[:5])
print('Sample data', data[:10], [reverse_dictionary[i] for i in data[:10]])

with open('data_count_dictionary_reverse_dictionary.pkl', 'wb') as f:  # Python 3: open(..., 'wb')
    pickle.dump([data, count, dictionary, reverse_dictionary], f)

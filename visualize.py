
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import math
import os
import random
import zipfile

import numpy as np
from six.moves import urllib
from six.moves import xrange  # pylint: disable=redefined-builtin
import tensorflow as tf
import pickle


data_index = 0
with open('data_count_dictionary_reverse.pkl','rb') as f:  # Python 3: open(..., 'rb')
    data, count, dictionary, reverse_dictionary, final_embeddings = pickle.load(f)
    f.close()



def plot_with_labels(low_dim_embs, labels, filename='tsne.png'):
  assert low_dim_embs.shape[0] >= len(labels), "More labels than embeddings"
  plt.figure(figsize=(18, 18))  # in inches
  for i, label in enumerate(labels):
    x, y = low_dim_embs[i, :]
    plt.scatter(x, y)
    plt.annotate(label,
                 xy=(x, y),
                 xytext=(5, 2),
                 textcoords='offset points',
                 ha='right',
                 va='bottom')

  # plt.savefig(filename)
  plt.show()

try:
  from sklearn.manifold import TSNE
  import matplotlib.pyplot as plt



  # Getting back the objects:

  # with open('objs.pkl') as f:  # Python 3: open(..., 'rb')
  #     data, count, dictionary, reverse_dictionary, final_embeddings = pickle.load(f)

  tsne = TSNE(perplexity=30, n_components=2, init='pca', n_iter=5000)
  plot_only = 500
  low_dim_embs = tsne.fit_transform(final_embeddings[:plot_only, :])
  labels = [reverse_dictionary[i] for i in xrange(plot_only)]
  plot_with_labels(low_dim_embs, labels)

except ImportError:
  print("Please install sklearn, matplotlib, and scipy to visualize embeddings.")

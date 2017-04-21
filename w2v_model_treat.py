# https://radimrehurek.com/gensim/models/keyedvectors.html
# https://radimrehurek.com/gensim/models/word2vec.html

from gensim.models.keyedvectors import KeyedVectors
import logging
import numpy as np
import re

def load_w2v_model(file_name: str):
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    w2v_model = KeyedVectors.load_word2vec_format(file_name, binary=True, encoding='utf-8')
    print("word2vec model '%s' loaded" % file_name)
    return w2v_model

model = load_w2v_model("c:/data/ruscorpora.model.bin.gz")

spro_keys = [model.index2word[idx]
             for idx in range(len(model.index2word))
             if '_SPRO' in model.index2word[idx]]

apro_keys = [model.index2word[idx]
             for idx in range(len(model.index2word))
             if '_APRO' in model.index2word[idx]]

conj_keys = [model.index2word[idx]
             for idx in range(len(model.index2word))
             if '_CONJ' in model.index2word[idx]]

advpro_keys = [model.index2word[idx]
             for idx in range(len(model.index2word))
             if '_ADVPRO' in model.index2word[idx]]

part_keys = [model.index2word[idx]
             for idx in range(len(model.index2word))
             if '_PART' in model.index2word[idx]]   # ??

pr_keys = [model.index2word[idx]
           for idx in range(len(model.index2word))
           if '_PR' in model.index2word[idx]]


def clear_word(word):
    under_idx = word.find('_')
    return word[:under_idx] if under_idx >= 0 else word


def is_word_dirty(word, re_exp):
    under_idx = word.find('_')
    if under_idx >= 0:
        word = word[:under_idx].upper()
        if re.match(re_exp, word):
            return False
    return True


re_rus_word = re.compile('^[А-Я\-]+$')
dirty_keys = [model.index2word[idx]
              for idx in range(len(model.index2word))
              if is_word_dirty(model.index2word[idx], re_exp=re_rus_word)]

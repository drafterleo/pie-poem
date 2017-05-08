import pymorphy2
from gensim.models import KeyedVectors
import logging
import numpy as np
import heapq
import pickle
import re

grammar_map_MY_STEM = {
    'NOUN': '_S',
    'VERB': '_V', 'INFN': '_V', 'GRND': '_V', 'PRTF': '_V', 'PRTS': '_V',
    'ADJF': '_A', 'ADJS': '_A',
    'ADVB': '_ADV',
    'PRED': '_PRAEDIC'
}


# https://github.com/akutuzov/universal-pos-tags
grammar_map_POS_TAGS =  {
    'NOUN': '_NOUN',
    'VERB': '_VERB', 'INFN': '_VERB', 'GRND': '_VERB', 'PRTF': '_VERB', 'PRTS': '_VERB',
    'ADJF': '_ADJ', 'ADJS': '_ADJ',
    'ADVB': '_ADV',
    'PRED': '_ADP'
}


class PoemsModel:
    morph_analyzer = pymorphy2.MorphAnalyzer()

    def __init__(self, poems_model_file='', w2v_file=''):
        self.w2v = KeyedVectors()

        self.poems = []            # [str, str, ...]
        self.bags = []             # [[str, str, ...], ...]
        self.vocab = {}            # {word: count, ...}
        self.matrices = []         # [np.ndarray, ...]

        self.grammar_map = grammar_map_POS_TAGS

        if w2v_file:
            self.load_w2v_model(w2v_file)
        if poems_model_file:
            self.read(poems_model_file)

    def load_w2v_model(self, file_name: str):
        print("loading w2v_model...")
        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
        self.w2v = KeyedVectors.load_word2vec_format(file_name, binary=True, encoding='utf-8')
        print("word2vec model '%s' loaded" % file_name)

    def canonize_words(self, words: list) -> list:
        stop_words = ('быть', 'мой', 'наш', 'ваш', 'их', 'его', 'её', 'их',
                      'этот', 'тот', 'где', 'который', 'либо', 'нибудь', 'нет', 'да')

        normalized = []
        for w in words:
            forms = self.morph_analyzer.parse(w.lower())
            try:
                form = max(forms, key=lambda x: (x.score, x.methods_stack[0][2]))
            except Exception:
                form = forms[0]
                print(form)
            if not (form.tag.POS in ['PREP', 'CONJ', 'PRCL', 'NPRO', 'NUMR']
                    or 'Name' in form.tag
                    or 'UNKN' in form.tag
                    or form.normal_form in stop_words):  # 'ADJF'
                norm_word = form.normal_form.replace("ё", "е")
                normalized.append(norm_word + self.grammar_map.get(form.tag.POS, ''))
        return normalized

    def semantic_associations(self, bag: list, topn=10) -> list:
        positive_lst = [w for w in bag if w in self.w2v.vocab]
        if len(positive_lst) > 0:
            assoc_lst = self.w2v.most_similar(positive=positive_lst, topn=topn)
            return [a[0] for a in assoc_lst]
        else:
            print('empty association for bag:', bag)
            return ['пустота_S']

    def bag_to_matrix(self, bag: list):
        mx = []
        for i in range(len(bag)):
            try:
                mx.append(self.w2v[bag[i]])
            except:
                pass
        return np.vstack(mx) if len(mx) > 0 else np.array([])

    def read_poems(self, file_name: str):
        file = open(file_name, encoding='utf-8')
        lines = file.readlines()
        self.poems = []
        poem = ""
        for line in lines:
            if len(line.strip()) == 0:
                if len(poem.strip()) > 0:
                    self.poems.append(poem.lower())
                    poem = ""
            else:
                poem += line

    def make_bags(self, texts: list) -> (list, dict):
        bags = []
        vocabulary = {}
        for txt in texts:
            bag = []  # {}
            clear_txt = re.sub(r',|\.|!|\?|;|"|@|#|%|&|\*|\\|/|:|\+', ' ', txt)  # remove punctuation
            words = self.canonize_words(clear_txt.split())
            for w in words:
                if w not in bag:
                    bag.append(w)  # bag[w] = bag.get(w, 0) + 1
                vocabulary[w] = vocabulary.get(w, 0) + 1
            bags.append(bag)
        return bags, vocabulary

    def compile(self, poems_file: str = "", w2v_file: str = ""):
        if poems_file:
            self.read_poems(poems_file)
            print('poem count:', len(self.poems))

        print('making word bags...')
        self.bags, self.vocab = self.make_bags(self.poems)

        if w2v_file:
            self.load_w2v_model(w2v_file)
        print("model is compiled")

    def read(self, file_name: str):
        with open(file_name, mode='rb') as file:
            print('reading pickle poems model...')
            data = pickle.load(file)
            self.poems = data['poems']
            self.bags = data['bags']
            self.vocab = data['vocab']

            print("vectorizing model...")
            self.matrices = [self.bag_to_matrix(bag) for bag in self.bags]

            print('model is loaded')

    def write(self, file_name: str):
        with open(file_name, mode='wb') as file:
            data = {
                'poems': self.poems,
                'bags': self.bags,
                'vocab': self.vocab,
            }
            pickle.dump(data, file)

    def similar_poems_idx(self, query: str, topn=5) -> list:  # [(poem_idx, sim)]

        def semantic_similarity_fast(mx1: np.ndarray, mx2: np.ndarray) -> float:
            return np.sum(np.dot(mx1, mx2.T)) if len(mx1) > 0 and len(mx2) > 0 else 0.0

        def semantic_similarity_fast_log(mx1: np.ndarray, mx2: np.ndarray) -> float:
            return np.sum(np.dot(mx1, mx2.T)) * np.log10(len(mx2)) / len(mx2) \
                   if len(mx1) > 0 and len(mx2) > 0 else 0.0

        clear_query = re.sub(r',|\.|!|\?|;|"|@|#|%|&|\*|\\|/|:|\+', ' ', query)  # remove punctuation
        query_bag = self.canonize_words(clear_query.split())
        query_mx = self.bag_to_matrix(query_bag)
        if len(query_mx) == 0:
            return []
        similars = [(i, semantic_similarity_fast_log(query_mx, mx))
                    for i, mx in enumerate(self.matrices)]
        # similars.sort(key=lambda x: x[1], reverse=True)
        return heapq.nlargest(topn, similars, key=lambda x: x[1])

    def similar_poems(self, query: str, topn=5) -> list:  # [(poem, sim)]
        return [(self.poems[idx], sim)
                for idx, sim in self.similar_poems_idx(query, topn)]


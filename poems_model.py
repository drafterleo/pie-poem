import pymorphy2
from gensim.models import KeyedVectors
import logging
import numpy as np
import pickle

grammar_map_MY_STEM = {
    'NOUN': '_S',
    'VERB': '_V', 'INFN': '_V', 'GRND': '_V', 'PRTF': '_V', 'PRTS': '_V',
    'ADJF': '_A', 'ADJS': '_A',
    'ADVB': '_ADV',
    'PRED': '_PRAEDIC'
}

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
        self.bags = []             #
        self.vocab = {}            # {word: count, ...}
        self.associations = []     # [list, list, ...]

        self.grammar_map = grammar_map_POS_TAGS

        if w2v_file:
            self.load_w2v_model(w2v_file)
        if poems_model_file:
            self.read(poems_model_file)

    def load_w2v_model(self, file_name: str):
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
            words = self.canonize_words(txt.split())
            for w in words:
                if w not in bag:
                    bag.append(w)  # bag[w] = bag.get(w, 0) + 1
                vocabulary[w] = vocabulary.get(w, 0) + 1
            bags.append(bag)
        return bags, vocabulary

    def compile(self, poems_file: str, w2v_file: str):
        print("making poems model...")
        self.read_poems(poems_file)
        print('poem count:', len(self.poems))
        self.bags, self.vocab = self.make_bags(self.poems)
        print("loading w2v_model...")
        self.load_w2v_model(w2v_file)
        print("adding semantics to model...")
        self.associations = [self.semantic_associations(bag) for bag in self.bags]
        print("model is compiled")

    def read(self, file_name: str):
        with open(file_name, mode='rb') as file:
            data = pickle.load(file)
            self.poems = data['poems']
            self.bags = data['bags']
            self.vocab = data['vocab']
            self.associations = data['associations']

    def write(self, file_name: str):
        with open(file_name, mode='wb') as file:
            data = {
                'poems': self.poems,
                'bags': self.bags,
                'vocab': self.vocab,
                'associations': self.associations
            }
            pickle.dump(data, file)

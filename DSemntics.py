import gensim
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

DATA_DIR = 'C:/TEMP/data/'
model = gensim.models.Word2Vec.load_word2vec_format(DATA_DIR + "ruwikiruscorpora.model.bin.gz",
                                                    binary=True, encoding='utf-8')

# print(model.similarity('муж_S', 'жена_S'))
model.most_similar(positive=['человек_S', 'семья_S'], negative=['община_S'])
model.most_similar(positive=['париж_S', 'германия_S'], negative=['франция_S'])
model.most_similar(positive=['москва_S', 'государство_S'], negative=[])

# sentences = [['first sentence'], ['second', 'sentence']]
# train word2vec on the two sentences
# model = gensim.models.Word2Vec(sentences, min_count=1)

def semaintic_dencity(bag: list) -> int:
    if len(bag) == 0:
        return
    ss = 0.0
    bag_set = list(set(bag)) # remove duplicates
    for i in range(len(bag)):
        for j in range(i+1, len(bag)):
            try:
                ss += model.similarity(bag_set[i], bag_set[j])
            except Exception:
                continue
    return ss / len(bag_set)

import gensim
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

DATA_DIR = 'C:/TEMP/data/'
model = gensim.models.Word2Vec.load_word2vec_format(DATA_DIR + "ruscorpora.model.bin.gz",
                                                    binary=True, encoding='utf-8')

# print(model.similarity('муж_S', 'жена_S'))
model.most_similar(positive=['человек_S', 'семья_S'], negative=['община_S'])
model.most_similar(positive=['париж_S', 'германия_S'], negative=['франция_S'])
model.most_similar(positive=['москва_S', 'государство_S'], negative=[])

# sentences = [['first sentence'], ['second', 'sentence']]
# train word2vec on the two sentences
# model = gensim.models.Word2Vec(sentences, min_count=1)


def semantic_density(bag: list, unknown_coef=0.00001) -> int:
    bag_set = list(set(bag))  # remove duplicates
    bag_set_len = len(bag_set)
    if bag_set_len < 2:
        return 0.0
    sim_sum = 0.0
    weight_sum = 0.0
    for i in range(bag_set_len):
        for j in range(i+1, bag_set_len):
            weight = 2/(j - i)
            weight_sum += weight
            try:
                sim = model.similarity(bag_set[i], bag_set[j])
                if sim < 0:
                    sim_sum = unknown_coef * weight
                else:
                    sim_sum += model.similarity(bag_set[i], bag_set[j]) * weight
            except Exception:
                sim_sum += unknown_coef * weight
    return sim_sum / weight_sum


import make_data_model as mdm
pm = mdm.read_data_model("data_model.dat")
sd = [semantic_density(bag, unknown_coef=0.0001) for bag in pm['bags']]
sd = enumerate(sd)
lsd = list(sd)
lsd.sort(key=lambda x: x[1])
for i in range(1, 10): print(pm['poems'][lsd[-i][0]], lsd[-i][1])
for i in range(0, 10): print(pm['poems'][lsd[i][0]], lsd[i][1])

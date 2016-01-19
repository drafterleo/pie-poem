import gensim
import logging
import data_model as dm

WORD2VEC_MODEL_FILE = 'C:/TEMP/data/ruscorpora.model.bin.gz'

# print(model.similarity('муж_S', 'жена_S'))
# model.most_similar(positive=['человек_S', 'семья_S'], negative=['община_S'])
# model.most_similar(positive=['париж_S', 'германия_S'], negative=['франция_S'])
# model.most_similar(positive=['москва_S', 'государство_S'], negative=[])

# sentences = [['first sentence'], ['second', 'sentence']]
# train word2vec on the two sentences
# model = gensim.models.Word2Vec(sentences, min_count=1)

def load_w2v_model(file_name: str):
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    w2v_model = gensim.models.Word2Vec.load_word2vec_format(file_name, binary=True, encoding='utf-8')
    return w2v_model


def semantic_density(bag: list, w2v_model, unknown_coef=0.0) -> int:
    bag_len = len(bag)
    if bag_len < 2:
        return 0.0
    sim_sum = 0.0
    weight_sum = 0.0
    for i in range(0, bag_len):
        for j in range(i+1, bag_len):
            if bag[i] != bag[j]:
                weight = 1/(j-i)
                weight_sum += weight
                try:
                    sim_sum += w2v_model.similarity(bag[i], bag[j]) * weight
                except Exception:
                    sim_sum += unknown_coef * weight
    return sim_sum / weight_sum


def semantic_association(bag: list, w2v_model) -> list:
    positive_lst = [w for w in bag if w in w2v_model.vocab]
    assoc_lst = w2v_model.most_similar(positive=positive_lst, topn=10)
    return [a[0] for a in assoc_lst]


def append_semantics_to_model(file_name: str) -> dict:
    print("loading poems model...")
    pm = dm.read_data_model(file_name)

    print("loading w2v_model...")
    w2v_model = load_w2v_model(WORD2VEC_MODEL_FILE)

    print("adding semantics to poems model...")
    sd = [semantic_density(bag, w2v_model, unknown_coef=-0.001)
          for bag in pm['bags']]
    sa = [semantic_association(bag, w2v_model)
          for bag in pm['bags']]

    pm['density'] = sd
    pm['associations'] = sa

    dm.write_data_model(file_name, pm)
    return pm


def print_poems_by_density(poems_model: dict):
    sd = poems_model['density']
    sa = poems_model['associations']
    lsd = list(enumerate(sd))
    lsd.sort(key=lambda x: x[1])
    for i in range(1, 10):
        print(poems_model['poems'][lsd[-i][0]], lsd[-i][1])
        print(poems_model['bags'][lsd[-i][0]])
        print(sa[lsd[-i][0]], "\n")
    for i in range(0, 10):
        print(poems_model['poems'][lsd[i][0]], lsd[i][1])
        print(poems_model['bags'][lsd[i][0]])
        print(sa[lsd[i][0]], "\n")


if __name__ == "__main__":
    pm = append_semantics_to_model("poems_model.dat")
    print_poems_by_density(pm)


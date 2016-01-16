import gensim
import logging
import data_model as dm

DATA_DIR = 'C:/TEMP/data/'


# print(model.similarity('муж_S', 'жена_S'))
# model.most_similar(positive=['человек_S', 'семья_S'], negative=['община_S'])
# model.most_similar(positive=['париж_S', 'германия_S'], negative=['франция_S'])
# model.most_similar(positive=['москва_S', 'государство_S'], negative=[])

# sentences = [['first sentence'], ['second', 'sentence']]
# train word2vec on the two sentences
# model = gensim.models.Word2Vec(sentences, min_count=1)


def semantic_density(bag: dict, w2v_model, unknown_coef=0.0) -> int:
    bag_lst = list(bag.keys())
    bag_lst_len = len(bag_lst)
    if bag_lst_len < 2:
        return 0.0
    sim_sum = 0.0
    for i in range(0, bag_lst_len):
        for j in range(i+1, bag_lst_len):
            try:
                sim_sum += w2v_model.similarity(bag_lst[i], bag_lst[j])
            except Exception:
                sim_sum += unknown_coef
    return sim_sum


def semantic_association(bag: dict, w2v_model) -> list:
    positive_lst = [w for w in bag.keys() if w in w2v_model.vocab]
    assoc_lst = w2v_model.most_similar(positive=positive_lst, topn=10)
    return [a[0] for a in assoc_lst]


def append_semantics_to_model(file_name: str):
    print("loading poems model...")
    pm = dm.read_data_model(file_name)

    print("loading w2v_model...")
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    w2v_model = gensim.models.Word2Vec.load_word2vec_format(DATA_DIR + "ruscorpora.model.bin.gz",
                                                    binary=True, encoding='utf-8')

    print("adding semantics to poems model...")
    sd = [semantic_density(bag, w2v_model, unknown_coef=-0.001)
          for bag in pm['bags']]
    sa = [semantic_association(bag, w2v_model)
          for bag in pm['bags']]

    pm['sem_density'] = sd
    pm['sem_associations'] = sa

    dm.write_data_model(file_name, pm)

    # lsd = list(enumerate(sd))
    # lsd.sort(key=lambda x: x[1])
    # for i in range(1, 10):
    #     print(pm['poems'][lsd[-i][0]], lsd[-i][1])
    #     print(pm['bags'][lsd[-i][0]])
    #     print(sa[lsd[-i][0]], "\n")
    # for i in range(0, 10):
    #     print(pm['poems'][lsd[i][0]], lsd[i][1])
    #     print(pm['bags'][lsd[i][0]])
    #     print(sa[lsd[i][0]], "\n")


# if __name__ == "__main__":
    # append_semantics_to_model("poems_model.dat")


import gensim
import logging

# http://ling.go.mail.ru/static/models/ruscorpora.model.bin.gz
WORD2VEC_MODEL_FILE = 'C:/TEMP/data/ruscorpora.model.bin.gz'


def load_w2v_model(file_name: str):
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    w2v_model = gensim.models.Word2Vec.load_word2vec_format(file_name, binary=True, encoding='utf-8')
    print("model '%s' loaded" % file_name)
    return w2v_model


def semantic_density(bag: list, w2v_model, unknown_coef=0.0) -> float:
    sim_sum = 0.0
    divisor = 0
    # weight_sum = 0.0
    for i in range(len(bag)):
        for j in range(i + 1, len(bag)):
            if bag[i] != bag[j]:
                divisor += 1
                # weight = 1 / (j - i)
                # weight_sum += weight
                try:
                    sim_sum += w2v_model.similarity(bag[i], bag[j]) # * weight
                except Exception:
                    sim_sum += unknown_coef # * weight
    return sim_sum / divisor # / weight_sum


def semantic_similarity(bag1, bag2: list, w2v_model, unknown_coef=0.0) -> float:
    sim_sum = 0.0
    for i in range(len(bag1)):
        for j in range(len(bag2)):
            try:
                sim_sum += w2v_model.similarity(bag1[i], bag2[j])
            except Exception:
                sim_sum += unknown_coef
    return sim_sum / (len(bag1) * len(bag2))


def semantic_association(bag: list, w2v_model) -> list:
    positive_lst = [w for w in bag if w in w2v_model.vocab]
    assoc_lst = w2v_model.most_similar(positive=positive_lst, topn=10)
    return [a[0] for a in assoc_lst]







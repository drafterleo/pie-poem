import random as rnd
import data_model as dm


# data model format
#   {'poems': [str, str, ...]
#    'bags': [list, list, ...]
#    'vocabulary': {word: count, ...}
#    'density': [float, float, ...]    <- append_semantics module
#    'associations: [list, list, ...]
#    'rate': [float, float, ...]       <- markupform module


def read_poems(file_name: str) -> list:
    file = open(file_name, encoding='utf-8')
    lines = file.readlines()
    poems = []
    poem = ""
    for line in lines:
        if len(line.strip()) == 0:
            if len(poem.strip()) > 0:
                poems.append(poem.lower())
                poem = ""
        else:
            poem += line
    return poems


def make_bags(texts: list) -> list:
    bags = []
    vocabulary = {}
    for txt in texts:
        bag = []  # {}
        words = dm.canonize_words(txt.split())
        for w in words:
            bag.append(w)  # bag[w] = bag.get(w, 0) + 1
            vocabulary[w] = vocabulary.get(w, 0) + 1
        bags.append(bag)
    return bags, vocabulary


def make_data_model(file_name: str) -> dict:
    poems = read_poems(file_name)
    bags, voc = make_bags(poems)
    return {'poems'     : poems,
            'bags'      : bags,
            'vocabulary': voc}


if __name__ == "__main__":
    poems = read_poems("poems.txt")
    print(len(poems))
    poem = rnd.choice(poems)
    print(poem)
    print(dm.canonize_words(poem.split()))
    pmodel = make_data_model("poems.txt")
    print(pmodel)
    dm.write_data_model("poems_model.dat", pmodel)




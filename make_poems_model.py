import random as rnd
import data_model as dm
import semantics as sem

# data model format
#   {'poems': [str, str, ...]
#    'bags': [list, list, ...]
#    'vocabulary': {word: count, ...}
#    'density': [float, float, ...]
#    'associations: [list, list, ...]
#    'rates': [float, float, ...]       <- markupform module


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


def make_bags(texts: list) -> (list, dict):
    bags = []
    vocabulary = {}
    for txt in texts:
        bag = []  # {}
        words = dm.canonize_words(txt.split())
        for w in words:
            if w not in bag:
                bag.append(w)  # bag[w] = bag.get(w, 0) + 1
            vocabulary[w] = vocabulary.get(w, 0) + 1
        bags.append(bag)
    return bags, vocabulary


def make_data_model(file_name: str) -> dict:
    print("making poems model...")
    poems = read_poems(file_name)
    bags, voc = make_bags(poems)
    print("loading w2v_model...")
    w2v_model = sem.load_w2v_model(sem.WORD2VEC_MODEL_FILE)
    print("adding semantics to model...")
    sd = [sem.semantic_density(bag, w2v_model, unknown_coef=-0.001) for bag in bags]
    sa = [sem.semantic_association(bag, w2v_model) for bag in bags]
    rates = [0.0 for _ in range(len(poems))]
    return {'poems'       : poems,
            'bags'        : bags,
            'vocabulary'  : voc,
            'density'     : sd,
            'associations': sa,
            'rates'       : rates}

def append_model_to_model(head_model, tail_model):
    for w in tail_model['vocabulary'].keys():
        head_model['vocabulary'][w] = head_model['vocabulary'].get(w, 0) + tail_model['vocabulary'][w]
    for i in range(len(tail_model['poems'])):
        if tail_model['bags'][i] not in head_model['bags']:
            head_model['poems'].append(tail_model['poems'][i])
            head_model['bags'].append(tail_model['bags'][i])
            head_model['density'].append(tail_model['density'][i])
            head_model['associations'].append(tail_model['associations'][i])
            head_model['rates'].append(tail_model['rates'][i])
        else:
            print('<!!!>\n', tail_model['poems'][i])

def print_poems_model(poems_model):
    print("poems: ", poems_model['poems'])
    print("bags: ", poems_model['bags'])
    print("vocabulary: ", poems_model['vocabulary'])
    print("density: ", poems_model['density'])
    print("associations: ", poems_model['associations'])
    print("rates: ", poems_model['rates'])


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
    poems = read_poems("poems.txt")
    print(len(poems))
    poem = rnd.choice(poems)
    print(poem)
    print(dm.canonize_words(poem.split()))
    pm = make_data_model("poems.txt")
    # print(pm)
    pm_file = "poems_model.dat"
    dm.write_data_model(pm_file, pm)
    print("model was saved to file '%s'" % pm_file)
    print_poems_model(pm)

# import data_model as dm
# pm = dm.read_data_model("poems_model.dat")
# print_poems_by_density(pm)




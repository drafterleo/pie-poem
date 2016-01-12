import pymorphy2
import random as rnd


# http://textmechanic.com/text-tools/basic-text-tools/remove-duplicate-lines/
# http://www.codeisart.ru/blog/python-shingles-algorithm/
def canonize_words(words: list) -> list:
    # stop_words = ('быть')
    morph = pymorphy2.MorphAnalyzer()
    normalized = []
    for i in words:
        forms = morph.parse(i)
        try:
            form = max(forms, key=lambda x: (x.score, x.methods_stack[0][2]))
        except Exception:
            form = forms[0]
            print(form)
        if not (form.tag.POS in ['PREP', 'CONJ', 'PRCL', 'NPRO']
                or 'Name' in form.tag or 'UNKN' in form.tag):  # 'ADJF'
            normalized.append(form.normal_form)
    return normalized  # [w for w in normalized if w not in stop_words]


def read_poems(file_name: str) -> list:
    file = open(file_name, encoding='utf-8')
    lines = file.readlines()
    poems = []
    poem = ""
    for line in lines:
        if len(line.strip()) == 0:
            if len(poem.strip()) > 0:
                poems.append(poem)
                poem = ""
        else:
            poem += line
    return poems


def make_bags(texts: list) -> list:
    bags = []
    vocabulary = {}
    for txt in texts:
        bag = {}
        words = canonize_words(txt.split())
        for w in words:
            bag[w] = bag.get(w, 0) + 1
            vocabulary[w] = vocabulary.get(w, 0) + 1
        bags.append(bag)
    return bags, vocabulary


if __name__ == "__main__":
    poems = read_poems("poems.txt")
    poem = rnd.choice(poems)
    print(poem)
    print(canonize_words(poem.split()))
    bags, voc = make_bags(poems)
    print(bags)
    print(voc)




import semantics as sem
import make_poems_model as mpm
import analyze_poem as ap
from pprint import pprint

w2v = sem.load_w2v_model("c:/data/ruscorpora.model.bin.gz")
pm = mpm.load_poems_model("poems_model.dat", w2v, vectorize=True)
pprint(ap.similar_poems("запрос", pm, w2v, topn=5, use_associations=False))

sem.most_similar(w2v, positive="ёжик", negative="причёска")
w2v.similarity("принцесса_S", "чудовище_S")
w2v.most_similar(positive=['латифундия_S'])

# w2v.index2word
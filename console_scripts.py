import semantics as sem
import make_poems_model as mpm
import analyze_poem as ap
from pprint import pprint

w2v_model = sem.load_w2v_model("c:/data/ruscorpora.model.bin.gz")
poems_model = mpm.load_poems_model("poems_model.dat", w2v_model, vectorize=True)
pprint(ap.similar_poems("запрос", poems_model, w2v_model, topn=5, use_associations=False))

sem.most_similar(w2v_model, positive="ёжик", negative="причёска")
w2v_model.similarity("принцесса_S", "чудовище_S")
w2v_model.most_similar(positive=['латифундия_S'])

# w2v.index2word
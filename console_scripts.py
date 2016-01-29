import semantics as sem
import data_model as dm
import analyze_poem as ap
from pprint import pprint

w2v = sem.load_w2v_model("c:/temp/data/ruscorpora.model.bin.gz")
pm = dm.read_data_model("poems_model.dat")
pprint(ap.similar_poems("запрос", pm, w2v))

w2v.similarity("принцесса_S", "чудовище_S")

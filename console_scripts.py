import semantics as sem
import data_model as dm
from pprint import pprint
from analyze_poem import *

w2v = sem.load_w2v_model(sem.WORD2VEC_MODEL_FILE)
pm = dm.read_data_model("poems_model.dat")
pprint(similar_poems("запрос", pm, w2v))

w2v.similarity("принцесса_S", "чудовище_S")

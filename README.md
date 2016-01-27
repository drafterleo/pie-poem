Чтобы поработать с моделью (poems_model.dat), следует загрузить в консоль питона содержимое console_scripts.py.

Сначала импорты (нужно, чтобы были установлены json, pymorphy2, gensim):
```python
import semantics as sem
import data_model as dm
from pprint import pprint
from analyze_poem import *
```
Потом вгрузить word2vec модель (занимает некоторое время), модели скачивал c [RusVectōrēs] (http://ling.go.mail.ru/dsm/ru/about#models)
```python
w2v = sem.load_w2v_model("c:/temp/data/ruscorpora.model.bin.gz") # указать путь до word2vec модели
```
Затем:
```python
pm = dm.read_data_model("poems_model.dat") # загрузить пирожковую модель
pprint(similar_poems("запрос", pm, w2v, topn=5)) # 5 наиболее близких к "запросу" пирожка
```

[Развёрнутый пример] (https://github.com/drafterleo/pie-poem/blob/master/example.ipynb) в формате блокнота IPython. 

P.S. Прошу простить за "ручной привод" - это экспериментальный проект, поиграться с модельками - на разработку "коробки автомат", к сожалению, не хватает времени.


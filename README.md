Чтобы поработать с моделью (poems_model.dat), следует загрузить в консоль питона содержимое [console_scripts.py] (https://github.com/drafterleo/pie-poem/blob/master/console_scripts.py)

Сначала импорты (также необходимы [pymorphy2](https://pymorphy2.readthedocs.org/en/latest/) и [gensim](https://radimrehurek.com/gensim/)):
```python
import semantics as sem
import make_poems_model as mpm
import analyze_poem as ap
from pprint import pprint
```
Потом вгрузить word2vec модель (занимает некоторое время), модели скачивал c [RusVectōrēs](http://ling.go.mail.ru/dsm/ru/about#models) (правда, у них периодически меняются грамматические суффиксы в словаре - поэтому, чтобы всё заработало, лучше [скачать](https://drive.google.com/open?id=0BynncCwFMx15cTIzM3M5bUl4S1k) модель, которая используется в примерах).
```python
w2v = sem.load_w2v_model("c:/temp/data/ruscorpora.model.bin.gz") # указать путь до файла word2vec модели
```
Затем:
```python
# загрузить пирожковую модель
pm = mpm.load_poems_model("poems_model.dat", w2v)

# распечатать 5 наиболее близких к "запросу" пирожка
pprint(ap.similar_poems("запрос", pm, w2v, topn=5)) 
```

[Развёрнутый пример](https://github.com/drafterleo/pie-poem/blob/master/example.ipynb) в формате блокнота IPython. 

[poems.csv](https://github.com/drafterleo/pie-poem/blob/master/poems.csv) - база [Поэтория](http://poetory.ru/) (любезно предоставил Иван Безденежных). Формат: [стишок, рейтинг]. 

P.S. Прошу простить за "ручной привод" - это экспериментальный проект, поиграться с модельками - на разработку "коробки автомат", к сожалению, не хватает времени.


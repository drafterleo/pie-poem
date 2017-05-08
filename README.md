
Необходимы [pymorphy2](https://pymorphy2.readthedocs.org/en/latest/) и [gensim](https://radimrehurek.com/gensim/)

Создать экземпляр PoemsModel и загрузить модели.<br>
Word2vec модель скачивал отсюда: http://rusvectores.org/ru/models/
```python
from poems_model import PoemsModel

poems_data = 'poems_model.pickle'
w2v_file = 'c:/data/ruscorpora_1_300_10.bin.gz'

pm = PoemsModel(poems_data, w2v_file)
```
Сформулировать запрос:
```python
pm.similar_poems('иллюзия', topn=10)
```

[Развёрнутый пример](https://github.com/drafterleo/pie-poem/blob/master/example.ipynb) в формате блокнота IPython. 

[poems.csv](https://github.com/drafterleo/pie-poem/blob/master/poems.csv) - база [Поэтория](http://poetory.ru/) (любезно предоставил Иван Безденежных). Формат: [стишок, рейтинг]. 



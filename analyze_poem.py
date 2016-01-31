import semantics as sem
import data_model as dm
import random as rnd
from pprint import pprint


def similar_poems_idx(query: str, poem_model, w2v_model, topn=5, use_associations=False) -> list:
    query_bag = dm.canonize_words(query.split())
    if use_associations:
        query_bag += sem.semantic_association(query_bag, w2v_model, topn=5)
        similars = [(i, sem.semantic_similarity_fast(query_bag, bag + poem_model['associations'][i], w2v_model))
                    for i, bag in enumerate(poem_model['bags'])]
    else:
        similars = [(i, sem.semantic_similarity_fast(query_bag, bag, w2v_model))
                    for i, bag in enumerate(poem_model['bags'])]
    similars.sort(key=lambda x: x[1], reverse=True)
    return similars[:topn]


def similar_poems(query: str, poem_model, w2v_model, topn=5, use_associations=False) -> list:
    return [(poem_model['poems'][idx], sim)
            for idx, sim in similar_poems_idx(query, poem_model, w2v_model, topn, use_associations)]


def rate_poem(poem: str, poem_model: dict, w2v_model, nearest=20) -> float:
    similars = similar_poems_idx(poem, poem_model, w2v_model, nearest)
    res_rate = 0.0
    sim_sum = 0.0
    for idx, sim in similars:
        rate = poem_model['rates'][idx]
        if sim > 0:
            res_rate += rate * sim
            sim_sum += sim
    if sim_sum > 0:
        return res_rate / sim_sum
    else:
        return 0.0


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
    test_poems = (
        "мадам а не хотите кофе\n сказал он глядя ей в глаза\n три таракана были против\n пять за\n",
        "в ночи повеяло прохладой\n как будто в дом прокралось зло\n а это просто одеяло сползло\n",
        "на юг летят все птицы в мире\n едва лишь осень на порог\n одни пингвины не летают\n пингвинам некуда лететь\n",
        "лежу у самой кромки моря\n немножко пьяный ну и пусть\n то море на меня накатит\n то грусть\n",
        "олег купил в мясном отделе\n кило можроженных сердец\n и с упоеньем разбивал их\n подлец\n",
        "мдам я весь пылаю страстью\n отдайтесь мне среди осин\n я очарован цветом ваших\n лосин\n",
        "автобус сделал остановку\n открылась дверь в густой туман\n и я сошла легко и ловко\n с ума",
        "когда одна осталась пуля\n а ты врагами окружен\n стреляй последней пулей в солнце\n и уходи пока темно\n",
        "горячий чай с пломбиром вместе\n ты ешь смотря цинично вдаль\n скажи дружочек а не треснет\n эмаль",
        "на почту бабушки слетелись\n воркуют топчатся голдят\n наверно крошек в виде пенсий\n хотят\n",
        "детей кому нибудь подарим\n беспечно отмахнулся пётр\n так был решён вопрос со свадьбой\n с опасным сексом и вобще\n",
        "жених идёт и пышет жаром\n и все невесты на селе\n к нему подходят чтоб погреться\n кто посмелее прикурить\n",
        "олег оксану в чистом поле\n случайно в полночь повстречал\n и легкомысленно кого-то\n зачал\n",
        "зима бежишь с горы кататься\n наперекор своей судьбе\n и кажется что минус двадцать\n тебе\n",
        "у истины довольно много\n начал концов и середин\n зато в тупик всегда заходишь\n в один\n",
        "чтоб жизнь свою наполнить смыслом\n из вздохов шерсти и тоски\n старушки каждодневно вяжут\n носки\n",
        "цветы засушенные в книге\n помада в сумке шоколад\n олег слегка волнуясь прибыл\n в стройбат\n",
        "поэт закажет проститутку\n и ночь проводит с ней в стихах\n та иитирует восторги\n ох ах\n",
        "маньяк насилует людмилу\n четвёртый час четвёртый раз\n людмила думает вот суки\n про бывших трёх своих мужей\n",
        "иван семёныч дерзкий грубый\n брутальный весь такой мужик\n помадой нежно красит губы\n привык\n"
    )

    w2v = sem.load_w2v_model(sem.WORD2VEC_MODEL_FILE)
    pm = dm.read_data_model("poems_model.dat")
    test_poem = rnd.choice(test_poems)
    sim_poems = similar_poems(test_poem, pm, w2v)
    print(test_poem)
    pprint(sim_poems)

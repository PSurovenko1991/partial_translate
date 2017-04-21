from transl import trans
import pymorphy2
from collections import Counter



# получить корпус +
# с помощью pymorphy2 перевести все слова в нормальные формы +
# с помощью heapq найдем N наиболее часто встречающихся в тексте слов по формуле. N = длинна корипуса/250/2 +
# получим индексы наиболее встречающихся слов в нормализованном корпусе +

 # * - найти индекс - начало вставки переведенного слова???

# по индексам сохраним формы слов из первоначального корпуса
# совершим перевод часто встречающихся слов +
# СОХРАНИМ переведенные слова в словарь
# по индексам совершим подстановку переведенных слов в первоначальный корпус
# по индексам и ранее сохраненным формам слов(п6) совершим преобразование переведенных слов в нужную смысловую форму
# из списка получим строку - Результат.



f = open("file.txt","r")
s = f.read()
f.close()


def form_corp(s): # формируем корпус из строки, заменяя переводы строки на "**"
    corp = s.replace("\n", " ** ").split(" " )
    return corp

def normform(s):
    s1 = [] # список форм слов начального корпуса
    s2 = [] # список приведенный в нормальную форму
    morph = pymorphy2.MorphAnalyzer()
    for i in s:
        #s1.append(morph.parse(i)[0].tag)
        s2.append(morph.parse(i)[0].normal_form)
    return (s2)

def top_word(s): #получаем наиболее часто встречающиеся слова
    tw = Counter(s).most_common(10) #(int(len(s)/250/2))
    return tw

def id_tw(s,s1):  # s - top_word, s1 - normform - запоминаем индексы наиболее часто встречающихся элементов
    s2 =[]
    for i in range(len(s)):
        s2.append([s[i][0]])
        for j in range(len(s1)):
            if s[i][0] == s1[j]:
                s2[i].append(j)
    return s2









def trans_spis(s): #принимает список, возвращает переведенный
    di = {}
    for i in range(len(s)):
        di.update({ s[i] : trans(s[i]) })
    return di

def splinstr(s):    #переводим список обратно в строку, учитывая переносы строки( ** )
    st = " ".join(s)
    stro = st.replace(" ** ","\n")
    return stro





def main(s):
     print(top_word(normform(form_corp(s))))

     print(id_tw(top_word(normform(form_corp(s))),normform(form_corp(s))))



if __name__ == "__main__":
    main(s)

from transl import trans
import pymorphy2
from collections import Counter
from breakd import breakdown
import copy

# получить корпус +
# с помощью pymorphy2 перевести все слова в нормальные формы +
# с помощью heapq найдем N наиболее часто встречающихся в тексте слов по формуле. N = длинна корипуса/250/2 +
# получим индексы наиболее встречающихся слов в нормализованном корпусе +
# Упорядочим частовустречающиеся слова по принципу "заменяем, исключая наибольшие потери в будущем" - breakdown
# найти индекс - начало вставки переведенного слова+

# по индексам сохраним формы слов из первоначального корпуса*
# совершим перевод часто встречающихся слов +
# СОХРАНИМ переведенные слова в словарь
# по индексам совершим подстановку переведенных слов в первоначальный корпус
# по индексам и ранее сохраненным формам слов(п6) совершим преобразование переведенных слов в нужную смысловую форму
# из списка получим строку - Результат.
# юзаем data['CountryID'] = pd.factorize(data.Country)[0] для сокращенния времени работы ???


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
    tw = Counter(s).most_common(17) #(int(len(s)/350))
    return tw

def get_index_tw(s,s1):  # s - top_word, s1 - normform - запоминаем индексы наиболее часто встречающихся элементов
    s2 =[]
    for i in range(len(s)):
        s2.append([s[i][0]])
        for j in range(len(s1)):
            if s[i][0] == s1[j]:
                s2[i].append(j)
    return s2 # индексы наиболее часто встречающихся слов


def get_first_index(s, s1): # s - список упорядоченных ТВ (OrdonoTW),s1 - список индексов(IndexTW) / принимает списокупорядоченных слов,
    s3=[]
    x=0
    for i in range(len(s)):
        for i1 in range(len(s1)):
            if s1[i1][0] == s[i]:
                for i2 in range(1,len(s1[i1])):
                    if s1[i1][i2]>x:
                        s3.append((s[i],s1[i1][i2]))
                        x=x+40#250
                        break
    return s3






# def nach_ins(s): #возвращает среднее расстояние между элементами
#     s2 =[]
#     for i in s:
#         s1 =0
#
#         for j in range(len(i)):
#             if j == 0:
#                 pass
#             else:
#                 if j< (len(i)-1):
#                     s1 = s1+(i[j]-i[j+1])
#         s1 = int(abs(s1/(len(i)-1)))
#         s2.append(s1)
#     return s2

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
    Logejo = form_corp(s) # получили корпус из строки /list
    # print(Logejo[0:30])

    NFlogejo = normform(Logejo) # Получили список слов в нормальной форме /list
    # print(NFlogejo[0:30])

    TopWordLog = (top_word(NFlogejo)) # Получили топовые слова нормального корпуса /list
    # print("Topword: ",TopWordLog)

    IndexTW = get_index_tw(TopWordLog, NFlogejo) # получили индексы часто встречающихся слов /list
    print("IndexTW: ",IndexTW)
    IndexTW1 = copy.deepcopy(IndexTW) # создаем копию т.к. объект IndexTW1 ,будет изменен в процессе выполнения breakdown(fuck encapsulation)

    OrdonoTW= breakdown(NFlogejo,TopWordLog,IndexTW1) # получили список слов для замены упорядоченный функцией breakdown /list
    print("OrdonoTW: ",OrdonoTW)

    FirstIndex = get_first_index(OrdonoTW, IndexTW) # получили начальные индексы для вставки слов
    print("first index: ",FirstIndex)




    # print(len(form_corp(s)))
    # print(p)

    #  print(nach_ins(ix_tw(p, p1)))


if __name__ == "__main__":
    main(s)

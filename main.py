
f = open("file.txt","r")
s = f.read()
f.close()


def form_corp(s): # формируем корпус из строки, заменяя переводы строки на "**"
    corp = s.replace("\n", " ** ").split(" " )
    return corp

def get_spis(s): #принимает строку в виде списка, возвращает список без повторяющихся элементов
    s1=[]
    for i in s:
        if i not in s1:
            s1.append(i)
    return s1

def get_dict(s,s1):     # принимает на вход основной список(Fcorp) и без повторяющихся(Gspis)
                       # возвращает словарь(слово:количество вхождений в текст)
    di = {}
    for i in range(len(s1)):
        kolvo = 0
        i1 = s1[i]
        for j in range(len(s)):
            if i1 == s[j]:
                kolvo = kolvo+1
        di[i1] = kolvo
    return di

def splinstr(s):    #переводим список обратно в строку, учитывая переносы строки( ** )
    st = " ".join(s)
    stro = st.replace(" ** ","\n")
    return stro





def main(s):
    e = get_dict(form_corp(s),get_spis(form_corp(s)))
    ...
    print(e)

if __name__ == "__main__":
    main(s)
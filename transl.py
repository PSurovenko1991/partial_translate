from textblob import TextBlob

def trans0(text1):
    import requests
    url = 'https://translate.yandex.net/api/v1.5/tr.json/translate?'
    key = 'trnsl.1.1.20170412T082822Z.106aadd2c087fc91.dfdbc4cde60d6cd54d9cd5b764ab06c27a4fd4bd'
    text = text1
    lang = 'ru-en'
    r = requests.post(url, data={'key': key, 'text': text, 'lang': lang})
    *_,t,_ = (r.text).split('"')
    # Выводим результат
    return (t)

def trans1(text,l): # l = language
    text1 = TextBlob(text)
    text2 = text1.translate(to=l)
    return (text2)


if __name__ == "__main__":
    x = input("введите текст для перевода(ru-en): ")
    print(trans1(x))

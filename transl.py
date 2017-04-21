


def trans(text1):
    import requests
    url = 'https://translate.yandex.net/api/v1.5/tr.json/translate?'
    key = ''
    text = text1
    lang = 'ru-en'
    r = requests.post(url, data={'key': key, 'text': text, 'lang': lang})
    *_,t,_ = (r.text).split('"')
    # Выводим результат
    return (t)

if __name__ == "__main__":
    x = input("введите текст для перевода(ru-en): ")
    print(trans(x))
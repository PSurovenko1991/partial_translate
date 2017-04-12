import requests
url = 'https://translate.yandex.net/api/v1.5/tr.json/translate?'
key = 'ВАШ API КЛЮЧ'
text = 'ТЕКСТ ДЛЯ ПЕРЕВОДА'
lang = 'ru-en'
r = requests.post(url, data={'key': key, 'text': text, 'lang': lang})
# Выводим результат
print(r.text)
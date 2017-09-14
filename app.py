from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
import os
import core



UPLOAD_FOLDER = 'files/'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/') #@app.route('/upload')              # Отображаем начальную страницу загрузки
def upload_file():
    return render_template('upload.html')


@app.route('/uploader', methods=['GET', 'POST'])    # Получаем файл от пользователя
def upload_files():
    language_dict={
        "English":"en",
        "Deutsch":"de",
        "中国":"zh",
        "Esperanto":"eo",
        "Français":"fr"
    }
    if request.method == 'POST':            # Определяем метод обращения к странице как 'Post'
        language = request.form['Language:'] # Получаем с формы выбранный язык перевода


        f = request.files['file']           # Получаем файл выбранный пользователем
        fname = f.filename                  # сохраняем имя файла
        *_,ext = fname.split(".")           # узнаем расширение
        li = os.listdir()                   # получаем список файлов в каталоге
        i=0
        while i < len(li):
            if li[i].find("."+ext)==(-1):
                del li[i]
            else:
                i += 1                       # получаем список файлов в каталоге только с искомым расширением
        n=0
        li2=[]
        if len(li) > 0:
            for i in range(len(li)):
                x,*_= li[i].split("."+ext)
                if x.isdigit():              # проверяем не обработан ли файл ранее, (допускаем только с цифровым именем)
                    li2.append(int(x))
            n = max(li2)                     # узнаем максимальный номер файла из ранее сохраненных
        fname2 = str(n+1)+"."+ext            # новое имя файла в пространстве сервера
        f.save(fname2)                       # сохраняем загруженный файл под номером, на 1 больше максимального имевшегося

        core.main(fname2, language_dict[language])              # str(language_dict(language))


        # f.save(secure_filename(f.filename))
        return render_template('download.html', fname2=str(n+1)+"_processed("+language_dict[language].upper()+")"+"."+ext) #'file uploaded successfully'


@app.route('/return-files/<fname2>')                 # Отдаем файл пользователю
def return_files_tut(fname2):
    try:
        return send_file(fname2, attachment_filename="file_X")
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    app.run(debug=True)
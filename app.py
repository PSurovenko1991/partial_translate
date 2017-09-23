from flask import Flask, render_template, request, send_file, flash, url_for, redirect, session
from werkzeug.utils import secure_filename
import copy
import os
import core
import MySQLdb
from dbconnect import connect
from WForm import RegistrationForm
from passlib.hash import sha256_crypt
from MySQLdb import escape_string as thwart
import gc





UPLOAD_FOLDER = 'files/'#
app = Flask(__name__)
app.secret_key = "my_secret_key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER         # папка загрузки файлов
max_file_size = 2
app.config['MAX_CONTENT_LENGTH'] = max_file_size * 1024 * 1024 # максимальный размер файла 2мб


#Вход в систему:
@app.route('/login/', methods=['GET','POST'])
def login_page():
    error=""
    try:
        if request.method =="POST":
            a_username = request.form['username']
            a_password = request.form['password']

            if a_username == "admin" and a_password == "admin":
                return redirect(url_for('upload_file'))
            else:
                error = "Неверный логин или пароль. Попробуйте ещё раз"
        return render_template('login.html', error=error)
    except Exception as e:
        error = e
        return render_template('login.html', error=error)

# Регистрация:


@app.route('/registration/', methods=['GET','POST'])
def reg_page():
    form = RegistrationForm(request.form)
    if request.method == "POST" and form.validate():
        username = form.username.data
        email = form.email.data
        password = sha256_crypt.encrypt(str(form.password.data))
        c, conn = connect()
        #zap = "SELECT * FROM users WHERE username = '{0}'".format(str((username)))
        #print(zap)
        x = c.execute("SELECT * FROM users WHERE username = '{0}'".format(str(username)))
        if int(x)>0:
            message = "логин занят, придумайте другой."
            print(message)
            return render_template('registration.html', form=form)
        else:
            c.execute("INSERT INTO users (username, password, email) VALUES (%s, %s, %s)",
                    (thwart(username),thwart(password),thwart(email)))
            conn.commit()
            c.close()
            conn.close()
            gc.collect()
            session["logged_in"] = True
            return redirect(url_for("upload_file"))
    return render_template('registration.html', form = form)



@app.route('/upload/')   #@app.route('/') #           # Отображаем начальную страницу загрузки
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

        # if len(f.read())> 2 * 1024 * 1024-1: # Вызывает ошибку если файл не превышает размер
        #     return "Превышен размер файла"


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






# Блок ошибок:

@app.errorhandler(413)
def err_413(error):
    message = "Превышен размер файла "+str(max_file_size)+"Мб."
    return render_template('error.html', message=message), 413

@app.errorhandler(404)
def page_not_found(error):
    message = "Страница не найдена!"
    return render_template('error.html', message=message), 404



if __name__ == '__main__':
    app.run(debug=True)

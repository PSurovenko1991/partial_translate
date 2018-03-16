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
from functools import wraps
import datetime
from transl import trans1
from flask_mail import Mail, Message
import random

# email config
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'PartiaLTranslate@gmail.com'
MAIL_PASSWORD = '67637111Aa'


UPLOAD_FOLDER = 'files/'#
app = Flask(__name__)

app.secret_key = "my_secret_key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER         # папка загрузки файлов
max_file_size = 2
app.config['MAX_CONTENT_LENGTH'] = max_file_size * 1024 * 1024 # максимальный размер файла 2мб

app.config.from_object(__name__)
mail = Mail(app)






# Заппрет отображения страниц для анонимного пользователя
def login_requaired(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            print("!!!")
            return f(*args, **kwargs)
        else:
            print('Войдите в систему')
            return redirect(url_for('login_page'))
    return wrap



#Вход в систему:
@app.route('/login/', methods=['GET','POST'])
def login_page():
    error=""
    try:

        c, conn = connect()
        if request.method =="POST":


            data = c.execute("SELECT * FROM users WHERE username = '{0}'".format(request.form['username']))
            data = c.fetchone()[2]
            c.close()
            conn.close()
            if sha256_crypt.verify((request.form['password']),data):
                session['logged_in'] = True
                session['username'] = request.form['username']

                return redirect(url_for('upload_files'))
            else:
                error = "Неверный логин или пароль. Попробуйте ещё раз"
        return render_template('login.html', error=error)
    except Exception as e:
        error = e
        return render_template('login.html', error=error)

#Выход из системы:
@app.route('/logout/')
def logout():
    error=""
    session.clear()
    return redirect(url_for('login_page'))

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
            session['username'] = username
            return redirect(url_for("upload_files"))
    return render_template('registration.html', form = form)

# восстановление пароля:
#шаг 1: поставить валидацию формы
@app.route('/repair_pass/', methods=['GET','POST'])
def repair_pass():
    c, conn = connect()
    if request.method =="POST":
        email = c.execute("SELECT email, username FROM users WHERE email = '{0}'".format(request.form['mail']))
        global Gusername, Gtestcode
        email, Gusername = c.fetchone()

        if email is None:
            print('этот адрес не использовался при регистрации ')

        else:
            c.close()
            conn.close()

            Gtestcode = str(random.randint(1000, 9999))
            msg = Message('Repair Password from Partial Translate',
                           sender=MAIL_USERNAME,
                           recipients=[email])
            msg.body = Gusername+", для восстановления пароля в следующем окне введите: " + Gtestcode
            mail.send(msg)

            return render_template('repair_pass2.html')# передаём далее username, testcode;
    return render_template('repair_pass.html')
#шаг 2:
@app.route('/repair_pass2/', methods=['GET','POST'])
def repair_pass_step2():
    if request.method == "POST":
        if Gusername == request.form['username'] and Gtestcode == request.form['testcode']:
            return render_template('repair_pass3.html')
        else:
            print("Одно из указанных значений неверно, попробуйте ещё раз")
    return render_template('repair_pass2.html')
#шаг 3:
@app.route('/repair_pass3/', methods=['GET','POST'])
def repair_pass_step3():
    if request.method == "POST":
        if  request.form['new_password'] ==  request.form['confirm']:
            password = str(sha256_crypt.encrypt(request.form['new_password']))
            # print(password)
            c, conn = connect()
            ex = "update users set password = "+str("'"+(password)+"'")+ " where username = '"+Gusername+"';"
            # print(ex)
            c.execute(ex)
            c.execute('commit;')
            c.close()
            conn.close()
            return  render_template('login.html')
        else:
            print("пароли не совпадают")
    return render_template('repair_pass3.html')



# Отображаем начальную страницу загрузки
@app.route('/')   #@app.route('/') #
def base():
    return render_template('Base.html')

# Получаем файл от пользователя, обрабатываем, сохраняем список обработанных слов для пользователя
@login_requaired
@app.route('/upload/', methods=['GET', 'POST'])
def upload_files():

    language_dict={
        "English":"en",
        "Deutsch":"de",
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



# вносим слова в базу для текущего пользователя:
#!!!!!!!!!!!!!!!

        c, conn = connect()
        ex = 'SELECT * FROM users WHERE username = ' + '"' + session['username'] + '"'
        user_id = c.execute(ex)
        user_id = str(c.fetchone()[0])

        #Замена ранее изученных слов:
        ex = 'select RU, '+language_dict[language].upper()+'  FROM (words_users JOIN words ON words_users.id_word=words.id) where id_user = "' + user_id + '" order by date;'
        user_dict_now = c.execute(ex)
        user_dict_now = c.fetchall() # передаём в core для автозамены


        x_list = core.main(fname2, language_dict[language],user_dict_now)# str(language_dict(language))# !!!!!!!:L:L:L:L:!!!

        # f.save(secure_filename(f.filename))
        now,t =  str(datetime.datetime.now()).split(' ') #текущая дата - now
        now = now.split('-')[0]+now.split('-')[1]+now.split('-')[2]
        t = t.split('.')[0] # текущее время
        x_list2 = []
        for i in x_list:
            x_list2.append(str(trans1(i,language_dict[language])))


        for i in range(len(x_list)):
            # проверяем добавлялось ли слово ранее в словарь
            ex = 'SELECT * FROM words WHERE RU = "'+str(x_list[i])+'";'
            c.execute(ex)
            id_word = c.fetchone()
            if id_word is None:
                ex = 'INSERT INTO words (RU,'+language_dict[language].upper()+') VALUES ("'+x_list[i]+'", "'+x_list2[i]+'");'
                c.execute(ex)
                c.execute('SELECT * FROM words WHERE id=(SELECT max(id) FROM words)')
                id_word = str(c.fetchone()[0])
            else: id_word=str(id_word[0])
            # проверяем есть ли связь слово-пользователь, если нет - добавляем
            ex = 'SELECT * FROM words_users WHERE id_user = '+user_id+' and id_word = '+id_word+';'
            c.execute(ex)
            if c.fetchone() is None:
                ex = u'INSERT INTO words_users (id_user, id_word, date) VALUES ('+user_id+", "+str(id_word)+", "+now+")"
                c.execute(ex)
        c.execute('commit;')
        c.close()
        conn.close()
#!!!!!!!!!!!!!!!!!

        return render_template('download.html', fname2=str(n+1)+"_processed("+language_dict[language].upper()+")"+"."+ext) #'file uploaded successfully'

    if request.method == 'GET':
        return render_template('upload.html')
    return render_template('upload.html')

# Отдаем файл пользователю
@login_requaired
@app.route('/return-files/<fname2>')
def return_files_tut(fname2):
    try:
        return send_file(fname2, attachment_filename="file_X")
    except Exception as e:
        return str(e)

# словарь:
@app.route('/dict/', methods=['GET','POST'])
def dict():
    c, conn = connect()
    ex = 'SELECT * FROM users WHERE username = ' + '"' + session['username'] + '"'
    user_id = c.execute(ex)
    user_id = str(c.fetchone()[0])
    ex = 'select RU, EN, date FROM (words_users JOIN words ON words_users.id_word=words.id) where id_user = "'+user_id+'" order by date;'
    user_dict = c.execute(ex)
    user_dict = c.fetchall()
    #пользователь вносит свои слова в словарь:
    if request.method == "POST":
        Ru_word = request.form['Ru']
        L_word = request.form['Language']
        ex = 'INSERT INTO words( RU, EN)  VALUES("'+Ru_word+'" , "'+L_word+'");'
        c.execute(ex) # Внесли слова в базу

        c.execute('SELECT * FROM words WHERE id=(SELECT max(id) FROM words)')
        id_word = str(c.fetchone()[0])
        # получили id внесённого слова
        now, t = str(datetime.datetime.now()).split(' ')  # текущая дата - now
        now = now.split('-')[0] + now.split('-')[1] + now.split('-')[2]
        #создаём связь слово - пользователь
        ex = 'INSERT INTO words_users(id_user, id_word, date)  VALUES('+user_id+', '+id_word+', '+now+ ');'
        c.execute(ex)
        c.execute('commit;')
        return redirect(url_for("dict"))
    return render_template('dict.html', user_dict = user_dict )


# каталог:








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

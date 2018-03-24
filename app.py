from flask import Flask, render_template, request, send_file, flash, url_for, redirect, session, Response
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



#Вход в систему: +rest
@app.route('/login/', methods=['GET','POST'])
def login_page():
    error=""
    try:
        c, conn = connect()
        requestType = 0
        if request.content_type == 'application/json':
            Content = request.get_json()
            username = Content['login']
            password = Content["pass"]
            requestType = 1
        if request.method == "POST" and requestType == 0:
            username = request.form['username']
            password = request.form['password']
            requestType = 2
        if requestType != 0:
            data = c.execute("SELECT * FROM users WHERE username = '{0}'".format(username))
            data = c.fetchone()[2]
            if data is not None:
                c.close()
                conn.close()
                if sha256_crypt.verify(password,data):
                    session['logged_in'] = True
                    session['username'] = username
                    if requestType == 1:
                        return Response(status=200)
                    else:
                        return redirect(url_for('upload_files'))
                else:
                    if requestType == 1:
                        return Response(status=403)
                    else:
                        error = "Неверный логин или пароль. Попробуйте ещё раз"
        return render_template('login.html', error=error)
    except Exception as e:
        error = e
        if requestType == 1:
            return Response(status=403)
        else:
            return render_template('login.html', error=error)

#Выход из системы:
@app.route('/logout/')
def logout():
    error=""
    session.clear()
    return redirect(url_for('login_page'))

# Регистрация:+ rest
@app.route('/registration/', methods=['GET','POST'])
def reg_page():
    form = RegistrationForm(request.form)

    requestType = 0
    if request.content_type == 'application/json':
        Content = request.get_json()
        username = Content['login']
        email = Content["email"]
        password = sha256_crypt.encrypt(Content["pass"])
        requestType =1

    if request.method == "POST" and form.validate():
        username = form.username.data
        email = form.email.data
        password = sha256_crypt.encrypt(str(form.password.data))
        requestType = 2

    if requestType != 0:
        c, conn = connect()
        x1 = c.execute("SELECT * FROM users WHERE email = '{0}'".format(str(email)))
        x = c.execute("SELECT * FROM users WHERE username = '{0}'".format(str(username)))
        if int(x) > 0 or int(x1)>0:
            message = "логин занят, придумайте другой, или адресс эл почты ранее использовался для регистрации"
            print(message)
            if (requestType == 1):
                return Response(status=403)
            else:
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
            if (requestType == 1):
                return Response(status=200)
            else:
                return redirect(url_for("logout"))
    return render_template('registration.html', form = form)


# восстановление пароля: +rest шаг 1:
@app.route('/repair_pass/', methods=['GET','POST'])
def repair_pass():
    c, conn = connect()
    requestType = 0
    if request.content_type == 'application/json':
        Content = request.get_json()
        email = Content['email']
        requestType = 1
    if request.method =="POST" and requestType ==0:
        email = request.form['mail']
        requestType = 2
    if requestType != 0:
        c.execute("SELECT email, username FROM users WHERE email = '{0}'".format(email))
        global Gusername, Gtestcode
        if c.fetchone() is None:
            if requestType ==2:
                print('этот адрес не использовался при регистрации ')
            else:
                return Response(status=403)
        else:
            email, Gusername = c.fetchone()
            c.close()
            conn.close()
            Gtestcode = str(random.randint(1000, 9999))
            msg = Message('Repair Password from Partial Translate',
                           sender=MAIL_USERNAME,
                           recipients=[email])
            msg.body = Gusername+", для восстановления пароля в следующем окне введите: " + Gtestcode
            mail.send(msg)
            if requestType == 2:
                return redirect(url_for("repair_pass_step2"))
            else:
                return Response(status=200)
    return render_template('repair_pass.html')
#шаг 2:
@app.route('/repair_pass2/', methods=['GET','POST'])
def repair_pass_step2():
    requestType = 0
    if request.content_type == 'application/json':
        Content = request.get_json()
        username = Content['username']
        testcode = Content['testcode']
        requestType = 1
    if request.method == "POST" and requestType == 0:
        username = request.form['username']
        testcode = request.form['testcode']
        requestType =2
    if requestType!= 0:
        if Gusername == username and Gtestcode == testcode:
            if requestType == 2:
                return render_template('repair_pass3.html')
            else: return Response(status=200)
        else:
            if requestType == 2:
                print("Одно из указанных значений неверно, попробуйте ещё раз")
            else: return Response(status=403)
    return render_template('repair_pass2.html')
#шаг 3:
@app.route('/repair_pass3/', methods=['GET','POST'])
def repair_pass_step3():
    requestType = 0
    if request.content_type == 'application/json':
        Content = request.get_json()
        new_password = Content['new_password']
        confirm = Content['confirm']
        requestType = 1

    if request.method == "POST" and requestType == 0:
        new_password = request.form['new_password']
        confirm = request.form['confirm']
        requestType =2
    if requestType!=0:
        if  new_password ==  confirm:
            # print(new_password)
            # print(confirm)
            # print(requestType)
            password = str(sha256_crypt.encrypt(new_password))
            c, conn = connect()
            ex = "update users set password = "+str("'"+(password)+"'")+ " where username = '"+Gusername+"';"
            c.execute(ex)
            c.execute('commit;')
            c.close()
            conn.close()
            if requestType == 2:
                return redirect(url_for("login_page"))
            else:
                return Response(status=200)
        else:
            if requestType == 2:
                print("пароли не совпадают")
            else:
                return Response(status=403)
    return render_template('repair_pass3.html')



# Отображаем начальную страницу загрузки
@app.route('/')   #@app.route('/') #
def base():
    return render_template('Base.html')

# Получаем файл от пользователя, обрабатываем, сохраняем список обработанных слов для пользователя
# В Rest не нуждается, только для пользователя сайта.
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


        x_list = core.main(fname2, fname.split('.')[0], language_dict[language],user_dict_now)# str(language_dict(language))# !!!!!!!:L:L:L:L:!!!

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
                                                                                                                    #fname.split('.')[0]+
        return render_template('download.html', fname2=str(n + 1)+"_processed("+language_dict[language].upper()+")"+fname.split('.')[0]+"."+ext) #'file uploaded successfully'

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

    requestType = 0

    c, conn = connect()
    ex = 'SELECT * FROM users WHERE username = ' + '"' + session['username'] + '"'
    user_id = c.execute(ex)
    user_id = str(c.fetchone()[0])
    ex = 'select RU, EN, date FROM (words_users JOIN words ON words_users.id_word=words.id) where id_user = "'+user_id+'" order by date;'
    user_dict = c.execute(ex)
    user_dict = c.fetchall()
    #пользователь вносит свои слова в словарь:


    if request.content_type == 'application/json':
        Content = request.get_json()
        Ru_word = Content['Ru_word']
        L_word = Content['L_word']
        requestType = 1

    if request.method == "POST" and requestType ==0:
        Ru_word = request.form['Ru']
        L_word = request.form['Language']
        requestType =2

    if requestType!=0:
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
        if requestType ==2:
            requestType = 0
            return redirect(url_for("dict"))

        else:
            requestType = 0
            return Response(status=200)


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

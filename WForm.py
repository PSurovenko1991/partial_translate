from wtforms import *




class RegistrationForm(Form):
    username = TextField('Username',[validators.length(min = 4, max=20)])
    email = StringField('Email adress',[validators.length(min = 6, max=50)])
    password = PasswordField('Password',[validators.required(),
                                         validators.equal_to('confirm', message='password must match.')])
    confirm = PasswordField('repeat password')
    Yalogin = StringField('Yandex login')
    Yapassword = StringField('Yandex password')
    accept = BooleanField('<a href="/"> I accept</a>', [validators.required()])

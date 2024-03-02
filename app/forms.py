from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, EqualTo, ValidationError

from app import db
from app.models import User

abc = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя- '
from string import ascii_letters, digits

class LoginForm(FlaskForm):
    username = StringField('Никнейм', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class SignupForm(FlaskForm):
    username = StringField('Никнейм', validators=[DataRequired(message="Поле не может быть пустым")])
    name = StringField('ФИО', validators=[DataRequired(message="Поле не может быть пустым")])
    school = StringField('Учебное заведение', validators=[DataRequired(message="Поле не может быть пустым")])
    password = PasswordField('Пароль', validators=[DataRequired(message="Поле не может быть пустым")])
    confirm_password = PasswordField('Подтверждение пароля', validators=[EqualTo('password', message='Пароли не совпадают')])
    submit = SubmitField('Зарегистрироваться')

    def validate_username(self, username):
        if User.query.filter_by(login=username.data).first():
            raise ValidationError("Этот никнейм уже занят")
        else:
            for char in username.data:
                if char not in f'{ascii_letters}{digits}_':
                    raise ValidationError("Никнейм может содержать только латинские буквы, цифры и _")

    def validate_name(self, name):
        name_ = name.data.split()
        full_abc = f'{abc}{abc.upper()}'
        if len(name_) != 3: raise ValidationError("ФИО должно быть заполнено как три слова, разделенных пробелами. Для пропуска отчества поставьте 0")
        for char in f'{name_[0]}{name_[1]}':
            if char not in full_abc: raise ValidationError("ФИО может содержать только буквы кириллицы и дефис" + char)
        if name_[2] != '0':
            for char in f'{name_[2]}':
                if char not in full_abc: raise ValidationError("ФИО может содержать только буквы кириллицы и дефис" + char)

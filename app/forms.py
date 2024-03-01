from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, EqualTo, ValidationError

from app import db
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')


class SignupForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    fname = StringField('Имя', validators=[DataRequired()])
    mname = StringField('Отчество', validators=[DataRequired()])
    lname = StringField('Фамилия', validators=[DataRequired()])
    school = StringField('Школа', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Подтвердите пароль', validators=[EqualTo('password', message='Passwords do not match')])
    submit = SubmitField('Sign up')

    def validate_username(self, username):
        if User.query.filter_by(login=username.data).first():
            raise ValidationError("This username is already taken")

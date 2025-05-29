from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FileField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Старый пароль', validators=[DataRequired()])
    new_password = PasswordField('Новый пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Повторите новый пароль', validators=[
        DataRequired(), EqualTo('new_password', message='Пароли должны совпадать')
    ])
    submit = SubmitField('Обновить пароль')


class ImageGenerationForm(FlaskForm):
    prompt = TextAreaField('Описание', validators=[DataRequired()])
    audio = FileField('Загрузите аудиофайл (MP3)', validators=[DataRequired()])
    submit = SubmitField('Генерировать изображение')

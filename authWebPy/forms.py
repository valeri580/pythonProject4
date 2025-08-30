from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import (
    DataRequired, Email, EqualTo, Length, ValidationError
)
from models import User

class RegisterForm(FlaskForm):
    name = StringField("Имя", validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField("Почта", validators=[DataRequired(), Email(), Length(max=255)])
    password = PasswordField("Пароль", validators=[DataRequired(), Length(min=6, max=128)])
    password2 = PasswordField("Повторите пароль", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Зарегистрироваться")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError("Эта почта уже зарегистрирована.")

class LoginForm(FlaskForm):
    email = StringField("Почта", validators=[DataRequired(), Email(), Length(max=255)])
    password = PasswordField("Пароль", validators=[DataRequired()])
    submit = SubmitField("Войти")

class ProfileForm(FlaskForm):
    name = StringField("Имя", validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField("Почта", validators=[DataRequired(), Email(), Length(max=255)])
    current_password_for_info = PasswordField(
        "Текущий пароль (для подтверждения изменений имени/почты)",
        validators=[DataRequired(), Length(min=6, max=128)]
    )
    submit_info = SubmitField("Сохранить изменения профиля")

    def __init__(self, original_email: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_email = original_email

    def validate_email(self, field):
        if field.data.lower() != self.original_email.lower():
            if User.query.filter_by(email=field.data.lower()).first():
                raise ValidationError("Эта почта уже используется другим аккаунтом.")

class PasswordChangeForm(FlaskForm):
    current_password = PasswordField("Текущий пароль", validators=[DataRequired(), Length(min=6, max=128)])
    new_password = PasswordField("Новый пароль", validators=[DataRequired(), Length(min=6, max=128)])
    new_password2 = PasswordField("Повторите новый пароль", validators=[DataRequired(), EqualTo("new_password")])
    submit_pass = SubmitField("Обновить пароль")

class EmptyForm(FlaskForm):
    submit = SubmitField('Отправить')
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class RegistrationForm(FlaskForm):
    username = StringField("Логін", validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField(
        "Пароль",
        validators=[DataRequired(), Length(min=6, message="Мінімум 6 символів")],
    )
    password2 = PasswordField(
        "Підтвердження паролю",
        validators=[DataRequired(), EqualTo("password", message="Паролі мають співпадати")],
    )
    submit = SubmitField("Зареєструватися")


class LoginForm(FlaskForm):
    username = StringField("Логін", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    submit = SubmitField("Увійти")

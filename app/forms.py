from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, BooleanField, SelectField, PasswordField
from wtforms.validators import DataRequired, Length, Email, Regexp

class ContactForm(FlaskForm):
    name = StringField("Ім'я", validators=[DataRequired(), Length(min=4, max=10)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    phone = StringField("Телефон", validators=[DataRequired(), Regexp(r'^\+380\d{9}$', message="Телефон має бути у форматі +380XXXXXXXXX")])
    subject = SelectField("Тема", choices=[
        ("question", "Запитання"),
        ("support", "Підтримка"),
        ("offer", "Пропозиція"),
        ("other", "Інше"),
    ], validators=[DataRequired()])
    message = TextAreaField("Повідомлення", validators=[DataRequired(), Length(max=500)])
    submit = SubmitField("Надіслати")

class LoginForm(FlaskForm):
    username = StringField("Логін або email", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired(), Length(min=4, max=10)])
    remember = BooleanField("Запам'ятати мене")
    submit = SubmitField("Увійти")
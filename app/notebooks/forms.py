from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DecimalField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

class NotebookForm(FlaskForm):
    name = StringField("Назва ноутбука", validators=[DataRequired(), Length(max=150)])
    description = TextAreaField("Опис", validators=[Length(max=2000)])
    price = DecimalField(
        "Ціна, $",
        places=2,
        validators=[DataRequired(), NumberRange(min=0)],
    )
    brand_id = SelectField("Бренд", coerce=int, validators=[DataRequired()])
    submit = SubmitField("Зберегти")

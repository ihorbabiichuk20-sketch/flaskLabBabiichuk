from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length
from wtforms.fields import DateTimeLocalField

class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(max=150)])
    content = TextAreaField("Content", validators=[DataRequired()])
    is_active = BooleanField("Is active", default=True)
    publish_date = DateTimeLocalField(
        "Publish date",
        format="%Y-%m-%dT%H:%M",
        default=datetime.utcnow,
    )
    category = SelectField(
        "Category",
        choices=[("news", "News"), ("publication", "Publication"), ("tech", "Tech"), ("other", "Other")],
        default="other",
    )
    submit = SubmitField("Save")

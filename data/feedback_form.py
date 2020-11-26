from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, TextAreaField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class FeedbackForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    email = EmailField('Почта', validators=[DataRequired()])
    description = TextAreaField('Описание', validators=[DataRequired()])
    submit = SubmitField('Отправить')
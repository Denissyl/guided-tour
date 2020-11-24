from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class FeedbackForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    email = EmailField('Почта', validators=[DataRequired()])
    description = StringField('Описание', validators=[DataRequired()])
    submit = SubmitField('Отправить')
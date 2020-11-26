from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired


class FeedbackForm(FlaskForm):
    note = StringField('Заметка', validators=[DataRequired()])
    submit = SubmitField('Сохранить')
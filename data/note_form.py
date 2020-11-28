from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired


class NoteForm(FlaskForm):
    note = TextAreaField('Заметка', validators=[DataRequired()])
    submit = SubmitField('Сохранить')

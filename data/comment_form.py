from flask_wtf import FlaskForm
from wtforms import SubmitField, RadioField, TextAreaField
from wtforms.validators import DataRequired


class CommentForm(FlaskForm):
    description = TextAreaField('Описание')
    mark = RadioField('Оценка', choices=[('one_point', '1'), ('two_points', '2'),
                                         ('three_points', '3'), ('four_points', '4'),
                                         ('five_points', '5')], validators=[DataRequired()])
    submit = SubmitField('Отправить')


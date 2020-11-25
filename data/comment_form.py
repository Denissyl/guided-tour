from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, RadioField
from wtforms.validators import DataRequired


class CommentForm(FlaskForm):
    description = StringField('Описание')
    mark = RadioField('Оценка', choices=[('one_point', '1'), ('two_points', '2'),
                                         ('three_points', '3'), ('four_points', '4'),
                                         ('five_points', '5')], validators=[DataRequired()])
    submit = SubmitField('Отправить')


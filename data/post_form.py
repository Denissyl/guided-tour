from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, TextAreaField
from wtforms.validators import DataRequired, length


class PostForm(FlaskForm):
    images = TextAreaField('Ссылки на изображения, разделенные знаком "#"', validators=[DataRequired(), length(max=600)])
    sight = StringField('Название', validators=[DataRequired()])
    description = TextAreaField('Описание', validators=[DataRequired(), length(max=1200)])
    submit = SubmitField('Добавить')

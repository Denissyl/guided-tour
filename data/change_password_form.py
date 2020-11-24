from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.validators import DataRequired


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Текущий пароль', validators=[DataRequired()])
    new_password = PasswordField('Новый пароль', validators=[DataRequired()])
    new_password_again = PasswordField('Повторите новый пароль', validators=[DataRequired()])
    submit = SubmitField('Подтвердить')

import datetime
import os

from flask import render_template, app, Flask, redirect
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_mail import Mail, Message

from data import db_session
from data.change_password_form import ChangePasswordForm
from data.comment_form import CommentForm
from data.comments import Comment
from data.db_session import global_init, create_session
from data.feedback_form import FeedbackForm
from data.feedbacks import Feedback
from data.login_form import LoginForm
from data.register import RegisterForm
from data.users import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ptpit_secret_key'
login_manager = LoginManager()
login_manager.login_view = '/register'
login_manager.init_app(app)

global_init('db/guided-tour.sqlite')
session = create_session()

mail = Mail(app)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'permtourcompany@gmail.com'
app.config['MAIL_DEFAULT_SENDER'] = 'permtourcompany@gmail.com'
app.config['MAIL_PASSWORD'] = 'p1a2s3s4'


def main():
    @app.route('/', methods=['GET', 'POST'])
    def index():
        form = FeedbackForm()
        if form.validate_on_submit():
            # msg = Message("Feedback", recipients=['denis-syl@yandex.ru'])
            # msg.body = "You have received a new feedback from."
            # mail.send(msg)
            #
            # print("Data received.")

            feedback = Feedback(
                description=form.description.data,
                name=form.name.data,
                email=form.email.data,
            )

            session.add(feedback)
            session.commit()

            return render_template('index.html', title="Гид-экскурсия", form=form,
                                   message="Ваш отзыв был отправлен")
        return render_template('index.html', title="Гид-экскурсия", form=form)

    db_session.global_init("db/guided-tour.sqlite")

    @app.route('/<sight>', methods=['GET', 'POST'])
    def sights(sight):
        form = CommentForm()
        if form.validate_on_submit():
            if current_user.is_authenticated:
                comment_to_db = Comment(
                    description=form.description.data,
                    sight=sight,
                    nickname=current_user.nickname,
                    email=current_user.email,
                    mark=form.mark.data,
                    datetime=str(datetime.datetime.now(datetime.timezone.utc) +
                                 datetime.timedelta(hours=5, minutes=0))[:19]
                )

                session.add(comment_to_db)
                session.commit()
                return render_template(sight + ".html", message="Ваш комментарий был отправлен",
                                       sight=sight, title=sight,
                                       Comment=Comment, session=session, form=form)
            else:
                return redirect('/login')


        return render_template(sight + ".html",
                               sight=sight, title=sight,
                               Comment=Comment, session=session, form=form)

    @app.route('/delete_comment/<sight>/<number>', methods=['GET', 'POST'])
    def delete_comment(sight, number):
        if current_user.is_authenticated:
            session = db_session.create_session()
            comment = session.query(Comment).get(number)

            session.delete(comment)
            session.commit()
            return redirect('/' + sight)
        else:
            return redirect('/login')




    @app.route('/cabinet', methods=['GET', 'POST'])
    @login_required
    def cabinet():
        form = ChangePasswordForm()
        if form.validate_on_submit():
            session = db_session.create_session()
            user = session.query(User).filter(User.nickname == current_user.nickname).first()
            if not user.check_password(form.current_password.data) and (form.new_password.data != form.new_password_again.data):
                return render_template('cabinet.html',
                                       form=form,
                                       message="Текущий пароль не верный и новые пароли не совпадают")
            if form.new_password.data != form.new_password_again.data:
                return render_template('cabinet.html',
                                       form=form,
                                       message="Новые пароли не совпадают")
            if not user.check_password(form.current_password.data):
                return render_template('cabinet.html',
                                       form=form,
                                       message="Текущий пароль не верный")

            user.set_password(form.new_password.data)
            session.add(user)
            session.commit()

        return render_template('cabinet.html', title="Личный кабинет", form=form)

    @login_manager.user_loader
    def load_user(user_id):
        session = db_session.create_session()
        return session.query(User).get(user_id)

    @app.route('/register', methods=['GET', 'POST'])
    def reqister():
        form = RegisterForm()
        if form.validate_on_submit():
            if form.password.data != form.password_again.data:
                return render_template('register.html',
                                       form=form,
                                       message="Пароли не совпадают")
            session = db_session.create_session()
            if session.query(User).filter(User.email == form.email.data).first():
                return render_template('register.html',
                                       form=form,
                                       message="Такой пользователь уже есть")
            user = User(
                nickname=form.nickname.data,
                email=form.email.data,
            )
            user.set_password(form.password.data)
            session.add(user)
            session.commit()
            return redirect('/login')
        return render_template('register.html', form=form)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            session = db_session.create_session()
            user = session.query(User).filter(User.email == form.email.data).first()
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                return redirect("/")
            return render_template('login.html',
                                   message="Неправильный логин или пароль",
                                   form=form)
        return render_template('login.html', form=form)

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect("/")


if __name__ == '__main__':
    main()
    port = int(os.environ.get('PORT', 7000))
    # app.run(debug=True)
    app.run('0.0.0.0', port)


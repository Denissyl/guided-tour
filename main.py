import datetime
import os

from flask import render_template, app, Flask, redirect, request
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
from data.note_form import NoteForm
from data.notes import Note
from data.post_form import PostForm
from data.posts import Post
from data.register import RegisterForm
from data.users import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ptpit_secret_key'
login_manager = LoginManager()
login_manager.login_view = 'login'
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
            if current_user.is_authenticated:
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
                                       message="Ваш отзыв был отправлен", Post=Post, session=session)
            return redirect("login")

        return render_template('index.html', Post=Post, session=session, title="Гид-экскурсия", form=form)

    db_session.global_init("db/guided-tour.sqlite")

    @app.route('/<sight>', methods=['GET', 'POST'])
    def sights(sight):

        sights = {"Ancient_volcano": "Древний вулкан",
                  "Basegi_Nature_Reserve": "Заповедник Басеги",
                  "Blue_lakes": "Голубые озёра", "Cathedral_square": "Соборная площадь",
                  "Perm_36": "Пермь-36", "Usva_pillars": "Устьвинские столбы",
                  "Vakutin_stone": "Вакутин камень",
                  "Vishera_nature_reserve": "Вишерский заповедник"}
        sights2 = ["Ancient_volcano", "Basegi_Nature_Reserve", "Blue_lakes", "Cathedral_square",
                  "Perm_36", "Usva_pillars", "Vakutin_stone", "Vishera_nature_reserve"]
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

                if sight in sights2:
                    return render_template(sight + ".html", message="Ваш комментарий был отправлен",
                                           sight=sight, title=sight,
                                           Comment=Comment, session=session, form=form)
                else:
                    return render_template("add_post_page.html", message="Ваш комментарий был отправлен",
                                           sight=sight, title=sight,
                                           Comment=Comment, session=session, form=form, Post=Post)
            else:
                return redirect('/login')

        if sight in sights2:
            return render_template(sight + ".html",
                                   sight=sight, title=sights[sight],
                                   Comment=Comment, session=session, form=form)
        else:
            return render_template("add_post_page.html", title=sight, Post=Post, form=form,
                                   sight=sight, session=session, Comment=Comment)


    @app.route('/add_post', methods=['GET', 'POST'])
    @login_required
    def add_post():
        form = PostForm()
        if form.validate_on_submit():
            session = db_session.create_session()
            if current_user.is_authenticated:
                post_to_db = Post(
                    images=form.images.data,
                    sight=form.sight.data,
                    description=form.description.data,
                    nickname=current_user.nickname,
                    email=current_user.email,
                    datetime=str(datetime.datetime.now(datetime.timezone.utc) +
                                 datetime.timedelta(hours=5, minutes=0))[:19]
                )

                session.add(post_to_db)
                session.commit()

                return redirect('/')
            else:
                return redirect('/login')
        return render_template('add_post.html', title="Добавление достопримечательности", form=form)

    @app.route('/add_note/<sight>', methods=['GET', 'POST'])
    @login_required
    def add_note(sight):
        form = NoteForm()
        if form.validate_on_submit():
            session = db_session.create_session()
            if current_user.is_authenticated:
                note_to_db = Note(
                    note=form.note.data,
                    sight=sight,
                    nickname=current_user.nickname,
                    email=current_user.email,
                    datetime=str(datetime.datetime.now(datetime.timezone.utc) +
                                 datetime.timedelta(hours=5, minutes=0))[:19]
                )

                session.add(note_to_db)
                session.commit()

                return redirect('/cabinet')
            else:
                return redirect('/login')
        return render_template('add_note.html', title="Добавить заметку", form=form)

    @app.route('/delete_note/<number>', methods=['GET', 'POST'])
    def delete_note(number):
        if current_user.is_authenticated:
            session = db_session.create_session()
            note = session.query(Note).get(number)

            session.delete(note)
            session.commit()

            return redirect('/cabinet')
        else:
            return redirect('/login')

    @app.route('/delete_comment/<sight>/<number>', methods=['GET', 'POST'])
    def delete_comment(sight, number):
        if current_user.is_authenticated:
            session = db_session.create_session()
            comment = session.query(Comment).get(number)

            session.delete(comment)
            session.commit()

            return redirect("/" + sight)
        else:
            return redirect('/login')

    @app.route('/delete_post/<sight>/<number>', methods=['GET', 'POST'])
    def delete_post(sight, number):
        if current_user.is_authenticated:
            session = db_session.create_session()
            post = session.query(Post).get(number)
            comment = session.query(Comment)

            for i in range(session.query(Comment).count()):
                if comment[i].sight == sight:
                    session.delete(comment[i])

            session.delete(post)
            session.commit()

            return redirect("/")
        else:
            return redirect('/login')

    @app.route('/cabinet', methods=['GET', 'POST'])
    @login_required
    def cabinet():
        return render_template('cabinet.html', title="Личный кабинет", Note=Note, session=session, User=User)

    @app.route('/change_password', methods=['GET', 'POST'])
    @login_required
    def change_password():
        form = ChangePasswordForm()
        if form.validate_on_submit():
            session = db_session.create_session()
            user = session.query(User).filter(User.nickname == current_user.nickname).first()
            if not user.check_password(form.current_password.data) and (
                    form.new_password.data != form.new_password_again.data):
                return render_template('change_password.html',
                                       form=form,
                                       message="Текущий пароль не верный и новые пароли не совпадают")
            if form.new_password.data != form.new_password_again.data:
                return render_template('change_password.html',
                                       form=form,
                                       message="Новые пароли не совпадают")
            if not user.check_password(form.current_password.data):
                return render_template('change_password.html',
                                       form=form,
                                       message="Текущий пароль не верный")

            user.set_password(form.new_password.data)
            session.add(user)
            session.commit()
            return render_template('change_password.html', title="Личный кабинет",
                                   message="Ваш пароль был изменен", form=form)
        return render_template('change_password.html', title="Смена пароля", form=form)

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
                datetime=str(datetime.datetime.now(datetime.timezone.utc) +
                             datetime.timedelta(hours=5, minutes=0))[:19],
                role="user"
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
    app.run('0.0.0.0', port)


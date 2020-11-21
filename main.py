import os

from flask import render_template, app, Flask, redirect
from flask_login import LoginManager, login_user, login_required, logout_user

from data import db_session
from data.db_session import global_init, create_session
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

def main():
    @app.route('/')
    def index():
        return render_template('index.html', title="Гид-экскурсия")

    db_session.global_init("db/guided-tour.sqlite")

    @app.route('/Cathedral_square')
    def Cathedral_square():
        return render_template('Cathedral_square.html', title="Соборная площадь")

    @app.route('/Vishera_nature_reserve')
    def Vishera_nature_reserve():
        return render_template('Vishera_nature_reserve.html', title="Вишерский заповедник")

    @app.route('/Perm_36')
    def Perm_36():
        return render_template('Perm_36.html', title="Пермь-36")

    @app.route('/Usva_pillars')
    def Usva_pillars():
        return render_template('Usva_pillars.html', title="Устьвинские столбы")

    @app.route('/Vakutin_stone')
    def Vakutin_stone():
        return render_template('Vakutin_stone.html', title="Вакутин камень")

    @app.route('/Ancient_volcano')
    def Ancient_volcano():
        return render_template('Ancient_volcano.html', title="Древний вулкан")

    @app.route('/Basegi_Nature_Reserve')
    def Basegi_Nature_Reserve():
        return render_template('Basegi_Nature_Reserve.html', title="Заповедник Басеги")

    @app.route('/Blue_lakes')
    def Blue_lakes():
        return render_template('Blue_lakes.html', title="Голубые озёра")


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
    app.run('0.0.0.0', port)


from flask import Flask, render_template, redirect, url_for, flash, request
from data import db_session
from data.users import User
from data.shop import Shop
from forms.users import LoginForm, RegisterForm
from flask_login import LoginManager, login_user
from flask_login import LoginManager, login_user, login_required, logout_user


import json

from data_collection import Data_collection


Data_collection() #data


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)



#routes
@app.route('/', methods=['GET', 'POST'])
def index():
    with open('result.json', encoding='utf-8') as f:
        templates = json.load(f)
    product = request.form.get("product_id", "")
    current_email = request.form.get("name", "")
    val = request.form.get("value", "")
    if product:
        db_sess = db_session.create_session()
        user = db_sess.query(User).first()
        new_product = Shop(content=product, email=current_email, user=user)
        db_sess.add(new_product)
        db_sess.commit()
    if val:
        return redirect(url_for('basket', current_email=val))
    return render_template('index.html', templates=templates)





@app.route('/basket', methods=['GET', 'POST'])
def basket():
    with open('result.json', encoding='utf-8') as f:
        templates = json.load(f)
    c = ''
    summ = 0
    current_email = request.args.get('current_email')
    db_sess = db_session.create_session()
    basket_list = db_sess.query(Shop).all()
    for basket in basket_list:
        if basket.email == current_email:
            c += basket.content + ' '

    for i in c.split():
        for el in templates:
            if el['productId'] == i:
                summ += int(el['item_basePrice'])

    
    return render_template('basket.html', cont=c.split(), templates=templates, summ=summ)


@app.route('/pay')
def pay():
    
    return render_template('pay.html')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print('login')
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        print('Неправильный логин или пароль')
        return render_template('login.html',
                                message="Неправильный логин или пароль",
                                form=form)
    return render_template('login.html', title='Авторизация', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                    form=form,
                                    message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                    form=form,
                                    message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Вы вышли из аккаунта", "success")
    return redirect(url_for('login'))

if __name__ == "__main__":
    db_session.global_init("bd/blogs.db")
    app.run(debug=True)
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, current_user
from models import db, User, Product
from forms import LoginForm, RegistrationForm, ProductForm
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'index'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/', methods=['GET', 'POST'])
def index():
    login_form = LoginForm()
    register_form = RegistrationForm()

    if request.method == 'POST':
        if 'login' in request.form and login_form.validate_on_submit():
            user = User.query.filter_by(username=login_form.username.data).first()
            if user and user.check_password(login_form.password.data):
                login_user(user)
                flash('შესვლა წარმატებით შესრულდა')
                return redirect(url_for('index'))
            else:
                flash('არასწორი მომხმარებელი ან პაროლი')

        elif 'register' in request.form and register_form.validate_on_submit():
            existing_user = User.query.filter_by(username=register_form.username.data).first()
            if existing_user:
                flash('მომხმარებელი უკვე არსებობს')
            else:
                new_user = User(username=register_form.username.data, email=register_form.email.data)
                new_user.set_password(register_form.password.data)
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user)
                flash('რეგისტრაცია წარმატებით შესრულდა')
                return redirect(url_for('index'))

    return render_template('index.html', login_form=login_form, register_form=register_form)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/products', methods=['GET', 'POST'])
def products():
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(name=form.name.data, description=form.description.data)
        db.session.add(product)
        db.session.commit()
        flash('პროდუქტი დაემატა!')
        return redirect(url_for('products'))

    products = Product.query.all()
    return render_template('products.html', form=form, products=products)

@app.route('/admin')
def admin():
    users = User.query.all()
    return render_template('admin.html', users=users)

@app.route('/logout')
def logout():
    logout_user()
    flash('გამოსვლა შესრულდა')
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

from flask import render_template, redirect, url_for, flash, Blueprint, request
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.security import check_password_hash

from flaskr.models import User

auth = Blueprint('auth', __name__)


@auth.get('/login')
def login_page():
    return render_template('login.html')


@auth.post('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('web.main'))

    if not ('email' in request.form and 'password' in request.form):
        return redirect(url_for('web.auth.login_page'))

    email = request.form.get('email')
    password = request.form.get('password')
    user = User.query.filter_by(login=email).first()
    if not user or not check_password_hash(user.password_hash, password):
        flash('Неправильный логин или пароль')
        return redirect(url_for('web.auth.login_page'))

    login_user(user, remember='rememberme' in request.form)
    return redirect(url_for('web.main'))


@auth.post('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('web.auth.login_page'))

from flask import Blueprint, request
from werkzeug.security import check_password_hash
from flaskr.models import User, Company, Role
from flask_login import login_user, login_required, logout_user, current_user
from flaskr import db

auth = Blueprint('auth', __name__)


@auth.post('/login')
def auth_login():
    """
    ---
    post:
        summary: Вход в систему
        requestBody:
            description: Логин и пароль пользователя
            required: true
            content:
                application/json:
                    schema: InputLoginSchema
        responses:
            '200':
                description: Успешный вход в систему
                content:
                    application/json:
                        schema: OutputLoginSchema
        tags:
        - auth
    """
    if current_user.is_authenticated:
        return { 'message': 'already login' }, 409

    if not request.is_json:
        return { 'message': 'error' }, 422

    request_json = request.get_json()
    if not ('login' in request_json and 'password' in request_json):
        return { 'message': 'error' }, 403

    login = request_json.get('login')
    password = request_json.get('password')
    user = User.query.filter_by(login=login).first()
    if not user or not check_password_hash(user.password_hash, password):
        return { 'message': 'error' }, 403

    login_user(user)
    return { 'message': 'success' }, 200


@auth.post('/logout')
@login_required
def auth_logout():
    """
    ---
    post:
        summary: Выход из системы
        responses:
            '200':
                description: Успешный выход из системы
                content:
                    application/json:
                        schema: OutputLoginSchema
        tags:
        - auth
    """
    logout_user()
    return { 'message': 'success' }, 200

import json
import os
import time
from http import HTTPStatus

from flask import Flask, redirect, url_for, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


os.environ['TZ'] = 'Europe/Moscow'
time.tzset()

db = SQLAlchemy()


def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI='sqlite:///db.sqlite'
    )
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .api import api as api_bp
    app.register_blueprint(api_bp)

    from .static_frontend import web as web_bp
    app.register_blueprint(web_bp)

    from .swagger import swagger_ui_blueprint, SWAGGER_URL
    app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

    from flaskr.api.api_spec import get_apispec

    @app.route('/swagger')
    def create_swagger_spec():
        return json.dumps(get_apispec(app).to_dict())

    @app.route('/<path:path>', methods=['OPTIONS'])
    def options(path):
        return ''

    @app.after_request
    def apply_allow_origin(response):
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        return response

    @login_manager.unauthorized_handler
    def unauthorized():
        if request.blueprint.startswith('api'):
            abort(HTTPStatus.UNAUTHORIZED)
        return redirect(url_for('web.auth.login_page'))

    return app

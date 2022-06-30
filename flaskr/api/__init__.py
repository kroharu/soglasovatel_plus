from flask import Blueprint, request
from werkzeug.security import check_password_hash
from flaskr.models import User, Company, Role
from flask_login import login_user, login_required, logout_user, current_user
from flaskr import db

api = Blueprint('api', __name__, url_prefix='/api')

from .auth import auth as auth_bp
api.register_blueprint(auth_bp)

from .contracts import contracts as contracts_bp
api.register_blueprint(contracts_bp)

from .company import company as company_bp
api.register_blueprint(company_bp)

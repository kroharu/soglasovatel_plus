import datetime

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import current_user, login_required, login_user, logout_user
from flaskr.models import User, Contract, CompaniesContract, Company, ContractVersion, ContractVersionsUsers
from sqlalchemy import or_, desc
from werkzeug.security import check_password_hash
from flaskr.data import contracts_added_by, contract_by_id, contracts_for, is_contract_agreed_by_all
from flaskr import db
from .helpers import time_left

web = Blueprint('web', __name__, url_prefix='/web')

from .auth import auth as auth_bp
web.register_blueprint(auth_bp)

from .contracts import contracts as contracts_bp
web.register_blueprint(contracts_bp)

from .types import types as types_bp
web.register_blueprint(types_bp)


@web.get('/')
@login_required
def main():
    contracts_for_sign = db.session.query(
        CompaniesContract.title,
        Contract.id,
        Contract.created_at,
        Contract.sent_at,
        Contract.signed_at,
        Contract.agreed_at,
        Company.name) \
        .select_from(Contract) \
        .join(CompaniesContract) \
        .join(Company, Company.id == CompaniesContract.recipient_id) \
        .filter(Contract.should_signed_by == current_user.id, Contract.agreed_at != None, Contract.sent_at == None) \
        .all()
    contracts_list = []
    for c in contracts_for_sign:
        contracts_list.append({
            'id': c.id,
            'title': c.title,
            'created_at': c.created_at,
            'sent_at': c.sent_at,
            'signed_at': c.signed_at,
            'agreed_at': c.agreed_at,
            'agreed_by_all': is_contract_agreed_by_all(c.id),
            'name': c.name,
        })
    return render_template('main.html',
                           added_contracts=contracts_added_by(current_user.id),
                           contracts_for=contracts_for(current_user.id),
                           contracts_for_sign=contracts_list,
                           datetime=datetime,
                           time_left=time_left)

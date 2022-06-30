from flask import render_template, Blueprint, redirect, url_for, request
from flask_login import login_required, current_user

from flaskr import db
from flaskr.data import users_by_company
from flaskr.models import ContractsType, ContractsTypesUsers

types = Blueprint('types', __name__, url_prefix='/types')


@types.get('/')
@login_required
def main():
    if current_user.role.can_add:
        ct = ContractsType.query.all()
        for ct_item in ct:
            ctu = ContractsTypesUsers.query.filter(
                ContractsTypesUsers.contract_type_id == ct_item.id,
                ContractsTypesUsers.company_id == current_user.role.company.id
            ).all()
            ct_users = set()
            for ctu_item in ctu:
                ct_users.add(ctu_item.user_id)
            ct_item.users = ct_users
        return render_template('types.html',
                               types=ct,
                               users=users_by_company(current_user.role.company.id, can_sign=False))
    else:
        return redirect(url_for('web.main'))


@types.post('/<t_id>/save')
@login_required
def save(t_id):
    if current_user.role.can_add:
        users_ids = request.form.getlist('users')

        ctu = ContractsTypesUsers.query.filter(
            ContractsTypesUsers.contract_type_id == t_id,
            ContractsTypesUsers.company_id == current_user.role.company.id
        ).delete()
        for u_id in users_ids:
            new_ctu = ContractsTypesUsers(contract_type_id=t_id,
                                          company_id=current_user.role.company.id,
                                          user_id=u_id)
            db.session.add(new_ctu)
        db.session.commit()
        return redirect(url_for('web.types.main'))
    else:
        return redirect(url_for('web.main'))

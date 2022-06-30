from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user

from flaskr import db
from flaskr.models import ContractsType, User, Role, ContractsTypesUsers, Company

company = Blueprint('company', __name__)


@company.post('/companies/search')
@login_required
def get_companies():
    """
    ---
    post:
        summary: Поиск компаний
        requestBody:
            description: Запрос
            required: true
            content:
                application/json:
                    schema: InputCompanySchema
        responses:
            '200':
                description: Возврат компаний, название которых начинается с запроса
                content:
                    application/json:
                        schema:
                            type: array
                            items: CompanySchema
            '403':
                description: Вы не можете загружать договоры
                content:
                    application/json:
                        schema: ErrorSchema
            '415':
                description: Передайте данные в виде json
                content:
                    application/json:
                        schema: ErrorSchema
            '400':
                description: Некорректные данные
                content:
                    application/json:
                        schema: ErrorSchema
        tags:
        - company
    """
    if not current_user.role.can_add:
        return jsonify({
            'status': 'error',
            'error': 'Вы не можете загружать договоры'
        }), 403

    if not request.is_json:
        return jsonify({
            'status': 'error',
            'error': 'Передайте данные в виде json'
        }), 415

    request_json = request.get_json()
    if 'name' not in request_json \
            or request_json['name'] == '':
        return jsonify({
            'status': 'error',
            'error': 'Некорретные данные'
        }), 400

    request_like = f"%{request_json['name']}%"
    companies = Company.query.filter(Company.name.ilike(request_like))
    companies_list = []
    for c in companies:
        companies_list.append({
            'id': c.id,
            'name': c.name,
            'inn': c.inn,
            'info': c.info,
        })

    return jsonify(companies_list)


@company.get('/company/contracts/types')
@login_required
def get_contracts_types():
    """
    ---
    get:
        summary: Получение типов договоров для текущей компании
        responses:
            '200':
                description: Возврат типов договоров с согласующими
                content:
                    application/json:
                        schema:
                            type: array
                            items: ContractsTypesSchema
            '403':
                description: У вас нет прав загружать договор
                content:
                    application/json:
                        schema: ErrorSchema
        tags:
        - company
    """
    if not current_user.role.can_add:
        jsonify({
            'status': 'error',
            'error': 'У вас нет прав загружать договор'
        }), 403
    ct = ContractsType.query.filter(ContractsType.company_id == current_user.role.company.id).all()
    ct_list = []
    for ct_item in ct:
        users_list = []
        users = db.session.query(User.id, User.name, Role.name.label('role_name'))\
            .select_from(ContractsTypesUsers)\
            .join(User)\
            .join(Role)\
            .filter(ContractsTypesUsers.contract_type_id == ct_item.id).all()
        for u in users:
            users_list.append({
                'id': u['id'],
                'name': u['name'],
                'role_name': u['role_name']
            })
        ct_list.append({
            'id': ct_item.id,
            'name': ct_item.name,
            'users': users_list
        })
    return jsonify(ct_list)


@company.post('/company/contracts/type')
@login_required
def post_comment():
    """
    ---
    post:
        summary: Создание нового типа договора
        requestBody:
            description: Название типа и согласующие пользователи
            required: true
            content:
                application/json:
                    schema: InputContractsTypesSchema
        responses:
            '200':
                description: Успешное добавление типа договора
                content:
                    application/json:
                        schema: OutputOkSchema
            '403':
                description: Вы не можете загружать договоры
                content:
                    application/json:
                        schema: ErrorSchema
            '415':
                description: Передайте данные в виде json
                content:
                    application/json:
                        schema: ErrorSchema
            '400':
                description: Некорректные данные
                content:
                    application/json:
                        schema: ErrorSchema
        tags:
        - company
    """
    if not current_user.role.can_add:
        return jsonify({
            'status': 'error',
            'error': 'Вы не можете загружать договоры'
        }), 403

    if not request.is_json:
        return jsonify({
            'status': 'error',
            'error': 'Передайте данные в виде json'
        }), 415

    request_json = request.get_json()
    if 'name' not in request_json\
            or request_json['name'] == ''\
            or 'users' not in request_json \
            or not len(request_json['users']) > 0:
        return jsonify({
            'status': 'error',
            'error': 'Некорретные данные'
        }), 400

    ct = ContractsType(
        name=request_json['name'],
        company_id=current_user.role.company.id
    )

    # TODO: add user_id verification from input
    for user in request_json['users']:
        ctu = ContractsTypesUsers(user_id=user)
        ct.users.append(ctu)

    db.session.add(ct)
    db.session.commit()

    return jsonify({
        'status': 'ok'
    })

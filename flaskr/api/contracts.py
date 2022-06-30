import datetime

from flask import Blueprint, request, jsonify, send_from_directory
from sqlalchemy import desc, func, or_

from flaskr import db
from flaskr.models import ContractVersion, User, Role, Company, Contract, ContractVersionsUsers, UsersComments, \
    CompaniesContract
from flask_login import login_required, current_user
from flaskr.data import upload_contract, contract_by_id, contract_agreements, users_by_company, sign_by_company, \
    contracts_added_by, is_contract_agreed_by_all, users_by_contract, update_contract, is_contract_still_agrees

contracts = Blueprint('contracts', __name__)


@contracts.get('/contracts/created')
@login_required
def contracts_by():
    """
    ---
    get:
        summary: Получение добавленных договоров текущего пользователя
        responses:
            '200':
                description: Возврат информации о договорах
                content:
                    application/json:
                        schema: ContractsAddedSchema
        tags:
        - contracts
    """

    result = []
    cab = contracts_added_by(current_user.id)
    for c in cab:
        result.append({
            'id': c.id,
            'title': c.title,
            'created_at': c.created_at
        })
    return jsonify(result)


@contracts.get('/company/users')
@login_required
def get_users():
    """
    ---
    get:
        summary: Получение подразделений компании
        responses:
            '200':
                description: Возврат информации о подразделениях
                content:
                    application/json:
                        schema: RolesSchema
            '403':
                description: Пользователь не имеет прав загружать договоры
                content:
                    application/json:
                        schema: ErrorSchema
        tags:
        - company
    """
    if current_user.role.can_add:
        users = db.session.query(User).join(Role).join(Company) \
            .filter(Company.id == current_user.role.company.id).all()
        roles = db.session.query(Role).join(Company) \
            .filter(Company.id == current_user.role.company.id).all()
        result = []
        for role in roles:
            _users = []
            for user in users:
                if user.role.id == role.id:
                    _users.append({'id': user.id, 'name': user.name})
            result.append({
                'role': role.name,
                'users': _users,
                'can_add': role.can_add,
                'can_sign': role.can_sign
            })
        return jsonify({
            'status': 'ok',
            'roles': result
        })
    else:
        return jsonify({
            'status': 'error',
            'error': 'У вас нет прав загружать договоры'
        }), 403


@contracts.get('/contract/<contract_id>')
@login_required
def get_by_id(contract_id):
    """
    ---
    get:
        summary: Получение договора по идентификатору
        parameters:
            - in: path
              name: contract_id
              schema:
                type: integer
              required: true
              description: идентификатор договора
        responses:
            '200':
                description:
                    "Возврат информации о договоре\n\n
                     Новое: initiator, recepeint"
                content:
                    application/json:
                        schema: OutputContractSchema
            '404':
                description: Договор не найден
                content:
                    application/json:
                        schema: ErrorSchema
        tags:
        - contracts
    """
    try:
        contract = contract_by_id(contract_id)
    except Exception:
        return jsonify({
            'status': 'error',
            'error': 'Договор не найден'
        }), 404
    agreements = contract_agreements(contract_id)
    initiator = Company.query.get(contract.companies_contract.recipient_id)
    recepeint = Company.query.get(contract.companies_contract.initiator_id)
    return jsonify({
        'status': 'ok',
        'contract': {
            'id': contract.id,
            'title': contract.companies_contract.title,
            'initiator': {
                'id': initiator.id,
                'name': initiator.name,
                'inn': initiator.inn
            },
            'recepeint': {
                'id': recepeint.id,
                'name': recepeint.name,
                'inn': recepeint.inn
            },
            'created_at': contract.created_at.strftime("%H:%M %d.%m.%Y"),
            'agreed_at': contract.agreed_at.strftime("%H:%M %d.%m.%Y") if contract.agreed_at is not None else None,
            'signed_at': contract.signed_at.strftime("%H:%M %d.%m.%Y") if contract.signed_at is not None else None,
            'agreed_by_all': is_contract_agreed_by_all(contract_id),
            'agreements': agreements
        }
    })


ALLOWED_EXTENSIONS = {'docx'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@contracts.post('/contract/upload')
@login_required
def upload():
    """
    ---
    post:
        summary: Загрузка договора
        requestBody:
            description:
                "Информация о договоре\n\n
                Устарело: title, agreements, partner, sign"
            required: true
            content:
                multipart/form-data:
                    schema: InputUploadContractSchema
        responses:
            '200':
                description: Возврат информации о договоре
                content:
                    application/json:
                        schema: OutputUploadContractSchema
            '400':
                description: Ошибка ввода
                content:
                    application/json:
                        schema: ErrorSchema
            '403':
                description: Пользователь не имеет прав загружать договоры
                content:
                    application/json:
                        schema: ErrorSchema
        tags:
        - contracts
    """
    if not current_user.role.can_add:
        return jsonify({'status': 'error', 'error': 'you can\t add new docs'}), 403
    if 'file' not in request.files \
            or request.files['file'] == '':
        return jsonify({'status': 'error', 'error': 'check fields'}), 400

    file = request.files['file']
    if not (file and allowed_file(file.filename)):
        return jsonify({'status': 'error', 'error': 'check file'}), 400

    c_id = upload_contract(file, current_user.id, current_user.id)

    return jsonify({
        'status': 'ok',
        'last_inserted_id': c_id
    })


@contracts.post('/contract/<c_id>/update')
@login_required
def update(c_id):
    """
    ---
    post:
        summary: Загрузка новой версии договора
        parameters:
            - in: path
              name: c_id
              schema:
                type: integer
              required: true
              description: идентификатор договора
        requestBody:
            description: Информация о договоре
            required: true
            content:
                multipart/form-data:
                    schema: InputUpdateContractSchema
        responses:
            '200':
                description: Возврат информации о договоре
                content:
                    application/json:
                        schema: OutputOkSchema
            '403':
                description: Пользователь не имеет прав загружать договоры
                content:
                    application/json:
                        schema: ErrorSchema
            '409':
                description: Текущая версия договора еще согласуется или уже согласована
                content:
                    application/json:
                        schema: ErrorSchema
            '400':
                description: Ошибка ввода
                content:
                    application/json:
                        schema: ErrorSchema
        tags:
        - contracts
    """
    if not current_user.role.can_add:
        return jsonify({'status': 'error', 'error': 'you can\t add new docs'}), 403

    if is_contract_still_agrees(c_id):
        return jsonify({
            'status': 'error',
            'error': 'Текущая версия договора еще согласуется'
        }), 409

    if is_contract_agreed_by_all(c_id):
        return jsonify({
            'status': 'error',
            'error': 'Текущая версия договора уже согласована'
        }), 409

    if 'file' not in request.files or request.files['file'] == '':
        return jsonify({'status': 'error', 'error': 'check fields'}), 400

    file = request.files['file']
    if not (file and allowed_file(file.filename)):
        return jsonify({'status': 'error', 'error': 'check file'}), 400

    update_contract(c_id, file, users_by_contract(c_id))

    return jsonify({
        'status': 'ok'
    })


@contracts.get('/contract/version/<cvu_id>/pdf')
@login_required
def get_pdf(cvu_id):
    """
    ---
    get:
        summary: Просмотр pdf определенной версии договора
        parameters:
            - in: path
              name: cvu_id
              schema:
                type: integer
              required: true
              description: версия договора для пользователя
        responses:
            '200':
                description: Возврат pdf договора
                content:
                    application/pdf:
                        schema:
                            type: file
            '404':
                description: Договор не найден
                content:
                    application/json:
                        schema: ErrorSchema
        tags:
        - contracts
    """
    cv = db.session.query(ContractVersion.filename)\
        .select_from(ContractVersion)\
        .join(ContractVersionsUsers)\
        .filter(ContractVersionsUsers.id == cvu_id)\
        .first()
    if cv is None:
        return jsonify({
            'status': 'error',
            'error': 'Договор не найден'
        }), 404
    return send_from_directory('../pdf', cv.filename + '.pdf')


@contracts.get('/contracts/for')
@login_required
def contracts_for():
    """
    ---
    get:
        summary: Получение договоров для согласования для текущего пользователя
        responses:
            '200':
                description: Возврат договоров для согласования
                content:
                    application/json:
                        schema: ContractsForSchema
        tags:
        - contracts
    """
    cv = db.session.query(Contract.title, ContractVersion.created_at, ContractVersionsUsers.id)\
        .select_from(ContractVersionsUsers)\
        .join(ContractVersion)\
        .join(Contract)\
        .filter(ContractVersionsUsers.status == None, ContractVersionsUsers.user_id == current_user.id).all()
    cv_list = []
    for c in cv:
        cv_list.append({
            'version': c.id,
            'title': c.title,
            'created_at': c.created_at.strftime("%H:%M %d.%m.%Y")
        })
    return jsonify({
        'status': 'ok',
        'contracts': cv_list
    })


@contracts.post('/comment/<cvu_id>')
@login_required
def post_comment(cvu_id):
    """
    ---
    post:
        summary: Согласование договора текущим пользователем
        parameters:
            - in: path
              name: cvu_id
              schema:
                type: integer
              required: true
              description: версия договора для пользователя
        requestBody:
            description: Статус и комментарии (при наличии)
            required: true
            content:
                application/json:
                    schema: CommentsSchema
        responses:
            '200':
                description: Успешное согласование
                content:
                    application/json:
                        schema: OutputOkSchema
            '404':
                description: Договор не найден
                content:
                    application/json:
                        schema: ErrorSchema
            '409':
                description: Некорректный договор
                content:
                    application/json:
                        schema: ErrorSchema
            '415':
                description: Передайте данные в виде json
                content:
                    application/json:
                        schema: ErrorSchema
            '400':
                description: Не переданы комментарии при согласовании с замечаниями
                content:
                    application/json:
                        schema: ErrorSchema
        tags:
        - comments
    """
    cvu = ContractVersionsUsers.query.get(int(cvu_id))
    if cvu is None:
        return jsonify({
            'status': 'error',
            'error': 'Договор не найден'
        }), 404

    if cvu.status is not None or cvu.user_id != current_user.id:
        return jsonify({
            'status': 'error',
            'error': 'Некорректный договор'
        }), 409

    if not request.is_json:
        return jsonify({
            'status': 'error',
            'error': 'Передайте данные в виде json'
        }), 415

    request_json = request.get_json()
    if not ('status' in request_json):
        return jsonify({
            'status': 'error',
            'error': 'На найден status'
        }), 403

    cvu.status = request_json['status']
    cvu.status_added_at = datetime.datetime.now()

    if not cvu.status\
            and (not ('comments' in request_json)
                 or not len(request_json['comments']) > 0):
        return jsonify({
            'status': 'error',
            'error': 'Не переданы комментарии при согласовании с замечаниями'
        }), 400
    else:
        for comment in request_json['comments']:
            user_comment = UsersComments(
                clause=comment['clause'],
                original=comment['original'],
                modified=comment['modified']
            )
            cvu.comments.append(user_comment)

    db.session.add(cvu)
    db.session.commit()

    return jsonify({
        'status': 'ok'
    })


@contracts.post('/contract/<c_id>/approve')
@login_required
def approve_contract(c_id):
    """
    ---
    post:
        summary: Визирование договора юристом
        parameters:
            - in: path
              name: c_id
              schema:
                type: integer
              required: true
              description: идентификатор договора
        responses:
            '200':
                description: Успешное визирование
                content:
                    application/json:
                        schema: OutputOkSchema
            '403':
                description: Вы не можете визировать этот договор
                content:
                    application/json:
                        schema: ErrorSchema
            '404':
                description: Договор не найден
                content:
                    application/json:
                        schema: ErrorSchema
            '409':
                description: Договор уже завизирован или еще не согласован
                content:
                    application/json:
                        schema: ErrorSchema
        tags:
        - contracts
    """
    c = Contract.query.get(int(c_id))
    if c is None:
        return jsonify({
            'status': 'error',
            'error': 'Договор не найден'
        }), 404

    if c.should_agreed_by != current_user.id:
        return jsonify({
            'status': 'error',
            'error': 'Вы не можете визировать этот договор'
        }), 403

    if not is_contract_agreed_by_all(c_id):
        return jsonify({
            'status': 'error',
            'error': 'Договор еще не согласован'
        }), 409

    if c.agreed_at is not None:
        return jsonify({
            'status': 'error',
            'error': 'Договор уже завизирован'
        }), 409

    c.agreed_at = datetime.datetime.now()

    db.session.add(c)
    db.session.commit()

    return jsonify({
        'status': 'ok'
    })


@contracts.post('/contract/<c_id>/sign')
@login_required
def sign_contract(c_id):
    """
    ---
    post:
        summary: Подписание договора директором
        parameters:
            - in: path
              name: c_id
              schema:
                type: integer
              required: true
              description: идентификатор договора
        responses:
            '200':
                description: Успешное подписание
                content:
                    application/json:
                        schema: OutputOkSchema
            '404':
                description: Договор не найден
                content:
                    application/json:
                        schema: ErrorSchema
            '403':
                description: Вы не можете подписывать договоры
                content:
                    application/json:
                        schema: ErrorSchema
            '409':
                description: Договор уже подписан, еще не завизирован или еще не согласован
                content:
                    application/json:
                        schema: ErrorSchema
        tags:
        - contracts
    """
    c = Contract.query.get(int(c_id))
    if c is None:
        return jsonify({
            'status': 'error',
            'error': 'Договор не найден'
        }), 404

    if not current_user.role.can_sign:
        return jsonify({
            'status': 'error',
            'error': 'Вы не можете подписывать договоры'
        }), 403

    if not is_contract_agreed_by_all(c_id):
        return jsonify({
            'status': 'error',
            'error': 'Договор еще не согласован'
        }), 409

    if c.agreed_at is None:
        return jsonify({
            'status': 'error',
            'error': 'Договор еще не завизирован'
        }), 409

    if c.signed_at is not None:
        return jsonify({
            'status': 'error',
            'error': 'Договор уже подписан'
        }), 409

    c.signed_at = datetime.datetime.now()

    db.session.add(c)
    db.session.commit()

    return jsonify({
        'status': 'ok'
    })


@contracts.post('/contract/<c_id>/send')
@login_required
def send_contract(c_id):
    """
    ---
    post:
        summary: Отправка договора компании контрагенту
        parameters:
            - in: path
              name: c_id
              schema:
                type: integer
              required: true
              description: идентификатор договора
        responses:
            '200':
                description: Успешная отправка
                content:
                    application/json:
                        schema: OutputOkSchema
            '404':
                description: Договор не найден
                content:
                    application/json:
                        schema: ErrorSchema
            '403':
                description: Вы не можете отправлять договоры
                content:
                    application/json:
                        schema: ErrorSchema
            '409':
                description: Договор уже отправлен, еще не подписан, еще не завизирован или еще не согласован
                content:
                    application/json:
                        schema: ErrorSchema
        tags:
        - contracts
    """
    c = Contract.query.get(int(c_id))
    if c is None:
        return jsonify({
            'status': 'error',
            'error': 'Договор не найден'
        }), 404

    if not current_user.role.can_add:
        return jsonify({
            'status': 'error',
            'error': 'Вы не можете отправлять договоры'
        }), 403

    if not is_contract_agreed_by_all(c_id):
        return jsonify({
            'status': 'error',
            'error': 'Договор еще не согласован'
        }), 409

    if c.agreed_at is None:
        return jsonify({
            'status': 'error',
            'error': 'Договор еще не завизирован'
        }), 409

    if c.signed_at is None:
        return jsonify({
            'status': 'error',
            'error': 'Договор еще не подписан'
        }), 409

    if c.sent_at is not None:
        return jsonify({
            'status': 'error',
            'error': 'Договор уже отправлен'
        }), 409

    c.sent_at = datetime.datetime.now()

    db.session.add(c)
    db.session.commit()

    return jsonify({
        'status': 'ok'
    })
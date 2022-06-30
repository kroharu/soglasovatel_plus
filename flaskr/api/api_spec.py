from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from marshmallow import Schema, fields


DOCS_FILENAME = 'docs.yaml'


class ErrorSchema(Schema):
    status = fields.Str()
    error = fields.Str()


class InputLoginSchema(Schema):
    login = fields.Str(required=True)
    password = fields.Str(required=True)


class OutputLoginSchema(Schema):
    status = fields.Str()


class AgreementCommentSchema(Schema):
    clause = fields.Str()
    original = fields.Str()
    modified = fields.Str()


class AgreementSchema(Schema):
    name = fields.Str()
    role_name = fields.Str()
    status = fields.Bool(allow_none=True)
    user_id = fields.Int()
    comments = fields.Nested(AgreementCommentSchema, many=True, allow_none=True)


class ContractCompanySchema(Schema):
    id = fields.Int()
    name = fields.Str()
    inn = fields.Str()


class ContractSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    created_at = fields.Str()
    agreed_at = fields.Str(allow_none=True)
    signed_at = fields.Str(allow_none=True)
    title = fields.Str()
    agreed_by_all = fields.Bool()
    agreement = fields.Nested(AgreementSchema, many=True)
    initiator = fields.Nested(ContractCompanySchema)
    recepeint = fields.Nested(ContractCompanySchema)


class OutputContractSchema(Schema):
    status = fields.Str()
    contract = fields.Nested(ContractSchema, many=True)


class InputUpdateContractSchema(Schema):
    file = fields.Raw(type='file', required=True)


class InputUploadContractSchema(Schema):
    title = fields.Str()
    partner = fields.Str()
    file = fields.Raw(type='file', required=True)
    agreements = fields.List(fields.Integer())
    sign = fields.Int()


class OutputUploadContractSchema(Schema):
    status = fields.Str()
    last_inserted_id = fields.Int()


class UserSchema(Schema):
    id = fields.Integer()
    name = fields.Str()


class RoleSchema(Schema):
    name = fields.Str()
    users = fields.Nested(UserSchema, many=True)


class RolesSchema(Schema):
    status = fields.Str()
    roles = fields.Nested(RoleSchema, many=True)
    can_add = fields.Bool()
    can_sign = fields.Bool()


class ContractVersionSchema(Schema):
    cvu_id = fields.Integer()
    title = fields.Str()
    created_at = fields.Str()


class ContractsForSchema(Schema):
    status = fields.Str()
    contracts = fields.Nested(ContractVersionSchema, many=True)
    
    
class ContractAddedSchema(Schema):
    id = fields.Integer()
    title = fields.Str()
    created_at = fields.Str()
    
    
class ContractsAddedSchema(Schema):
    status = fields.Str()
    contracts = fields.Nested(ContractAddedSchema, many=True)


class CommentSchema(Schema):
    clause = fields.Str(required=True)
    original = fields.Str(required=True)
    modified = fields.Str(required=True)


class CommentsSchema(Schema):
    status = fields.Bool(required=True)
    comments = fields.Nested(CommentSchema, many=True)


class OutputOkSchema(Schema):
    status = fields.Str()


class UsersContractsTypesSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    role_name = fields.Str()


class ContractsTypesSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    users = fields.Nested(UsersContractsTypesSchema, many=True)


class InputContractsTypesSchema(Schema):
    name = fields.Str()
    users = fields.List(fields.Integer)


class InputCompanySchema(Schema):
    name = fields.Str()


class CompanySchema(Schema):
    id = fields.Int()
    name = fields.Str()
    inn = fields.Str()
    info = fields.List(fields.Str())


def create_tags(spec):
    """ Создаем теги.

    :param spec: объект APISpec для сохранения тегов
    """
    tags = [
        {'name': 'auth', 'description': 'Авторизация'},
        {'name': 'contracts', 'description': 'Договоры'},
        {'name': 'company', 'description': 'Компания'},
        {'name': 'comments', 'description': 'Комментарии'},
    ]

    for tag in tags:
        print(f"Добавляем тег: {tag['name']}")
        spec.tag(tag)


def load_docstrings(spec, app):
    """ Загружаем описание API.

    :param spec: объект APISpec, куда загружаем описание функций
    :param app: экземпляр Flask приложения, откуда берем описание функций
    """
    for fn_name in app.view_functions:
        if fn_name == 'static':
            continue
        print(f'Загружаем описание для функции: {fn_name}')
        view_fn = app.view_functions[fn_name]
        spec.path(view=view_fn)


def get_apispec(app):
    """ Формируем объект APISpec.

    :param app: объект Flask приложения
    """
    spec = APISpec(
        title="СогласовательПлюс API",
        version="0.2.0",
        openapi_version="3.0.3",
        plugins=[FlaskPlugin(), MarshmallowPlugin()],
    )

    create_tags(spec)

    load_docstrings(spec, app)

    return spec


def write_yaml_file(spec: APISpec):
    """ Экспортируем объект APISpec в YAML файл.
    :param spec: объект APISpec
    """
    with open(DOCS_FILENAME, 'w') as file:
        file.write(spec.to_yaml())
    print(f'Сохранили документацию в {DOCS_FILENAME}')
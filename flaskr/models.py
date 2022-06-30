import datetime
from flask_login import UserMixin
from . import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50), unique=True)
    password_hash = db.Column(db.String(150))
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    can_add = db.Column(db.Boolean, default=False)
    can_sign = db.Column(db.Boolean, default=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))

    users = db.relationship('User', backref='role')


class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    inn = db.Column(db.String(50))
    info = db.Column(db.String(100))
    admin_email = db.Column(db.String(100))
    admin_password_hash = db.Column(db.String(100))

    roles = db.relationship('Role', backref='company')


class Contract(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    companies_contract_id = db.Column(db.Integer, db.ForeignKey('companies_contract.id'))
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    should_agreed_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    agreed_at = db.Column(db.DateTime, nullable=True)
    should_signed_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    signed_at = db.Column(db.DateTime, nullable=True)
    sent_at = db.Column(db.DateTime, nullable=True)

    # user = db.relationship('User', backref='added_contracts')
    versions = db.relationship('ContractVersion', backref='contract')
    companies_contract = db.relationship('CompaniesContract', back_populates='contracts')

    # TODO: delete title from contract table
    title = db.Column(db.String(50))


class ContractVersion(db.Model):
    __tablename__ = 'contract_version'
    id = db.Column(db.Integer, primary_key=True)
    contract_id = db.Column(db.Integer, db.ForeignKey('contract.id'))
    filename = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)

    agreements = db.relationship('ContractVersionsUsers', back_populates='contract_version')


class ContractVersionsUsers(db.Model):
    __tablename__ = 'contract_versions_users'
    id = db.Column(db.Integer, primary_key=True)
    contract_version_id = db.Column(db.Integer, db.ForeignKey('contract_version.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    status = db.Column(db.Boolean)
    status_added_at = db.Column(db.DateTime)

    contract_version = db.relationship('ContractVersion', back_populates='agreements')
    comments = db.relationship('UsersComments', backref='contract_versions_user')


class UsersComments(db.Model):
    __tablename__ = 'users_comments'
    id = db.Column(db.Integer, primary_key=True)
    versions_users_id = db.Column(db.Integer, db.ForeignKey('contract_versions_users.id'))
    clause = db.Column(db.String(100))
    original = db.Column(db.String(1000))
    modified = db.Column(db.String(1000))


class CompaniesContract(db.Model):
    __tablename__ = 'companies_contract'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    type = db.Column(db.Integer)
    initiator_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('company.id'))

    contracts = db.relationship('Contract', back_populates='companies_contract')


class ContractsType(db.Model):
    __tablename__ = 'contracts_type'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    token = db.Column(db.String)


class ContractsTypesUsers(db.Model):
    __tablename__ = 'contracts_types_users'
    id = db.Column(db.Integer, primary_key=True)
    contract_type_id = db.Column(db.Integer, db.ForeignKey('contracts_type.id'))
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    user = db.relationship('User')

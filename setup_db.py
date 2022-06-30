from datetime import datetime

from flaskr import db, create_app
from flaskr.models import User, Role, Company, Contract, ContractVersion, ContractVersionsUsers, UsersComments, \
    ContractsType, ContractsTypesUsers
from werkzeug.security import generate_password_hash

app = create_app()
app.app_context().push()
# db.init_app()
db.drop_all()
db.create_all()

companyA = Company(name='ООО "Орион"', inn='5034024175')
role1 = Role(name='Юридический отдел', can_add=True)
user1 = User(login='юрист',
             password_hash=generate_password_hash('юрист'),
             name='Виноградов Рудольф Наумович',
             email='gooddimkin@yandex.ru')
role1.users.append(user1)
role2 = Role(name='Бухгалтерия')
user2 = User(login='бухгалтер',
             password_hash=generate_password_hash('бухгалтер'),
             name='Ефимова Аделия Игоревна',
             email='gooddimkin@yandex.ru')
role2.users.append(user2)
role3 = Role(name='Отдел аренды')
user3 = User(login='аренда',
             password_hash=generate_password_hash('аренда'),
             name='Дубов Илья Елисеевич',
             email='gooddimkin@yandex.ru')
role3.users.append(user3)
role4 = Role(name='Директор', can_sign=True)
user4 = User(login='директор',
             password_hash=generate_password_hash('директор'),
             name='Зайцев Илларион Денисович',
             email='gooddimkin@yandex.ru')
role4.users.append(user4)
companyA.roles.extend([role1, role2, role3, role4])
companyB = Company(name='ООО "Рассвет"', inn='9715220265')
companyС = Company(name='ООО "Закат"', inn='9715221234')

ct1 = ContractsType(name='Договор аренды', token='аренд')
ct2 = ContractsType(name='Договор поставки', token='постав')

db.session.add_all([companyA, companyB, companyС, ct1, ct2])
db.session.commit()

ctu1 = ContractsTypesUsers(contract_type_id=ct1.id, user_id=user2.id, company_id=companyA.id)
ctu2 = ContractsTypesUsers(contract_type_id=ct1.id, user_id=user3.id, company_id=companyA.id)
ctu3 = ContractsTypesUsers(contract_type_id=ct2.id, user_id=user2.id, company_id=companyA.id)
db.session.add_all([ctu1, ctu2, ctu3])
db.session.commit()

# c = Contract(title='Договор аренды 1',
#              created_by=user1.id,
#              should_agreed_by=user1.id,
#              should_signed_by=user3.id)
# cv = ContractVersion(filename='document.docx')
# c.versions.append(cv)
# cvu = ContractVersionsUsers(user_id=user2.id)
# cv.agreements.append(cvu)
# db.session.add_all([c])
# db.session.commit()
#
# uc1 = UsersComments(clause='п. 1.2.1',
#                     original='Исходный текст',
#                     modified='Исправленный текст')
# uc2 = UsersComments(clause='п. 1.2.3',
#                     original='Исходный текст 2',
#                     modified='Исправленный текст 2')
# cvu.status = False
# cvu.status_added_at = datetime.now()
# cvu.comments.extend([uc1, uc2])
# db.session.add_all([cv])
# db.session.commit()

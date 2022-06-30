import datetime

from flask import Blueprint, render_template, request, flash, redirect, url_for, send_from_directory, abort
from flask_login import login_required, current_user

from sqlalchemy import desc
from flaskr import db
from flaskr.data import contract_by_id, contract_agreements, users_by_company, sign_by_company, upload_contract
from flaskr.data import add_comment, users_by_contract, update_contract, convert_to
from flaskr.models import Contract, User, ContractVersion, ContractVersionsUsers, CompaniesContract, Company, Role
from flaskr.models import ContractsTypesUsers
from flaskr.static_frontend import time_left
import subprocess
import smtplib
from email.mime.text import MIMEText

contracts = Blueprint('contracts', __name__)

MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465

MAIL_USERNAME = 'soglasovatel.plus.team2@gmail.com'
MAIL_PASSWORD = 'qaz135wsx'

@contracts.get('/contract/<contract_id>')
@login_required
def page(contract_id):
    ca = contract_agreements(contract_id)
    users = {}
    for a in ca:
        users[a['name']] = a['status']
    new = True
    for k in users:
        if users[k] is None:
            break
        else:
            new = new and users[k]
    return render_template('contract.html',
                           contract=contract_by_id(contract_id),
                           agreements=ca,
                           new=not new,
                           datetime=datetime,
                           time_left=time_left,
                           current_user=current_user)


@contracts.get('/contract/upload')
@login_required
def upload_page():
    return render_template('contract_upload.html',
                           users=users_by_company(current_user.role.company.id),
                           signs=sign_by_company(current_user.role.company.id))


ALLOWED_EXTENSIONS = {'docx'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@contracts.post('/contract_upload')
@login_required
def upload():
    if 'file' not in request.files or request.files['file'] == '':
        flash('Проверьте ввод')
        return redirect(url_for('web.contracts.upload_page'))

    file = request.files['file']
    if not (file and allowed_file(file.filename)):
        flash('Некорретный файл')
        return redirect(url_for('web.contract.upload_page'))
        return redirect(url_for('web.contracts.upload_page'))

    try:
        c_id = upload_contract(file, current_user.id, current_user.id)
    except Exception:
        return redirect(url_for('web.contracts.upload_page'))

    return redirect(url_for('web.contracts.page', contract_id=c_id))


@contracts.get('/contract/version/<int:v_id>/pdf')
@login_required
def get_pdf(v_id):
    cv = ContractVersion.query.get(v_id)
    if cv is None:
        abort(404)
    # TODO: заменить пути на абсолютные и добавить их в app config
    return send_from_directory('../pdf', cv.filename + '.pdf')


@contracts.get('/contract/<c_id>/result/docx')
@login_required
def result_docx(c_id):
    cv = db.session.query(CompaniesContract.title, ContractVersion.filename)\
        .select_from(ContractVersion)\
        .join(Contract)\
        .join(CompaniesContract)\
        .filter(Contract.id == c_id)\
        .order_by(desc(ContractVersion.created_at)).first()
    if cv is None:
        abort(404)
    # TODO: заменить пути на абсолютные и добавить их в app config
    return send_from_directory('../files',
                               cv.filename + '.docx',
                               as_attachment=True,
                               download_name=cv.title + '.docx')


@contracts.get('/contract/<c_id>/result/pdf')
@login_required
def result_pdf(c_id):
    cv = db.session.query(CompaniesContract.title, ContractVersion.filename)\
        .select_from(ContractVersion)\
        .join(Contract)\
        .join(CompaniesContract)\
        .filter(Contract.id == c_id)\
        .order_by(desc(ContractVersion.created_at)).first()
    if cv is None:
        abort(404)
    # TODO: заменить пути на абсолютные и добавить их в app config
    return send_from_directory('../pdf',
                               cv.filename + '.pdf',
                               as_attachment=True,
                               download_name=cv.title + '.pdf')


@contracts.get('/contract/<c_id>/approval_sheet/docx')
@login_required
def approval_sheet_docx(c_id):
    from flaskr.data.createListDocx import create_list_docx
    create_list_docx(c_id)
    # TODO: заменить пути на абсолютные и добавить их в app config
    return send_from_directory('../files',
                               'Лист согласования.docx',
                               as_attachment=True,
                               download_name='Лист согласования.docx')


@contracts.get('/contract/<c_id>/approval_sheet/pdf')
@login_required
def approval_sheet_pdf(c_id):
    from flaskr.data.createListDocx import create_list_docx
    create_list_docx(c_id)
    import os
    convert_to('pdf', os.path.join('files', 'Лист согласования.docx'), timeout=15)
    # TODO: заменить пути на абсолютные и добавить их в app config
    return send_from_directory('../pdf',
                               'Лист согласования.pdf',
                               as_attachment=True,
                               download_name='Лист согласования.pdf')


@contracts.get('/contract/version/<cvu_id>/comment')
@login_required
def comment_page(cvu_id):
    c = db.session.query(CompaniesContract.title,
                         Company.name,
                         Contract.created_at,
                         ContractVersion.id)\
        .select_from(ContractVersionsUsers)\
        .join(ContractVersion)\
        .join(Contract)\
        .join(CompaniesContract)\
        .join(Company, Company.id == CompaniesContract.recipient_id)\
        .filter(ContractVersionsUsers.id == cvu_id)
    return render_template('comment.html', contract=c.first(), cvu_id=cvu_id, datetime=datetime, time_left=time_left)


@contracts.post('/contract/version/<cvu_id>/comment')
@login_required
def comment(cvu_id):
    c = db.session.query(CompaniesContract.title) \
        .select_from(ContractVersionsUsers) \
        .join(ContractVersion) \
        .join(Contract) \
        .join(CompaniesContract) \
        .filter(ContractVersionsUsers.id == cvu_id).first()

    status = request.form.get('status')
    clause = request.form.getlist('clause')
    original = request.form.getlist('original')
    modified = request.form.getlist('modified')
    comments = []
    for i in range(len(clause)):
        comments.append({
            'clause': clause[0],
            'original': original[0],
            'modified': modified[0],
        })
    if status == '1':
        flash(c.title + ' согласован')
        add_comment(cvu_id, True)
    else:
        flash(c.title + ' согласован с правками')
        add_comment(cvu_id, False, comments)
    return redirect(url_for('web.main'))


@contracts.get('/contract/update/new/<c_id>')
@login_required
def update_page(c_id):
    return render_template('contract_upload_new.html',
                           users=users_by_contract(c_id), c_id=c_id)


@contracts.post('/contract/update/new/<c_id>')
@login_required
def update(c_id):
    if 'file' not in request.files \
            or request.files['file'] == '':
        flash('Проверьте ввод')
        return redirect(url_for('web.contracts.update_page'))

    file = request.files['file']
    if not (file and allowed_file(file.filename)):
        flash('Некорретный файл')
        return redirect(url_for('web.contracts.update_page'))

    c_id = update_contract(c_id, file, users_by_contract(c_id))

    return redirect(url_for('web.contracts.page', contract_id=c_id))


@contracts.post('/contract/<c_id>/approve')
@login_required
def approve(c_id):
    c = Contract.query.get(int(c_id))
    c.agreed_at = datetime.datetime.now()
    db.session.add(c)
    db.session.commit()

    FROM = MAIL_USERNAME
    TO = 'gooddimkin@yandex.ru'

    msg = 'Уважаемый(ая), Зайцев Илларион Денисович\n\n Вам пришёл договор на подпись.\n Для его просмотра перейдите по ссылке: http://kpint.site/web/login\n\n С уважением,\n СогласовательПлюс'
    msg = MIMEText('\n {}'.format(msg).encode('utf-8'), _charset='utf-8')

    smtpObj = smtplib.SMTP_SSL(MAIL_SERVER, MAIL_PORT)
    smtpObj.ehlo()
    smtpObj.login(MAIL_USERNAME, MAIL_PASSWORD)

    smtpObj.sendmail(FROM, TO, 
            'Subject: СогласовательПлюс - договор на подпись. \n{}'.format(msg).encode('utf-8'))
    smtpObj.quit()

    return redirect(url_for('web.contracts.page', contract_id=c_id))


@contracts.post('/contract/<c_id>/sign')
@login_required
def sign(c_id):
    c = Contract.query.get(int(c_id))
    c.signed_at = datetime.datetime.now()
    db.session.add(c)
    db.session.commit()

    FROM = MAIL_USERNAME
    TO = 'gooddimkin@yandex.ru'

    msg = 'Уважаемый(ая), Виноградов Рудольф Наумович\n\n Вам пришёл подписанный договор для отправки контрагенту.\n Для его просмотра перейдите по ссылке: http://kpint.site/web/login\n\n С уважением,\n СогласовательПлюс'
    msg = MIMEText('\n {}'.format(msg).encode('utf-8'), _charset='utf-8')

    smtpObj = smtplib.SMTP_SSL(MAIL_SERVER, MAIL_PORT)
    smtpObj.ehlo()
    smtpObj.login(MAIL_USERNAME, MAIL_PASSWORD)

    smtpObj.sendmail(FROM, TO, 
            'Subject: СогласовательПлюс - договор на отправку контрагенту. \n{}'.format(msg).encode('utf-8'))
    smtpObj.quit()

    return redirect(url_for('web.contracts.page', contract_id=c_id))


@contracts.post('/contract/<c_id>/send')
@login_required
def send(c_id):
    c = Contract.query.get(int(c_id))
    c.sent_at = datetime.datetime.now()
    db.session.add(c)
    db.session.commit()

    return redirect(url_for('web.contracts.page', contract_id=c_id))

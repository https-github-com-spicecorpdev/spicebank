from flask import render_template, flash, redirect, url_for, request
from . import create_manager_app, get_repositories, get_manager_repositories
from flask_login import login_user, current_user, login_required, logout_user
from .statement import Statement
from .address import Address
from .user import User
from .account import Account
from .manager import Manager
import logging
import time

app, login_manager = create_manager_app()

accountDatabase, statementDatabase, solicitationDatabase, bankDatabase, userDatabase, agencyDatabase = get_repositories()

managerDatabase = get_manager_repositories()

@app.context_processor
def current_time():
    return {'date': time.strftime('%d/%m/%Y %H:%M:%S')}

@app.context_processor
def current_manager():
    manager = current_user
    return {'manager': manager}

@app.route('/')
@login_required
def index():
    manager = current_user
    today = time.strftime('%d/%m/%Y %H:%M:%S')
    if manager.is_general_manager():
        bank_balance = bankDatabase.find_capital_by_id(1)
        if bank_balance <= 0:
            return render_template('capital.html'), 200
    return render_template('admhome.html',manager= manager,date=today), 200

@app.route('/capitalconfirm', methods = ['GET', 'POST'])
@login_required
def capital_confirm():
    manager = current_user
    today = time.strftime('%d/%m/%Y %H:%M:%S')
    value = request.form['fvalor']
    bankDatabase.update_bank_capital(1, value)
    return render_template('admhome.html',manager = manager,date = today), 200

@app.route('/balanceconfirm', methods = ['POST'])
@login_required
def balance_confirm():
    value = request.form['fvalor']
    return render_template('capitalconfirm.html', valor = value), 200

@login_manager.unauthorized_handler
def unauthorized():
    return render_template('loginGerente.html')

@login_manager.user_loader
def load_user(user_id):
    user = userDatabase.findById(user_id)
    return managerDatabase.find_by_user_id(user.id)

@app.route('/logout')
@login_required
def logoutmanager():
    logout_user()
    return render_template('loginGerente.html'), 200

@app.route('/loginGerente' , methods = ['GET'])
def admForm():
    return render_template('loginGerente.html'), 200

@app.route('/loginGerente', methods = ['POST'])
def loginGerente():
    today = time.strftime('%d/%m/%Y %H:%M:%S')
    if not validate_form(request.form):
        flash('Preencha todos os campos!')
        return render_template('loginGerente.html'), 400
    manager = managerDatabase.findByRegistrationNumberAndPassword (request.form['fmatricula'], request.form['fpassword'],)
    if manager:
        login_user(manager)
        return render_template('admhome.html', manager=manager, date=today), 200
    else:
        flash(f'Login inválido, verifique os dados de acesso!')
    return render_template('loginGerente.html'), 400

@app.route('/<user_id>/<action>/<id>/<type>/solicitacao',methods = ['GET','POST'])
@login_required
def solicitacao(user_id,action,id,type):
    manager=current_user
    if type=='Abertura de conta':
        account_approval(manager, user_id, action, id)
    elif type== 'Confirmação de depósito':
        deposit_approval(user_id, action, id)
        logging.info(f'ID: {user_id}, id_solicitation: {id}')
    elif type== 'Alteração de dados cadastrais':
        update_user_approval(user_id, action, id)
    elif type == 'Encerrar conta':
        close_account_approval(user_id, action, id)
    solicitations=solicitationDatabase.find_by_work_agency_id(manager.workAgency)
    return render_template('admsolicitations.html', solicitacoes=solicitations, manager = manager), 200

@app.route('/aprovar/<user_id>/<acao>/<id>/<type>/account/approval',methods = ['GET','POST'])
@login_required
def account_approval_by_general_manager(user_id,acao,id,type):
    agency_manager_id = request.form['fmanager']
    manager = managerDatabase.findById(agency_manager_id)
    if manager:
        if type=='Abertura de conta':
            account_approval(manager, user_id, acao, id)
    solicitations=solicitationDatabase.find_by_work_agency_id(current_user.workAgency)
    return render_template('admsolicitations.html', solicitacoes=solicitations, manager = current_user), 200

@app.route('/admsolicitations', methods = ['GET'])
@login_required
def solicitations():
    manager= current_user
    solicitations=solicitationDatabase.find_by_work_agency_id(manager.workAgency)
    return render_template('admsolicitations.html', solicitacoes=solicitations, manager = manager), 200

@app.route('/admsolicitationsgeral', methods = ['GET'])
@login_required
def solicitations_geral():
    manager= current_user
    solicitations=solicitationDatabase.find_solicitations_by_general_manager(manager.registrationNumber)
    return render_template('admsolicitations.html', solicitacoes=solicitations, manager = manager), 200

@app.route('/adm')
@login_required
def adm():
    manager= current_user
    users=userDatabase.find_all_users(manager)
    return render_template('admusers.html', users = users, manager = manager), 200

@app.route('/admagencycreation', methods = ['GET'])
@login_required
def admagencycreation():
    managers = managerDatabase.find_all_agency_manager_without_work_agency()
    return render_template('admagencycreation.html', managers = managers), 200

@app.route('/admagencycreation', methods = ['POST'])
@login_required
def perform_admagency_creation():
    agency_id = agencyDatabase.create_agency(1)
    manager_id = request.form['fmanager']
    logging.info(f'agency {agency_id}, manager {manager_id}')
    managerDatabase.update_work_agency_id_by_maganer_id(agency_id, manager_id)
    agencies = agencyDatabase.find_all_agencies()
    return render_template('admagency.html', agencies = agencies), 200


@app.route('/admagencymanagers', methods = ['GET'])
@login_required
def admagencymanagers():
    manager = current_user
    managers = managerDatabase.find_all_agency_manager()
    return render_template('admmanagers.html', managers = managers, manager = manager), 200


@app.route('/<user_id>/admuserdetails')
@login_required
def adm_user_details(user_id):
    manager = current_user
    user = userDatabase.findById(user_id)
    target_manager = managerDatabase.find_by_user_id(user.id)
    if target_manager:
        return render_template('admagencymanagerdetail.html', target_manager = target_manager, manager = manager), 200
    else:
        return render_template('admusersdetail.html', user = user, manager = manager), 200

@app.route('/admagency', methods = ['GET'])
@login_required
def admagency():
    manager = current_user
    agencies = agencyDatabase.find_all_agencies()
    return render_template('admagency.html', agencies = agencies, manager = manager), 200


@app.route('/admprofile', methods = ['POST', 'GET'])
@login_required
def admprofile():
    manager=current_user
    today = time.strftime('%d/%m/%Y %H:%M:%S')
    user = userDatabase.findById(manager.id)
    logging.info(f'{user}')
    if request.method == 'POST':
        address = Address(request.form['froad'], request.form['fnumberHouse'], request.form['fdistrict'], request.form['fcity'], request.form['fstate'], request.form['fcep'])
        logging.info(f'{address}')
        manager_update = User(manager.id, request.form['fname'], user.cpf, user.password, user.birthDate, request.form['fgenre'], address=address)
        userDatabase.update_user_data_by_manager(manager_update)
        flash('Dados alterados com sucesso!')
        return render_template('admhome.html',manager=manager, date=today), 200
    # return redirect(url_for('adm')), 200
    return render_template('admprofile.html', user = user, manager = manager), 200

@app.route('/admprofilegeneral', methods = ['POST', 'GET'])
@login_required
def admprofile_general():
    manager=current_user
    today = time.strftime('%d/%m/%Y %H:%M:%S')
    user = userDatabase.findById(manager.id)
    logging.info(f'{user}')
    if request.method == 'POST':
        address = Address(request.form['froad'], request.form['fnumberHouse'], request.form['fdistrict'], request.form['fcity'], request.form['fstate'], request.form['fcep'])
        logging.info(f'{address}')
        manager_update = User(manager.id, request.form['fname'], user.cpf, user.password, user.birthDate, request.form['fgenre'], address=address)
        userDatabase.update_user_data_by_manager(manager_update)
        message= flash('Dados alterados com sucesso!')
        return render_template('adm_geral_home.html',manager= manager,date=today), 200
    # return redirect(url_for('adm')), 200
    return render_template('admprofile_general.html', manager = user), 200

@app.route('/<user_id>/admeditdatauser', methods = ['POST','GET'])
@login_required
def adm_edit_data_user(user_id):
    manager=current_user
    user = userDatabase.findById(user_id)
    userDatabase.find_all_users(manager)
    address = Address(request.form['froad'], request.form['fnumberHouse'], request.form['fdistrict'], request.form['fcity'], request.form['fstate'], request.form['fcep'])
    user_update = User(user_id, request.form['fname'], user.cpf, user.password, user.birthDate, request.form['fgenre'], address=address)
    userDatabase.update_user_data_by_manager(user_update)
    flash('Dados alterados com sucesso!')
    if request.method == 'POST':
        return render_template('admhome.html',manager=manager), 200

@app.route('/<user_id>/<solicitation_id>/<type>/details')
@login_required
def details(user_id,solicitation_id,type):
    manager=current_user
    if type == 'Alteração de dados cadastrais':
        update_user_solicitation = solicitationDatabase.find_update_user_solicitation_by_id_solicitation(solicitation_id, user_id)
        user = userDatabase.findById(user_id)
        return render_template('admapprovedatachange.html', solicitation=update_user_solicitation, user=user, manager = manager), 200
    elif type == 'Encerrar conta':
        solicitation = solicitationDatabase.find_by_id(solicitation_id)
        user = userDatabase.findById(user_id)
        return render_template('admapprovedeleteaccount.html', user = user, solicitation = solicitation, manager = manager), 200
    elif type =='Confirmação de depósito':
        user = userDatabase.findById(user_id)
        solicitation = solicitationDatabase.find_deposit_solicitation_by_id_solicitation(solicitation_id)
        return render_template('admdepositconfirm.html', user = user, solicitation = solicitation, manager = manager), 200
    elif type == 'Abertura de conta':
        open_account_solicitation = solicitationDatabase.find_open_account_solicitation_by_id(solicitation_id)
        user = userDatabase.findById(user_id)
        managers = managerDatabase.find_all_agency_manager()
        return render_template('admdetailsuserapprove.html', solicitation=open_account_solicitation, user=user, managers = managers,  manager = manager), 200
    else:
        solicitations=solicitationDatabase.find_by_work_agency_id(manager.workAgency)
        return render_template('admsolicitations.html', solicitacoes=solicitations, manager = manager), 200

@app.route('/<user_id>/<solicitation_id>/withdraw-close', methods = ['GET'])
@login_required
def withdraw_and_close_account_view(user_id,solicitation_id):
    logging.info(f'withdraw_and_close_account_view::({user_id},{solicitation_id})')
    manager = current_user
    user = userDatabase.findById(user_id)
    return render_template('admwithdrawconfirm.html', user = user, id_solicitation = solicitation_id, manager = manager), 200

@app.route('/<user_id>/<solicitation_id>/withdraw-approval', methods = ['POST'])
@login_required
def withdraw_approval(user_id, solicitation_id):
    logging.info(f'withdraw_and_close_account::({user_id},{solicitation_id})')
    manager = current_user
    user = userDatabase.findById(user_id)
    withdrawConfirm(user_id, user.balance())
    statements = statementDatabase.findByUserId(user.id)
    close_account_approval(user_id, 'aprovar', solicitation_id)
    return render_template('admextrato.html', user=user, extratos=statements, manager = manager), 200

@app.route('/<user_id>/statement', methods = ['GET'])
@login_required
def statement_user(user_id):
    logging.info(f'statement_user::({user_id})')
    manager = current_user
    user = userDatabase.findById(user_id)
    statements = statementDatabase.findByUserId(user.id)
    return render_template('admextrato.html', user = user, extratos=statements, manager = manager), 200

@app.route('/<user_id>/print', methods = ['GET'])
@login_required
def print(user_id):
    manager = current_user
    user = userDatabase.findById(user_id)
    statements = statementDatabase.findByUserId(user_id)
    return render_template('extrato_impressao.html', name=user.name, agencia=user.agency(), conta=user.accountNumber(), saldo=user.balance(), extratos=statements, manager = manager), 200

def withdrawConfirm(user_id, value):
    logging.info(f'withdrawConfirm::({user_id},{value})')
    user = userDatabase.findById(user_id)
    today = time.strftime('%Y-%m-%d %H:%M:%S')
    bank_id = 1
    bankDatabase.withdraw_bank_balance_by_id(bank_id, value)
    user.account.withdraw(value)
    accountDatabase.updateBalanceByAccountNumber(user.balance(), user.accountNumber())
    statement = Statement('D', 'Aprovado', userId=user.id, balance=user.balance(), deposit=0, withdraw=value, date=today)
    statementDatabase.save(statement)

def account_approval(manager, user_id, action, id):
    if action =='aprovar':
        app.logger.info(f'Aprovando a solicitação do usuario {user_id}')
        accountDatabase.create(user_id,manager.workAgency)
        solicitationDatabase.update_status_by_id(id,'Aprovado') 
    else:
        app.logger.info(f'Reprovando a solicitação do usuario {user_id}')
        solicitationDatabase.update_status_by_id(id,'Reprovado')

def deposit_approval(user_id, action, solicitations_id):
    deposit_solicitation= solicitationDatabase.find_deposit_solicitation_by_id_solicitation(solicitations_id)
    account_balance=accountDatabase.getBalanceByAccountNumber(deposit_solicitation.account_number)
    if action =='aprovar':
        app.logger.info(f'Aprovando a solicitação de depósito do usuario {user_id}')
        total_balance= account_balance + deposit_solicitation.deposit_value
        bank_id = 1
        accountDatabase.updateBalanceByAccountNumber(total_balance, deposit_solicitation.account_number)
        bankDatabase.update_bank_balance(bank_id, deposit_solicitation.deposit_value)
        statement = Statement('C', 'Aprovado', userId=user_id, balance=total_balance, deposit=deposit_solicitation.deposit_value, withdraw=0,)
        statementDatabase.save(statement)
        solicitationDatabase.update_status_by_id(solicitations_id,'Aprovado') 
    else:
        statement = Statement('', 'Reprovado', userId=user_id, balance=account_balance, deposit=deposit_solicitation.deposit_value, withdraw=0,)
        statementDatabase.save(statement)
        solicitationDatabase.update_status_by_id(solicitations_id,'Reprovado')
        app.logger.info(f'Reprovando a solicitação de depósito do usuario {user_id}')
        
def update_user_approval(user_id, action, id):
    logging.info(f'User_id: {user_id}, action: {action}, solicitation_id: {id}')
    update_user_solicitation=solicitationDatabase.find_update_user_solicitation_by_id_solicitation(id, user_id)
    if action =='aprovar':
        logging.info(f'Aprovando a solicitação de alteração de dados do usuario {user_id}')   
        userDatabase.update_by_user_solicitation(update_user_solicitation)
        solicitationDatabase.update_status_by_id(id,'Aprovado') 
    else:
        logging.info(f'Reprovando a solicitação de alteração de dados do usuario {user_id}')
        solicitationDatabase.update_status_by_id(id,'Reprovado')

def close_account_approval(user_id, action, id):
    if action == 'aprovar':
        solicitationDatabase.update_status_by_id(id, 'Aprovado')
        open_account_solicitation_id = solicitationDatabase.find_solicitation_id_by_user_id_and_solicitation_type(user_id, 'Abertura de Conta')
        solicitationDatabase.update_status_by_id(open_account_solicitation_id, 'Encerrado')
    else:
        logging.info(f'Reprovando a solicitação de alteração de dados do usuario {user_id}')
        open_account_solicitation_id = solicitationDatabase.find_solicitation_id_by_user_id_and_solicitation_type(user_id, 'Abertura de Conta')
        solicitationDatabase.update_status_by_id(open_account_solicitation_id, 'Aprovado')
        solicitationDatabase.update_status_by_id(id,'Reprovado')
        user = userDatabase.findById(user_id)
        accountDatabase.activate_account(user.accountNumber())

def validate_form(form):
    for key in form:
        if not form[key]:
            return False
    return True

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5001, debug=True)
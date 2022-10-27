from flask import render_template, flash, request
from . import create_manager_app, get_repositories, get_manager_repositories
from flask_login import login_user, current_user, login_required, logout_user
from .statement import Statement

app, login_manager = create_manager_app()

accountDatabase, statementDatabase, solicitationDatabase, bankDatabase, userDatabase = get_repositories()

managerDatabase = get_manager_repositories()

@app.route('/')
@login_required
def index():
    return render_template('admhome.html'), 200

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
    if not validate_form(request.form):
        message = flash('Preencha todos os campos!')
        return render_template('loginGerente.html', message=message), 400
    manager = managerDatabase.findByRegistrationNumberAndPassword (request.form['fmatricula'], request.form['fpassword'])
    if manager:
        app.logger.info(manager)
        login_user(manager)
        return render_template('admhome.html'), 200
    else:
        message = flash(f'Login inválido, verifique os dados de acesso!')
    return render_template('loginGerente.html', message=message), 400

@app.route('/<user_id>/<action>/<id>/<type>/solicitacao')
@login_required
def solicitacao(user_id,action,id,type):
    manager=current_user
    if ((type=='Abertura de conta') or (type=='Encerrar conta')):
        account_approval(user_id, action, id)
    elif type== 'Confirmação de depósito':
        deposit_approval(user_id, action, id)
    solicitations=solicitationDatabase.find_by_work_agency_id(manager.workAgency)
    return render_template('admsolicitations.html', solicitacoes=solicitations), 200

@app.route('/admsolicitations', methods = ['GET'])
@login_required
def solicitations():
    manager= current_user
    solicitations=solicitationDatabase.find_by_work_agency_id(manager.workAgency)
    return render_template('admsolicitations.html', solicitacoes=solicitations), 200

def account_approval(user_id, action, id):
    manager=current_user
    if action =='aprovar':
        app.logger.info(f'Aprovando a solicitação do usuario {user_id}')
        accountDatabase.create(user_id,manager.workAgency) 
        solicitationDatabase.update_status_by_id(id,'Aprovado') 
    else:
        app.logger.info(f'Reprovando a solicitação do usuario {user_id}')
        solicitationDatabase.update_status_by_id(id,'Reprovado')

def deposit_approval(user_id, action, id):
    manager=current_user
    deposit_solicitation= solicitationDatabase.find_deposit_solicitation_by_id_solicitation(id)
    account_balance=accountDatabase.getBalanceByAccountNumber(deposit_solicitation.account_number)
    if action =='aprovar':
        app.logger.info(f'Aprovando a solicitação de depósito do usuario {user_id}')
        total_balance= account_balance + deposit_solicitation.deposit_value
        bank_id = 1
        accountDatabase.updateBalanceByAccountNumber(total_balance, deposit_solicitation.account_number)
        bankDatabase.update_bank_balance(bank_id, deposit_solicitation.deposit_value)
        statement = Statement('C', 'Aprovado', userId=user_id, balance=total_balance, deposit=deposit_solicitation.deposit_value, withdraw=0,)
        statementDatabase.save(statement)
        solicitationDatabase.update_status_by_id(id,'Aprovado') 
    else:
        statement = Statement('', 'Reprovado', userId=user_id, balance=account_balance, deposit=deposit_solicitation.deposit_value, withdraw=0,)
        statementDatabase.save(statement)
        solicitationDatabase.update_status_by_id(id,'Reprovado')
        app.logger.info(f'Reprovando a solicitação de depósito do usuario {user_id}')

def validate_form(form):
    for key in form:
        if not form[key]:
            return False
    return True

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5001, debug=True)
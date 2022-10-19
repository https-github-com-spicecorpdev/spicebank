from flask import request, render_template, session, flash
from flask_login import login_user, current_user, login_required, logout_user
import mariadb
from . import create_app, get_db_connection, get_account_database, get_user_database, get_statement_database, get_manager_database
from .manager import Manager
from .user import User
from .address import Address
from .statement import Statement
import time
import logging

app, login_manager = create_app()
connection = get_db_connection()
userDatabase = get_user_database()
accountDatabase = get_account_database()
statementDatabase = get_statement_database()
managerDatabase = get_manager_database()


@app.route('/')
@login_required
def index():
    user = current_user
    logging.info (user)
    if hasattr(user,'profile'):
        return render_template('homeGerente.html'), 200
    else:
        return render_template('home.html', name=user.name, agencia=user.agency(), conta=user.accountNumber(), saldo=user.balance()), 200

@login_manager.unauthorized_handler
def unauthorized():
    return render_template('login.html')

@login_manager.user_loader
def load_user(user_id):
    return userDatabase.findById(user_id)
    

@app.route('/login', methods = ['POST'])
def login():
    if not validate_form(request.form):
            message = flash('Preencha todos os campos!')
            return render_template('login.html', message=message), 400
    user = userDatabase.findByAgencyAccountAndPassword(request.form['fagency'],request.form['faccount'], request.form['fpassword'])
    if user:
        login_user(user)
        return render_template('home.html', name=user.name, agencia=user.agency(), conta=user.accountNumber(), saldo=user.balance()), 200
    else:
        message = flash(f'Login inválido, verifique os dados de acesso!')
    return render_template('login.html', message=message), 400

@app.route('/logout')
def logout():
    logout_user()
    return render_template('login.html'), 200

@app.route('/logoutmanager')
def logoutmanager():
    session['autenticado']=False
    session.clear()
    return render_template('loginGerente.html'), 200

@app.route('/acompanhamentoform')
def acompanhamentoform():
    return render_template('acompanhamento.html'), 200

@app.route('/loginAcomp', methods = ['POST'])
def loginAcomp():
    if not validate_form(request.form):
        message = flash('Preencha todos os campos!')
        return render_template('acompanhamento.html', message=message), 400
    solicitation = userDatabase.findSolicitationByCpfAndPassword(request.form['fcpf'], request.form['fpassword'])
    if solicitation:
        if solicitation.status == "aprovado":
            message = flash(f'Agência: {solicitation.agency} / Conta: {solicitation.account}')
            message = flash('Guarde sua agência e conta!')
            return render_template('homeAcomp.html', name=solicitation.name, solicitacao=solicitation.status, message=message), 200
        else:
            message = flash('Aguardando análise de solicitação.')
            return render_template('homeAcomp.html', name=solicitation.name, solicitacao=solicitation.status, message=message), 200
    else:
        message = flash(f'Login inválido, verifique os dados de acesso!')
    return render_template('acompanhamento.html', message=message), 400

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
        logging.info(manager)
        login_user(manager)
        return render_template('homeGerente.html'), 200
    else:
        message = flash(f'Login inválido, verifique os dados de acesso!')
    return render_template('loginGerente.html', message=message), 400

@app.route('/registerManager' , methods = ['GET'])
def registerFormManager():
    return render_template('cadastrogerente.html'), 200

@app.route('/registerManager', methods = ['POST'])
def registerManager():
        cursor = connection.cursor()
        if not validate_form(request.form):
            message = flash('Preencha todos os campos!')
            return render_template('cadastrogerente.html', message=message), 400
        else:
            if not userExists(request.form['fcpf']):
                try:
                    query = "INSERT INTO tuser (nameUser, cpfUser, roadUser, numberHouseUser, districtUser, cepUser, cityUser, stateUser, birthdateUser, genreUser, passwordUser, profileUser) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 2);"
                    parameters = (request.form['fname'], request.form['fcpf'], request.form['froad'], request.form['fnumberHouse'], request.form['fdistrict'], request.form['fcep'], request.form['fcity'], request.form['fstate'], request.form['fbirthdate'], request.form['fgenre'], request.form['fpassword'],)
                    print(parameters)
                    cursor.execute(query, parameters)
                    connection.commit()
                    query = "INSERT INTO tagency (accountAgency, idManager) values (next value for agency_manager, LAST_INSERT_ID());"
                    # query = "INSERT INTO tagency (accountAgeny) values (next value for agency_manager);"
                    cursor.execute(query)
                    connection.commit()
                    print(cursor.execute(query))
                    return render_template('loginGerente.html'), 201
                except mariadb.Error as e:
                    print(e)
                    return "Erro ao cadastrar usuário", 400
            else:
                requestCpf = request.form['fcpf']
                message = flash(f'CPF {requestCpf} com cadastra já existente!')
        return render_template('cadastrogerente.html', message=message), 400

@app.route('/registerform')
def registerForm():
    return render_template('cadastro.html'), 200

@app.route('/register', methods = ['POST'])
def register():
    if not validate_form(request.form):
        message = flash('Preencha todos os campos!')
        return render_template('cadastro.html', message=message), 400
    if userExists(request.form['fcpf']):
        requestCpf = request.form['fcpf']
        message = flash(f'CPF {requestCpf} com cadastro já existente!')
        return render_template('cadastro.html', message=message), 400
    else:
        address = Address(request.form['froad'], request.form['fnumberHouse'], request.form['fdistrict'], request.form['fcity'], request.form['fstate'], request.form['fcep'])
        user = User(None, request.form['fname'], request.form['fcpf'], request.form['fpassword'], request.form['fbirthdate'], request.form['fgenre'], address=address)
        userId = userDatabase.save(user)
        accountDatabase.create(userId)
        return render_template('login.html'), 201

@app.route('/aprovar')
def aprovar():
        # cursor = connection.cursor()
        # query = "SELECT * from taccount"
        # cursor.execute(query)
        # user = cursor.fetchone()
        # print(user)
        # session['idAccount']=user[0]
        cursor = connection.cursor()
        query = "UPDATE taccount SET agencyUser = ?, statusAccount = 1, solicitacao = 'aprovado' WHERE idAccount = ?"
        parameters = (session.get("accountAgency"))
        parameters2 = (session['idAccount'])
        numeroDConta = (parameters, parameters2,)
        print(numeroDConta)
        cursor.execute(query, numeroDConta)
        connection.commit()
        if user[3] == 2:
            cursor = connection.cursor()
            query = "SELECT U.idUser AS idUser, U.nameUser AS nameUser, U.cpfUser AS cpfUser, A.idAccount AS idAccount, A.idAccountUser AS idAccountUser, A.solicitacao AS solicitacao, A.numberAccount AS numberAccount FROM tuser AS U INNER JOIN taccount AS A ON idUser = idAccountUser WHERE solicitacao = 'pendente'"
            cursor.execute(query)
            rows = cursor.fetchall()
            print(rows)
            if cursor.rowcount > 0:
                print(cursor.rowcount)
                for user in rows:
                    print(user)
                while user[0] > 0:    
                    session['nameUser']=user[1]
                    session['cpfUser']=user[2]
                    session['idAccount']=user[3]
                    session['solicitacao']=user[5]
                    session['numberAccount']=user[6]
                    message = flash(f'Este usuário foi para a sua agência')
                    return render_template('homeGerente.html', nameManager=session['nameManager'], name=session['nameUser'], agenciadoGer=session['accountAgency'], solicitacao=session['solicitacao'], userDetails = rows, numeroConta=session['numberAccount'], message=(message)), 200
            else:
                return render_template('homeGerente.html', nameManager=session['nameManager'], name=session['nameUser'], agenciadoGer=session['accountAgency'], solicitacao=session['solicitacao'], numeroConta=session['numberAccount'], message=(message)), 200
        else:
            return render_template('homeGerente.html', nameManager=session['nameManager'], name=session['nameUser'], agenciadoGer=session['accountAgency'], solicitacao=session['solicitacao'], numeroConta=session['numberAccount'], message=(message)), 200

#Abertura de conta


#Abertura de conta bancária
# INSERT INTO taccount (numberAccount, totalbalance, idAccountUser) values ('12', '0', LAST_INSERT_ID());

@app.route('/withdrawform')
@login_required
def withdrawform():
    user = current_user
    saldo = user.balance()
    saldoFormatado=(f'{saldo:.2f}')
    return render_template('saque.html', agencia=user.agency(), conta=user.accountNumber(), saldo=saldoFormatado), 200

@app.route('/withdraw', methods = ['POST'])
@login_required
def withdraw():
    user = current_user
    today = time.strftime('%Y-%m-%d %H:%M:%S')
    saldo = user.balance()
    saldoFormatado=(f'{saldo:.2f}')
    if not validate_form(request.form):
        message = flash('Preencha um valor para sacar!')
        return render_template('saque.html', agencia=user.agency(), conta=user.accountNumber(), saldo=saldoFormatado, message=message), 400
    else:
        value = float(request.form['fvalor'])
        if value <= 0:
            message = flash('Valor de saque deve ser maior que R$00,00!')
            return render_template('saque.html', agencia=user.agency(), conta=user.accountNumber(), saldo=saldoFormatado, message=message), 400
        try:
            cursor = connection.cursor()
            query = "SELECT capital FROM bank WHERE BINARY id = ?"
            parameters = (1,)
            cursor.execute(query, parameters)
            bankBalance = float(cursor.fetchone()[0])
            if bankBalance >= value:
                return render_template('saque_confirmacao.html', name=user.name, agencia=user.agency(), conta=user.accountNumber(), valor=value, data=today), 200
            else:
                message = flash('Valor maior que o saldo disponível!')
                return render_template('saque.html', agencia=user.agency(), conta=user.accountNumber(), saldo=saldoFormatado, message=message), 400
        except mariadb.Error as e:
            logging.error(e)
            message=flash('Erro ao sacar valor desejado!')
            return render_template('saque_confirmacao.html', name=user.name, agencia=user.agency(), conta=user.accountNumber(), valor=value, data=today, message=message), 400

@app.route('/withdrawconfirm', methods = ['POST'])
def withdrawConfirm():
    value = float(request.form['fvalor'])
    today = time.strftime('%Y-%m-%d %H:%M:%S')
    try:
        cursor = connection.cursor()
        query = "SELECT capital FROM bank WHERE BINARY id = ?"
        parameters = (1,)
        cursor.execute(query, parameters)
        bankBalance = float(cursor.fetchone()[0])
        newBalance = bankBalance - value
        query = "UPDATE bank SET capital = ? WHERE id = ?"
        parameters = (newBalance, 1,)
        cursor.execute(query, parameters)
        current_user.account.withdraw(value)
        accountDatabase.updateBalanceByAccountNumber(current_user.balance(), current_user.accountNumber())
        statement = Statement('D', userId=current_user.id, balance=current_user.balance(), deposit=0, withdraw=value, date=today)
        statementDatabase.save(statement)
        return render_template('comprovante_saque.html', name=current_user.name, agencia=current_user.agency(), conta=current_user.accountNumber(), valor=value, data=today), 200
    except mariadb.Error as e:
        logging.error(e)
        message = flash('Falha ao depositar')
        return render_template('comprovante_saque.html', name=current_user.name, agencia=current_user.agency(), conta=current_user.accountNumber(), valor=value, data=today, message=message), 400

@app.route('/depositform')
@login_required
def depositform():
    user = current_user
    saldo = user.balance()
    saldoFormatado=(f'{saldo:.2f}')
    return render_template('deposito.html', name=user.name, agencia=user.agency(), conta=user.accountNumber(), saldo=saldoFormatado), 200

@app.route('/deposit', methods = ['POST'])
@login_required
def deposit():
    user = current_user
    saldo = user.balance()
    saldoFormatado=(f'{saldo:.2f}')
    if not validate_form(request.form):
        message = flash('Preencha um valor para depositar!')
        return render_template('deposito.html', name=user.name, agencia=user.agency(), conta=user.accountNumber(), saldo=saldoFormatado, message=message), 400
    valor = float(request.form['fvalor'])
    if valor <= 0:
        message = flash('Valor de depósito deve ser maior que R$00,00!')
        return render_template('deposito.html', name=user.name, agencia=user.agency(), conta=user.accountNumber(), saldo=saldoFormatado, message=message), 400
    if valor >= 0:
        value = (f'{valor:.2f}')
        return render_template('deposito_confirmacao.html', name=user.name, agencia=user.agency(), conta=user.accountNumber(), valor=value), 200


@app.route('/depositconfirm', methods = ['POST'])
@login_required
def depositconfirm():
    valor = float(request.form['fvalor'])
    today = time.strftime('%Y-%m-%d %H:%M:%S')
    try:
        bank_id = 1
        update_bank_balance(bank_id, valor)
        update_user_balance(valor)
        statement = Statement('C', userId=current_user.id, balance=current_user.balance(), deposit=valor, withdraw=0, date=today)
        statementDatabase.save(statement)
        depositedValue=(f'{valor:.2f}')
        return render_template('comprovante_deposito.html', name=current_user.name, agencia=current_user.agency(), conta=current_user.accountNumber(), valor=depositedValue, data=today), 200
    except mariadb.Error as e:
        logging.error(e)
        saldo = current_user.balance()
        saldoFormatado=(f'{saldo:.2f}')
        message = flash('Falha ao depositar')
        return render_template('deposito_confirmacao.html', name=current_user.name, agencia=current_user.agency(), conta=current_user.accountNumber(), saldo=saldoFormatado, message=message), 400

@app.route('/statementform', methods = ['GET'])
@login_required
def statementForm():
    user = current_user
    saldo = user.balance()
    statements = statementDatabase.findByUserId(user.id)
    return render_template('extrato.html', name=user.name, agencia=user.agency(), conta=user.accountNumber(), saldo=saldo, extratos=statements), 200

@app.route('/print', methods = ['GET'])
@login_required
def print():
    user = current_user
    statements = statementDatabase.findByUserId(user.id)
    return render_template('extrato_impressao.html', name=user.name, agencia=user.agency(), conta=user.accountNumber(), saldo=user.balance(), extratos=statements), 200

def userExists(cpf):
    return userDatabase.findByCpf(cpf)

def validate_form(form):
    for key in form:
        if not form[key]:
            return False
    return True

def update_bank_balance(bank_id, value):
    cursor = connection.cursor()
    query = "SELECT capital FROM bank WHERE id = ?"
    parameters = (bank_id,)
    cursor.execute(query, parameters)
    bankBalance = float(cursor.fetchone()[0])
    newBankBalance = bankBalance + value
    query = "UPDATE bank SET capital = ? WHERE id = ?"
    parameters = (newBankBalance, bank_id,)
    cursor.execute(query, parameters)
    connection.commit()

def update_user_balance(value):
    current_user.account.deposit(value)
    accountDatabase.updateBalanceByAccountNumber(current_user.balance(), current_user.accountNumber())
    
if __name__ == "__main__":

    app.run(debug=True)
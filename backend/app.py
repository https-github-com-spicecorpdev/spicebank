from flask import request, render_template, session, flash
from flask_login import login_user, current_user, login_required, logout_user
import mariadb
from . import create_app
from .user import User
import time
import logging

app, connection, login_manager = create_app()

@app.route('/')
@login_required
def index():
    user = current_user
    saldo = user.balance
    saldoFormatado=(f'{saldo:.2f}')
    return render_template('home.html', name=user.name, agencia=user.agency, conta=user.account, saldo=saldoFormatado), 200

@login_manager.unauthorized_handler
def unauthorized():
    return render_template('login.html')

@login_manager.user_loader
def load_user(user_id):
    cursor = connection.cursor(dictionary=True)
    query = """
    SELECT USR.*, ACCOUNT.* 
    FROM tuser AS USR INNER JOIN taccount AS ACCOUNT ON USR.idUser = ACCOUNT.idAccountUser
	WHERE ACCOUNT.agencyUser = ?
	AND ACCOUNT.numberAccount = ?
	AND USR.passwordUser = ?
    """
    parameters = (request.form['fagency'], request.form['faccount'], request.form['fpassword'], )
    cursor.execute(query, parameters) 
    userFromDB = cursor.fetchone()
    return User(userFromDB['idUser'], userFromDB['nameUser'], userFromDB['cpfUser'], request.form['fpassword'], userFromDB['birthdateUser'], userFromDB['genreUser'], request.form['faccount'], userFromDB['agencyUser'], userFromDB['totalbalance'], userFromDB['profileUser'])
    

@app.route('/login', methods = ['POST'])
def login():
    if not validate_form(request.form):
            message = flash('Preencha todos os campos!')
            return render_template('login.html', message=message), 400
    cursor = connection.cursor(dictionary=True)
    query = """
    SELECT USR.*, ACCOUNT.* 
    FROM tuser AS USR INNER JOIN taccount AS ACCOUNT ON USR.idUser = ACCOUNT.idAccountUser
	WHERE ACCOUNT.agencyUser = ?
	AND ACCOUNT.numberAccount = ?
	AND USR.passwordUser = ?
    """
    parameters = (request.form['fagency'], request.form['faccount'], request.form['fpassword'], )
    cursor.execute(query, parameters) 
    userFromDB = cursor.fetchone()
    if userFromDB and not (userFromDB['idUser'] == ''):
        user = User(userFromDB['idUser'], userFromDB['nameUser'], userFromDB['cpfUser'], request.form['fpassword'], userFromDB['birthdateUser'], userFromDB['genreUser'], request.form['faccount'], userFromDB['agencyUser'], userFromDB['totalbalance'], userFromDB['profileUser'])
        login_user(user)
        saldo = user.balance
        saldoFormatado=(f'{saldo:.2f}')
        return render_template('home.html', name=user.name, agencia=user.agency, conta=user.account, saldo=saldoFormatado), 200
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
    cursor = connection.cursor(dictionary=True)
    query = "SELECT USR.*, ACCOUNT.* FROM tuser AS USR INNER JOIN taccount AS ACCOUNT ON idUser = idAccountUser WHERE cpfUser = ? AND passwordUser = ? "
    parameters = (request.form['fcpf'], request.form['fpassword'], )
    cursor.execute(query, parameters)
    user = cursor.fetchone()
    if user and not (user['idUser'] == ''):
        if user['solicitacao'] == "aprovado":
            message = flash(f'Agência: {user["agencyUser"]} / Conta: {user["numberAccount"]}')
            message = flash('Guarde sua agência e conta!')
            return render_template('homeAcomp.html', name=user['nameUser'], agencia=user["agencyUser"], conta=user["numberAccount"], solicitacao=user['solicitacao'], message=(message)), 200
        else:
            message = flash('Aguardando análise de solicitação.')
            return render_template('homeAcomp.html', name=user['nameUser'],cpf=user['cpfUser'], solicitacao=user['solicitacao']), 200
    else:
        message = flash(f'Login inválido, verifique os dados de acesso!')
    return render_template('acompanhamento.html', message=message), 400

@app.route('/admForm')
@login_required
def admForm():
    return render_template('homeGerente.html'), 200

@app.route('/loginGerente', methods = ['POST'])
def loginGerente():
    if not validate_form(request.form):
        message = flash('Preencha todos os campos!')
        return render_template('loginGerente.html', message=message), 400
    cursor = connection.cursor()
    query = "SELECT U.idUser AS idUser, U.nameUser AS nameUser, U.cpfUser AS cpfUser, U.profileUser AS profileUser, U.passwordUser AS passwordUser, Ag.idAgency AS idAgency, Ag.accountAgency AS accountAgency, Ag.idManager AS idManager FROM tuser AS U INNER JOIN tagency AS Ag ON idUser = idManager WHERE cpfUser = ? AND profileUser != 3 AND passwordUser = ? "
    parameters = (request.form['fcpf'], request.form['fpassword'], )
    print(parameters)
    cursor.execute(query, parameters)
    user = cursor.fetchone()
    print(user)
    if user and not (user[0] == ''):
        session['autenticado'] = True
        session['nameManager']=user[1]
        session['cpfUser']=user[2]
        session['profileUser']=user[3]
        session['accountAgency']=user[6]
        message = flash(f'Olá, {user[1]}!')
        message = flash(f'Bem-vindo gerente da agência: {user[6]}')
        message = flash(f'Estas são as contas de usuários que aguardam confirmação!')
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
                return render_template('homeGerente.html', nameManager=session['nameManager'], agenciadoGer=session['accountAgency'], solicitacao=session['solicitacao'], numeroConta=session['numberAccount'], message=(message)), 200
        else:
            message = flash('Bem-Vindo Gerente Geral!')
            return render_template('homeGerente.html', name=session['nameUser'],cpf=session['cpfUser'], nameManager=session['nameManager'], agenciadoGer=session['accountAgency'], solicitacao=session['solicitacao'], numeroConta=session['numberAccount'], message=(message)), 200
    else:
        session['autenticado']=False
        message = flash(f'Login inválido, verifique os dados de acesso!')
    return render_template('loginGerente.html', message=message), 400

@app.route('/registerFormManager')
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
        cursor = connection.cursor()
        if not validate_form(request.form):
            message = flash('Preencha todos os campos!')
            return render_template('cadastro.html', message=message), 400
        else:
            if not userExists(request.form['fcpf']):
                try:
                    query = "INSERT INTO tuser (nameUser, cpfUser, roadUser, numberHouseUser, districtUser, cepUser, cityUser, stateUser, birthdateUser, genreUser, passwordUser) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"
                    parameters = (request.form['fname'], request.form['fcpf'], request.form['froad'], request.form['fnumberHouse'], request.form['fdistrict'], request.form['fcep'], request.form['fcity'], request.form['fstate'], request.form['fbirthdate'], request.form['fgenre'], request.form['fpassword'],)
                    print(parameters)
                    cursor.execute(query, parameters)
                    connection.commit()
                    query = "INSERT INTO taccount (numberAccount, totalbalance, idAccountUser, statusAccount, solicitacao) values (next value for account_number, 0, LAST_INSERT_ID(), 0, 'pendente');"
                    cursor.execute(query)
                    connection.commit()
                    print(cursor.execute(query))
                    return render_template('login.html'), 201
                except mariadb.Error as e:
                    print(e)
                    return "Erro ao cadastrar usuário", 400
            else:
                requestCpf = request.form['fcpf']
                message = flash(f'CPF {requestCpf} com cadastra já existente!')
        return render_template('cadastro.html', message=message), 400

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
    saldo = user.balance
    saldoFormatado=(f'{saldo:.2f}')
    return render_template('saque.html', agencia=user.agency, conta=user.account, saldo=saldoFormatado), 200

@app.route('/withdraw', methods = ['POST'])
@login_required
def withdraw():
    user = current_user
    today = time.strftime('%Y-%m-%d %H:%M:%S')
    saldo = user.balance
    saldoFormatado=(f'{saldo:.2f}')
    if not validate_form(request.form):
        message = flash('Preencha um valor para sacar!')
        return render_template('saque.html', agencia=user.agency, conta=user.account, saldo=saldoFormatado, message=message), 400
    else:
        value = float(request.form['fvalor'])
        if value <= 0:
            message = flash('Valor de saque deve ser maior que R$00,00!')
            return render_template('saque.html', agencia=user.agency, conta=user.account, saldo=saldoFormatado, message=message), 400
        try:
            cursor = connection.cursor()
            query = "SELECT capital FROM tbank WHERE BINARY id = ?"
            parameters = (1,)
            cursor.execute(query, parameters)
            bankBalance = float(cursor.fetchone()[0])
            if bankBalance >= value:
                return render_template('saque_confirmacao.html', name=user.name, agencia=user.agency, conta=user.account, valor=value, data=today), 200
            else:
                message = flash('Valor maior que o saldo disponível!')
                return render_template('saque.html', agencia=user.agency, conta=user.account, saldo=saldoFormatado, message=message), 400
        except mariadb.Error as e:
            logging.error(e)
            message=flash('Erro ao sacar valor desejado!')
            return render_template('saque_confirmacao.html', name=user.name, agencia=user.agency, conta=user.account, valor=value, data=today, message=message), 400

@app.route('/withdrawconfirm', methods = ['POST'])
def withdrawConfirm():
    value = float(request.form['fvalor'])
    today = time.strftime('%Y-%m-%d %H:%M:%S')
    try:
        cursor = connection.cursor()
        query = "SELECT capital FROM tbank WHERE BINARY id = ?"
        parameters = (1,)
        cursor.execute(query, parameters)
        bankBalance = float(cursor.fetchone()[0])
        newBalance = bankBalance - value
        query = "UPDATE tbank SET capital = ? WHERE id = ?"
        parameters = (newBalance, 1,)
        cursor.execute(query, parameters)
        current_user.withdraw(value)
        query = "UPDATE taccount SET totalbalance = ? WHERE numberAccount = ?"
        parameters = (current_user.balance, current_user.account)
        cursor.execute(query, parameters)
        query = "INSERT INTO bank_statement (id_user, balance, deposit, withdraw, date) values (?, ?, ?, ?, ?)"
        parameters = (current_user.id, current_user.balance, 0, value, today)
        logging.info(parameters)
        cursor.execute(query, parameters)
        connection.commit()
        return render_template('comprovante_saque.html', name=current_user.name, agencia=current_user.agency, conta=current_user.account, valor=value, data=today), 200
    except mariadb.Error as e:
        logging.error(e)
        message = flash('Falha ao depositar')
        return render_template('comprovante_saque.html', name=current_user.name, agencia=current_user.agency, conta=current_user.account, valor=value, data=today, message=message), 400

@app.route('/depositform')
@login_required
def depositform():
    user = current_user
    saldo = user.balance
    saldoFormatado=(f'{saldo:.2f}')
    return render_template('deposito.html', name=user.name, agencia=user.agency, conta=user.account, saldo=saldoFormatado), 200

@app.route('/deposit', methods = ['POST'])
@login_required
def deposit():
    user = current_user
    saldo = user.balance
    saldoFormatado=(f'{saldo:.2f}')
    if not validate_form(request.form):
        message = flash('Preencha um valor para depositar!')
        return render_template('deposito.html', name=user.name, agencia=user.agency, conta=user.account, saldo=saldoFormatado, message=message), 400
    valor = float(request.form['fvalor'])
    if valor <= 0:
        message = flash('Valor de depósito deve ser maior que R$00,00!')
        return render_template('deposito.html', name=user.name, agencia=user.agency, conta=user.account, saldo=saldoFormatado, message=message), 400
    if valor >= 0:
        value = (f'{valor:.2f}')
        return render_template('deposito_confirmacao.html', name=user.name, agencia=user.agency, conta=user.account, valor=value), 200


@app.route('/depositconfirm', methods = ['POST'])
@login_required
def depositconfirm():
    valor = float(request.form['fvalor'])
    today = time.strftime('%Y-%m-%d %H:%M:%S')
    try:
        bank_id = 1
        update_bank_balance(bank_id, valor)
        update_user_balance(valor)
        cursor = connection.cursor()
        query = "INSERT INTO bank_statement (id_user, balance, deposit, withdraw, date) values (?, ?, ?, ?, ?)"
        parameters = (current_user.id, current_user.balance, valor, 0, today)
        logging.info(parameters)
        cursor.execute(query, parameters)
        connection.commit()
        depositedValue=(f'{valor:.2f}')
        return render_template('comprovante_deposito.html', name=current_user.name, agencia=current_user.agency, conta=current_user.account, valor=depositedValue, data=today), 200
    except mariadb.Error as e:
        logging.error(e)
        saldo = current_user.balance
        saldoFormatado=(f'{saldo:.2f}')
        message = flash('Falha ao depositar')
        return render_template('deposito_confirmacao.html', name=current_user.name, agencia=current_user.agency, conta=current_user.account, saldo=saldoFormatado, message=message), 400    

def userExists(cpf):
    cursor = connection.cursor()
    query = "SELECT nameUser FROM tuser WHERE BINARY cpfUser = ?"
    parameters = (cpf, )
    cursor.execute(query, parameters)
    user = cursor.fetchone()
    return user

def validate_form(form):
    for key in form:
        if not form[key]:
            return False
    return True

def update_bank_balance(bank_id, value):
    cursor = connection.cursor()
    query = "SELECT capital FROM tbank WHERE id = ?"
    parameters = (bank_id,)
    cursor.execute(query, parameters)
    bankBalance = float(cursor.fetchone()[0])
    newBankBalance = bankBalance + value
    query = "UPDATE tbank SET capital = ? WHERE id = ?"
    parameters = (newBankBalance, bank_id,)
    cursor.execute(query, parameters)
    connection.commit()

def update_user_balance(value):
    cursor = connection.cursor()
    current_user.deposit(value)
    query = "UPDATE taccount SET totalbalance = ? WHERE numberAccount = ?"
    parameters = (current_user.balance, current_user.account,)
    cursor.execute(query, parameters)
    connection.commit()

if __name__ == "__main__":

    app.run(debug=True)
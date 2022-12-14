from flask import request, render_template, flash
from flask_login import login_user, current_user, login_required, logout_user
import mariadb
from . import create_app, get_connection, get_repositories
from .user import User
from .address import Address
from .statement import Statement
from .solicitation import CloseAccountSolicitation, UpdateDataSolicitation
import time
import logging

app, login_manager = create_app()
connection= get_connection()
accountDatabase, statementDatabase, solicitationDatabase, bankDatabase, userDatabase, agencyDatabase = get_repositories()

@app.context_processor
def current_time():
    return {'date': time.strftime('%d/%m/%Y %H:%M:%S')}

@app.route('/')
@login_required
def index():
    user = current_user
    logging.info(f'{user}')
    today = time.strftime('%d/%m/%Y %H:%M:%S')
    return render_template('home.html', name=user.name, agencia=user.agency(), conta=user.accountNumber(), saldo=user.balance(), date=today, type=user.account.typeAccount), 200

@login_manager.unauthorized_handler
def unauthorized():
    return render_template('login.html')

@login_manager.user_loader
def load_user(user_id):
    user = userDatabase.find_by_account_id(user_id)
    logging.info(f'Utilizando com conta {user.account.account}')
    return user

@app.route('/login', methods = ['POST'])
def login():
    today = time.strftime('%d/%m/%Y %H:%M:%S')
    if not validate_form(request.form):
            message = flash('Preencha todos os campos!')
            return render_template('login.html', message=message), 400
    user = userDatabase.findByAgencyAccountAndPassword(request.form['fagency'],request.form['faccount'], request.form['fpassword'])
    if user:
        logging.info(f'Logando com a conta {user.account.account}')
        login_user(user)
        logging.info(f'{user}')
        return render_template('home.html', name=user.name, agencia=user.agency(), conta=user.accountNumber(), saldo=user.balance(), date=today, type=user.account.typeAccount), 200
    else:
        message = flash(f'Login inválido, verifique os dados de acesso!')
    return render_template('login.html', message=message), 400

@app.route('/logout')
def logout():
    logout_user()
    return render_template('login.html'), 200

@app.route('/acompanhamentoform')
def acompanhamentoform():
    return render_template('acompanhamento.html'), 200

@app.route('/loginAcomp', methods = ['POST'])
def loginAcomp():
    if not validate_form(request.form):
        message = flash('Preencha todos os campos!')
        return render_template('acompanhamento.html', message=message), 400
    requestCpf = request.form['fcpf']
    eliminar = ".-"
    for i in range(0,len(eliminar)):
        requestCpf = requestCpf.replace(eliminar[i],"")
    accounts = userDatabase.find_all_accounts_by_cpf_and_password(requestCpf, request.form['fpassword'])
    if accounts:
        return render_template('homeAcomp.html', accounts=accounts, statements=None), 200
    else:
        message = flash(f'Login inválido, verifique os dados de acesso!')
    return render_template('acompanhamento.html', message=message), 400

@app.route('/registerform')
def registerForm():
    return render_template('cadastro.html'), 200

@app.route('/register', methods = ['POST'])
def register():
    if not validate_form(request.form):
        message = flash('Preencha todos os campos!')
        return render_template('cadastro.html', message=message), 400
    requestCpf = request.form['fcpf']
    eliminar = ".-"
    for i in range(0,len(eliminar)):
        requestCpf = requestCpf.replace(eliminar[i],"")
    logging.info(f"{requestCpf}")
    if userExists(requestCpf):
        message = flash(f'CPF {requestCpf} com cadastro já existente!')
        return render_template('cadastro.html', message=message), 400
    else:
        agency_id = agencyDatabase.find_next_agency_id_by_amount_users()
        requestCEP = request.form['fcep']
        eliminarCEP = "-"
        for i in range(0,len(eliminarCEP)):
            requestCEP = requestCEP.replace(eliminarCEP[i],"")
        if agency_id:

            account_type = request.form['faccount_type']
            address = Address(request.form['froad'], request.form['fnumberHouse'], request.form['fdistrict'], request.form['fcity'], request.form['fstate'], requestCEP)
            user = User(None, request.form['fname'], requestCpf, request.form['fpassword'], request.form['fbirthdate'], request.form['fgenre'], address=address)

            user_id = userDatabase.save(user)
            create_account(user_id, agency_id, account_type)
            return render_template('login.html'), 201
        flash('Nenhuma agência disponível')
        return render_template('cadastro.html'), 200

def create_account(user_id, agency_id, account_type):
    account_id = accountDatabase.create(user_id, agency_id, account_type)
    if account_type=='CP':
        solicitationDatabase.open_account_solicitation(user_id, account_id, 'Abertura de conta', 'Conta Poupança')
    else:
        solicitationDatabase.open_account_solicitation(user_id, account_id, 'Abertura de conta', 'Conta Corrente')


@app.route('/new_account', methods = ['GET','POST'])
def new_account():
    user=current_user
    if request.method == "POST":
        if user.account.typeAccount=='CC':
            create_account(user.id, user.account.agency, 'CP')
            return render_template('newaccountconfirm.html',user=user), 200
        else:
            create_account(user.id, user.account.agency, 'CC')
            return render_template('newaccountconfirm.html',user=user), 200
    return render_template('newaccount.html',user=user), 200

@app.route('/withdrawform')
@login_required
def withdrawform():
    user = current_user
    saldo = user.balance()
    saldoFormatado=(f'{saldo:.2f}')
    today = time.strftime('%d/%m/%Y %H:%M:%S')
    return render_template('saque.html', agencia=user.agency(), conta=user.accountNumber(), saldo=saldoFormatado, date=today, type=user.account.typeAccount), 200

@app.route('/withdraw', methods = ['POST'])
@login_required
def withdraw():
    user = current_user
    today = time.strftime('%d/%m/%Y %H:%M:%S')
    saldo = user.balance()
    saldoFormatado=(f'{saldo:.2f}')
    if not validate_form(request.form):
        message = flash('Preencha um valor para sacar!')
        return render_template('saque.html', agencia=user.agency(), conta=user.accountNumber(), saldo=saldoFormatado, message=message, date=today, type=user.account.typeAccount), 400
    else:
        valorStr = request.form['fvalor']
        valorStr = valorStr.replace("," , ".")
        value = float(valorStr)
        valor_format = (f'{value:.2f}')
        accountType = accountDatabase.getAccountTypeByAccountNumber(user.accountNumber())
        if value <= 0:
            message = flash('Valor de saque deve ser maior que R$00,00!')
            return render_template('saque.html', agencia=user.agency(), conta=user.accountNumber(), saldo=saldoFormatado, message=message, date=today, type=user.account.typeAccount), 400
        elif ((value > saldo) and (accountType == 'CP')):
            message = flash('Valor inserido maior que o saldo da conta')
            return render_template('saque.html', agencia=user.agency(), conta=user.accountNumber(), saldo=saldoFormatado, message=message, date=today, type=user.account.typeAccount), 400
        try:
            cursor = connection.cursor()
            query = "SELECT capital FROM bank WHERE BINARY id = ?"
            parameters = (1,)
            cursor.execute(query, parameters)
            bankBalance = float(cursor.fetchone()[0])
            if (bankBalance >= value):
                return render_template('saque_confirmacao.html', name=user.name, agencia=user.agency(), conta=user.accountNumber(), valor=valor_format, date=today, type=user.account.typeAccount), 200
            else:
                message = flash('Valor maior que o saldo do banco disponível!')
                return render_template('saque.html', agencia=user.agency(), conta=user.accountNumber(), saldo=saldoFormatado, message=message, date=today, type=user.account.typeAccount), 400
        except mariadb.Error as e:
            logging.error(e)
            message=flash('Erro ao sacar valor desejado!')
            return render_template('saque_confirmacao.html', name=user.name, agencia=user.agency(), conta=user.accountNumber(), valor=valor_format, date=today, type=user.account.typeAccount, message=message), 400

@app.route('/withdrawconfirm', methods = ['POST'])
def withdrawConfirm():
    value = float(request.form['fvalor'])
    valor_format = (f'{value:.2f}')
    today = time.strftime('%d/%m/%Y %H:%M:%S')
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
        statement = Statement('D', 'Aprovado', accountId=current_user.account.id, balance=current_user.balance(), deposit=0, withdraw=value, date=today)
        statementDatabase.save(statement)
        return render_template('comprovante_saque.html', name=current_user.name, agencia=current_user.agency(), conta=current_user.accountNumber(), valor=valor_format, date=today, type=current_user.account.typeAccount), 200
    except mariadb.Error as e:
        logging.error(e)
        message = flash('Falha ao depositar')
        return render_template('comprovante_saque.html', name=current_user.name, agencia=current_user.agency(), conta=current_user.accountNumber(), valor=valor_format, date=today, type=current_user.account.typeAccount,  message=message), 400

@app.route('/depositform')
@login_required
def depositform():
    user = current_user
    saldo = user.balance()
    saldoFormatado=(f'{saldo:.2f}')
    today = time.strftime('%d/%m/%Y %H:%M:%S')
    return render_template('deposito.html', name=user.name, agencia=user.agency(), conta=user.accountNumber(), saldo=saldoFormatado, date=today, type=user.account.typeAccount), 200

@app.route('/deposit', methods = ['POST'])
@login_required
def deposit():
    user = current_user
    saldo = user.balance()
    saldoFormatado=(f'{saldo:.2f}')
    today = time.strftime('%d/%m/%Y %H:%M:%S')
    if not validate_form(request.form):
        message = flash('Preencha um valor para depositar!')
        return render_template('deposito.html', name=user.name, agencia=user.agency(), conta=user.accountNumber(), saldo=saldoFormatado, message=message, date=today, type=user.account.typeAccount), 400
    valorStr = request.form['fvalor']
    valorStr = valorStr.replace("," , ".")
    valor = float(valorStr)
    if valor <= 0.0:
        message = flash('Valor de depósito deve ser maior que R$00,00!')
        return render_template('deposito.html', name=user.name, agencia=user.agency(), conta=user.accountNumber(), saldo=saldoFormatado, message=message, date=today, type=user.account.typeAccount), 400
    if valor >= 0.0:
        value = (f'{valor:.2f}')
        return render_template('deposito_confirmacao.html', name=user.name, agencia=user.agency(), conta=user.accountNumber(), valor=value, date=today, type=user.account.typeAccount), 200


@app.route('/depositconfirm', methods = ['POST'])
@login_required
def depositconfirm():
    valor = float(request.form['fvalor'])
    today = time.strftime('%d/%m/%Y %H:%M:%S')
    try:
        statement = Statement('C', 'Pendente', accountId=current_user.account.id, balance=current_user.balance(), deposit=valor, withdraw=0,)
        statementDatabase.save(statement)
        account = accountDatabase.find_by_account_number(current_user.accountNumber())
        solicitationDatabase.open_deposit_solicitation(current_user.id, current_user.accountNumber(), 'Confirmação de Depósito', valor, account.id)
        depositedValue=(f'{valor:.2f}')
        return render_template('comprovante_deposito.html', name=current_user.name, agencia=current_user.agency(), conta=current_user.accountNumber(), valor=depositedValue, date=today, type=current_user.account.typeAccount), 200
    except mariadb.Error as e:
        logging.error(e)
        saldo = current_user.balance()
        saldoFormatado=(f'{saldo:.2f}')
        message = flash('Falha ao depositar')
        return render_template('deposito_confirmacao.html', name=current_user.name, agencia=current_user.agency(), conta=current_user.accountNumber(), saldo=saldoFormatado, message=message, date=today, type=current_user.account.typeAccount), 400

@app.route('/transferform')
@login_required
def transferform():
    user = current_user
    saldo = user.balance()
    saldoFormatado=(f'{saldo:.2f}')
    today = time.strftime('%d/%m/%Y %H:%M:%S')
    return render_template('utransfer.html', name=user.name, agencia=user.agency(), conta=user.accountNumber(), saldo=saldoFormatado, today=today, type=user.account.typeAccount), 200

@app.route('/transfer', methods = ['POST'])
@login_required
def transfer():
    user = current_user
    saldo = user.balance()
    saldoFormatado=(f'{saldo:.2f}')
    today = time.strftime('%d/%m/%Y %H:%M:%S')
    if not validate_form(request.form):
        message = flash('Preencha todos os campos para transferir!')
        return render_template('utransfer.html', name=user.name, agencia=user.agency(), conta=user.accountNumber(), saldo=saldoFormatado, today=today, type=user.account.typeAccount, message=message), 400
    valorStr = request.form['fvalor']
    valorStr = valorStr.replace("," , ".")
    #logging.info(f'{valorStr}')
    valor = float(valorStr)
    logging.info(f'{valor}')
    
    if valor <= 0:
        message = flash('Valor de depósito deve ser maior que R$00,00!')
        return render_template('utransfer.html', name=user.name, agencia=user.agency(), conta=user.accountNumber(), saldo=saldoFormatado, today=today, type=user.account.typeAccount, message=message), 400
    else:
        userTransfer = accountDatabase.findByAccount(request.form['faccountForTransfer'],request.form['fagencyForTransfer'])
        logging.info(f'{user.id}')

        if not userTransfer:
            message = flash('Conta não encontrada, digite outro!')
            return render_template('utransfer.html', name=user.name, agencia=user.agency(), conta=user.accountNumber(), saldo=saldoFormatado, today=today, type=user.account.typeAccount, message=message), 400

        elif userTransfer.id == user.id:
            message = flash('Você não pode fazer uma transferência para você mesmo!')
            return render_template('utransfer.html', name=user.name, agencia=user.agency(), conta=user.accountNumber(), saldo=saldoFormatado, today=today, type=user.account.typeAccount, message=message), 400
        else:
            people = (f'{userTransfer.name}') #nome de quem está recebendo 
            idPeoplefis = (f'{userTransfer.id}') #id de de quem está recebendo
            idPeople = (f'{userTransfer.account.id}') #id da conta de quem está recebendo
            accountUserT = (f'{user.accountNumber()}') #número da conta de quem está enviando
            numberAccountT = (f'{userTransfer.account.account}') #número da conta de quem está recebendo
            agencyUserT = (f'{userTransfer.account.agency}') #número da agência de quem está recebendo
            value = (f'{valor:.2f}')
            dataAtual = today
            return render_template('utransferconfirm.html', name=user.name, agencia=user.agency(), conta=user.accountNumber(), valor=value, saldo=saldoFormatado, userForTransfer=people, idForTransfer=idPeople, accountUserT=accountUserT, agencyUserT=agencyUserT, idPeoplefis=idPeoplefis, numberAccountT=numberAccountT, today=today, dataAtual=dataAtual, type=user.account.typeAccount), 200


@app.route('/transferconfirm', methods = ['POST'])
@login_required
def transferconfirm():
    transferForPeople = request.form['fidTransfer'] #id da conta do usuário que está recebendo
    userForTransfer = request.form['fuserForTransfer'] #nome do usuário que está recebendo
    valor = float(request.form['fvalor'])
    valor_format = (f'{valor:.2f}')
    today = time.strftime('%d/%m/%Y %H:%M:%S')
    accountUserT = request.form['faccountUserT'] #conta do usuário que está enviando
    agencyUserT = request.form['fagencyUserT'] #agência do usuário que está recebendo
    idPeoplefis = request.form['fidPeoplefis'] #id do usuário que está recebendo
    numberAccountT = request.form['fnumberAccountT'] #número da conta de quem está recebendo

    try:
        bankBalance = accountDatabase.getBalanceByAccountNumber(accountUserT)
        accountType = accountDatabase.getAccountTypeByAccountNumber(accountUserT)
        logging.info(f'{bankBalance}')
        if ((bankBalance >= valor) or (accountType == 'CC')):
            user = current_user
            #sacar da conta do usuário que está enviando
            newBalance = bankBalance - valor
            logging.info(f'{newBalance}')
            accountDatabase.updateBalanceByAccountNumber(newBalance, accountUserT)
            statement = Statement('T', accountId=current_user.account.id, balance=newBalance, situation='Aprovado', deposit=0, withdraw=valor, date=today)
            statementDatabase.save(statement)
       
            #depositar na conta do usuário que está recebendo
            bankBalanceRece = accountDatabase.getBalanceByIdAccount(transferForPeople)
            newBalanceRece = bankBalanceRece + valor
            accountDatabase.updateBalanceByIdAccount(newBalanceRece, transferForPeople)
            target_account = accountDatabase.find_by_account_number(numberAccountT)
            statement = Statement('T', accountId=target_account.id, situation='Aprovado', balance=newBalanceRece, deposit=valor, withdraw=0, date=today)
            statementDatabase.save(statement)
            return render_template('utransfervoucher.html', name=current_user.name, nameTransfer=userForTransfer, receNumberAccount=accountUserT, agencia=current_user.agency(), conta=current_user.accountNumber(), data=today, valor=valor_format, userForTransfer=userForTransfer, accountUserT=accountUserT, agencyUserT=agencyUserT, idPeoplefis=idPeoplefis, numberAccountT=numberAccountT, dataAtual=today, type=user.account.typeAccount), 200
        else:
            user = current_user
            saldo = user.balance()
            saldoFormatado=(f'{saldo:.2f}')
            message = flash('Valor da transferência deve ser menor que seu saldo atual')
            return render_template('utransfer.html', name=user.name, agencia=user.agency(), today=today, conta=user.accountNumber(), saldo=saldoFormatado, type=user.account.typeAccount, message=message), 400
    except mariadb.Error as e:
        logging.error(e)
        user = current_user
        saldo = current_user.balance()
        saldoFormatado=(f'{saldo:.2f}')
        message = flash('Falha ao transferir')
        return render_template('utransfervoucher.html', name=current_user.name, agencia=current_user.agency(), conta=current_user.accountNumber(), saldo=saldoFormatado, type=user.account.typeAccount, message=message), 400

@app.route('/statementform', methods = ['GET', 'POST'])
@login_required
def statementForm():
    today = time.strftime('%d/%m/%Y %H:%M:%S')
    user = current_user
    
    saldo = user.balance()
    statements = statementDatabase.find_by_account_id(user.account.id)
    accountType = accountDatabase.getAccountTypeByAccountNumber(user.accountNumber())
    logging.info(f'{user.accountNumber()}')
    logging.info(f'{accountType}')
    if request.method == "POST":
        pesquisarOperacao = request.form['pesquisarOperacao']
        dataInicio = request.form['dataInicio']
        dataFinal = request.form['dataFinal']

        search_statements = statementDatabase.searchStatement(pesquisarOperacao, user.id, accountType, dataInicio, dataFinal)

        search_operation = statementDatabase.searchOperation(pesquisarOperacao, user.id, accountType)

        search_date = statementDatabase.searchDate(user.id, accountType, dataInicio, dataFinal)

        if search_statements:
            logging.info(search_statements)
            return render_template('extrato.html', name=user.name, agencia=user.agency(), conta=user.accountNumber(), saldo=saldo, extratos=search_statements, date=today, type=user.account.typeAccount), 200
            #return searchStatement

        elif search_operation:
            return render_template('extrato.html', name=user.name, agencia=user.agency(), conta=user.accountNumber(), saldo=saldo, extratos=search_operation, date=today, type=user.account.typeAccount), 200

        elif search_date:
          return render_template('extrato.html', name=user.name, agencia=user.agency(), conta=user.accountNumber(), saldo=saldo, extratos=search_date, date=today, type=user.account.typeAccount), 200

        else:
            if ((pesquisarOperacao == '') and (dataInicio == '') and (dataFinal == '')):
                logging.info(f'Voltou todas informações!')
                return render_template('extrato.html', name=user.name, agencia=user.agency(), conta=user.accountNumber(), saldo=saldo, extratos=statements, date=today, type=user.account.typeAccount), 200
            else:
                logging.info(f'Nenhum dado encontrado no extrato!')
                message = flash('Nenhum dado encontrado no extrato!')

                
                return render_template('extrato.html', name=user.name, agencia=user.agency(), conta=user.accountNumber(), saldo=saldo, extratos=statements, date=today, type=user.account.typeAccount, message = message), 200
                
    return render_template('extrato.html', name=user.name, agencia=user.agency(), conta=user.accountNumber(), saldo=saldo, extratos=statements, date=today, type=user.account.typeAccount), 200

@app.route('/print', methods = ['GET'])
@login_required
def print():
    today = time.strftime('%d/%m/%Y %H:%M:%S')
    user = current_user
    statements = statementDatabase.find_by_account_id(user.account.id)
    return render_template('extrato_impressao.html', name=user.name, agencia=user.agency(), conta=user.accountNumber(), saldo=user.balance(), extratos=statements, date=today, type=user.account.typeAccount), 200

@app.route('/<account_id>/print', methods = ['GET'])
def follow_up_statements(account_id):
    today = time.strftime('%d/%m/%Y %H:%M:%S')
    user = userDatabase.find_by_account_id(account_id)
    statements = statementDatabase.find_by_account_id(account_id)
    return render_template('extrato_impressao.html', name=user.name, agencia=user.agency(), conta=user.accountNumber(), saldo=user.balance(), extratos=statements, date=today, type=user.account.typeAccount), 200

@app.route('/update_user_data', methods = ['GET'])
@login_required
def update_user_data():
    user=current_user
    aniversario = user.birthDate
    birthDate = aniversario.strftime("%d/%m/%Y")
    return render_template('alteracaodados.html', user=user, birthDate=birthDate), 200

@app.route('/update_user_data', methods = ['POST'])
@login_required
def open_update_user_data_solicitation():
    today = time.strftime('%d/%m/%Y %H:%M:%S')
    user=current_user
    if not validate_form(request.form):
        message = flash('Preencha todos os campos!')
        return render_template('alteracaodados.html', user=user), 200
    solicitation= UpdateDataSolicitation(request.form ['fname'], request.form ['froad'], request.form ['fnumberHouse'], request.form ['fdistrict'], request.form ['fcep'], request.form ['fcity'], request.form ['fstate'], request.form ['fgenre'], user_id=user.id)
    solicitationDatabase.open_update_data_solicitation(user.id, solicitation, user.account.id)
    flash('Solicitação de alteração realizada com sucesso')
    return render_template('home.html', name=user.name, agencia=user.agency(), conta=user.accountNumber(), saldo=user.balance(), date=today, type=user.account.typeAccount), 200

@app.route('/close-account', methods = ['GET'])
@login_required
def close_account():
    user=current_user
    today = time.strftime('%d/%m/%Y %H:%M:%S')
    if int(user.balance()) > int(0.0):
        return render_template('accountclosenotification.html', user=user, date=today, type=user.account.typeAccount), 200
    elif int(user.balance()) < int(0.0):
        return render_template('accountclosereprove.html', user=user, date=today, type=user.account.typeAccount), 200
    return render_template('accountclosesolicitation.html', user=user, date=today, type=user.account.typeAccount), 200

@app.route('/close-account', methods = ['POST'])
@login_required
def close_account_solicitation():
    user=current_user
    close_account(user)
    flash('Solicitação de encerramento de conta criada!')
    logout_user()
    return render_template('acompanhamento.html'), 200
    
# @app.route('/proceed-close-account', methods = ['POST'])
# @login_required
# def proceed_close_account_solicitation():
#     user = current_user
#     close_account(user)
#     flash('Solicitação de encerramento de conta criada!')
#     logout_user()
#     return render_template('acompanhamento.html'), 200

def close_account(user):
    account = accountDatabase.find_by_account_number(user.account.account)
    logging.info(f'Solicitando encerramento de conta para conta {account.id}')
    solicitation= CloseAccountSolicitation(account.id, user.name, user.cpf, user.birthDate, user.address.road, user.address.numberHouse, user.address.district, user.address.cep, user.address.city, user.address.state, user.gender, user_id=user.id)
    solicitationDatabase.open_close_account_solicitation(user.id, solicitation, account.id)
    solicitation_id = solicitationDatabase.find_solicitation_id_by_account_id_and_solicitation_type(account.id, 'Abertura de conta')
    accountDatabase.analysis_account_by_solicitation_id(solicitation_id)
    solicitationDatabase.update_status_by_id(solicitation_id, 'Em Análise')
    logging.info(f'Inativando conta {account.account}')
    accountDatabase.inactivate_account(account.account)

def userExists(cpf):
    return userDatabase.findByCpf(cpf)

def validate_form(form):
    for key in form:
        if not form[key]:
            return False
    return True

def update_user_balance(value):
    current_user.account.deposit(value)
    accountDatabase.updateBalanceByAccountNumber(current_user.balance(), current_user.accountNumber())

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)
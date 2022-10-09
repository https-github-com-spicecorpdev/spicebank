from flask import Flask, request, render_template, session, flash, redirect, url_for
from flask_session import Session
from datetime import datetime
import mariadb
import sys

try:
    connection = mariadb.connect(
        user="root",
        password="124879",
        host="127.0.0.1",
        port=3306,
        database = "spicebank"
    )
except mariadb.Error as e:
   print(f"Error connecting to the database: {e}")
   sys.exit(1)

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/')
def index():
    if session.get('autenticado'):
        return render_template('home.html', name=session['nameUser'], agencia=session['agencyUser'], conta=session['numberAccount'], saldo=session['totalbalance']), 200
    else:
        return render_template('login.html'), 200

@app.route('/login', methods = ['POST'])
def login():
    if not validate_form(request.form):
            message = flash('Preencha todos os campos!')
            return render_template('login.html', message=message), 400
    cursor = connection.cursor()
    query = "SELECT U.idUser AS idUser, U.nameUser AS nameUser, U.passwordUser AS passwordUser, A.agencyUser AS agencyUser, U.cpfUser AS cpfUser, A.idAccount AS idAccount, A.numberAccount AS numberAccount, A.totalbalance AS totalbalance, A.idAccountUser AS idAccountUser, A.statusAccount AS statusAccount FROM tuser AS U INNER JOIN taccount AS A ON idUser = idAccountUser WHERE agencyUser = ? AND numberAccount = ? AND passwordUser = ? "
    parameters = (request.form['fagency'], request.form['faccount'], request.form['fpassword'], )
    print(parameters)
    cursor.execute(query, parameters)
    user = cursor.fetchone()
    print(user)
    if user and not (user[0] == ''):
        session['autenticado'] = True
        session['idUser']=user[0]
        session['nameUser']=user[1]
        session['cpfUser']=user[4]
        session['agencyUser']=user[3]
        session['numberAccount']=user[6]
        session['totalbalance']=float(user[7])
        session['idAccount']=user[5]
        return render_template('home.html', name=session['nameUser'], agencia=session['agencyUser'], conta=session['numberAccount'], saldo=session['totalbalance'], idAccount=session['idAccount']), 200
    else:
        session['autenticado']=False
        message = flash(f'Login inválido, verifique os dados de acesso!')
    return render_template('login.html', message=message), 400

@app.route('/logout')
def logout():
    session['autenticado']=False
    session.clear()
    return render_template('login.html'), 200

@app.route('/acompanhamentoform')
def acompanhamentoform():
    return render_template('acompanhamento.html'), 200

@app.route('/loginAcomp', methods = ['POST'])
def loginAcomp():
    if not validate_form(request.form):
            message = flash('Preencha todos os campos!')
            return render_template('login.html', message=message), 400
    cursor = connection.cursor()
    query = "SELECT U.idUser AS idUser, U.nameUser AS nameUser, U.cpfUser AS cpfUser, U.passwordUser AS passwordUser, A.idAccount AS idAccount, A.idAccountUser AS idAccountUser, A.solicitacao AS solicitacao FROM tuser AS U INNER JOIN taccount AS A ON idUser = idAccountUser WHERE cpfUser = ? AND passwordUser = ? "
    parameters = (request.form['fcpf'], request.form['fpassword'], )
    print(parameters)
    cursor.execute(query, parameters)
    user = cursor.fetchone()
    print(user)


    if user and not (user[0] == ''):
        session['autenticado'] = True
        session['nameUser']=user[1]
        session['cpfUser']=user[2]
        session['solicitacao']=user[6]
        if user[6] == "aprovado":
            cursor = connection.cursor()
            query = "SELECT U.idUser AS idUser, U.nameUser AS nameUser, U.cpfUser AS cpfUser, U.passwordUser AS passwordUser, A.idAccount AS idAccount, A.idAccountUser AS idAccountUser, A.solicitacao AS solicitacao, A.numberAccount AS numberAccount, A.agencyUser AS agencyUser FROM tuser AS U INNER JOIN taccount AS A ON idUser = idAccountUser WHERE cpfUser = ? AND passwordUser = ? "
            parameters = (request.form['fcpf'], request.form['fpassword'], )
            print(parameters)
            cursor.execute(query, parameters)
            user = cursor.fetchone()
            session['agencyUser']=user[8]
            session['numberAccount']=user[7]
            message = flash(f'Agência:{user[8]} / Conta:{user[7]}')
            message = flash('Grave sua agencia e conta')
            return render_template('homeAcomp.html', name=session['nameUser'], agencia=session['agencyUser'], conta=session['numberAccount'], solicitacao=session['solicitacao'], message=(message)), 200
            
        else:
            message = flash('Aguardando análise de solicitação')
            return render_template('homeAcomp.html', name=session['nameUser'],cpf=session['cpfUser'], solicitacao=session['solicitacao']), 200
    else:
        session['autenticado']=False
        message = flash(f'Login inválido, verifique os dados de acesso!')
    return render_template('login.html', message=message), 400

@app.route('/admForm')
def admForm():
    return render_template('loginGerente.html'), 200

@app.route('/loginGerente', methods = ['POST'])
def loginGerente():
    if not validate_form(request.form):
            message = flash('Preencha todos os campos!')
            return render_template('login.html', message=message), 400
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
                    # message = flash(f'Nome:{user[1]} / Conta:{user[6]}')

                    #CONTAS ATRELADAS AQUELA AGÊNCIA

                    return render_template('homeGerente.html', name=session['nameUser'], agenciadoGer=session['accountAgency'], solicitacao=session['solicitacao'], userDetails = rows, numeroConta=session['numberAccount'], message=(message)), 200

            else:
                return render_template('homeGerente.html', message=(message)), 200

            
        else:
            message = flash('Bem-Vindo Gerente Geral!')
            return render_template('homeGerente.html', name=session['nameUser'],cpf=session['cpfUser']), 200
    else:
        session['autenticado']=False
        message = flash(f'Esta conta não é da gerência, faça login como Usuário!')
    return render_template('login.html', message=message), 400

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
                    query = "INSERT INTO tuser (nameUser, cpfUser, passwordUser, roadUser, districtUser, numberHouseUser, cepUser, celUser, genreUser, birthdateUser, fdistrict) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"
                    parameters = (request.form['fname'], request.form['fcpf'], request.form['fpassword'], request.form['fcity'], request.form['fstate'], request.form['fnumberhouse'], request.form['fcep'], request.form['fcel'], request.form['fgenre'], request.form['fbirthday'], request.form['fdistrict'],)
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
        message = flash(f'Este usuário foi para a sua agência')
        return render_template('homeGerente.html', message=(message)), 200

#Abertura de conta


#Abertura de conta bancária
# INSERT INTO taccount (numberAccount, totalbalance, idAccountUser) values ('12', '0', LAST_INSERT_ID());

@app.route('/withdrawform')
def withdrawform():
    if session.get("autenticado"):
        return render_template('saque.html', name=session['nameUser'], agencia=session['agencyUser'], conta=session['numberAccount'], saldo=session['totalbalance'], idAccount=session['idAccount']), 200
    else:
        session['autenticado']=False
        return render_template('login.html'), 200

@app.route('/withdraw', methods = ['POST'])
def withdraw():
    print(session['idAccount'])
    if session.get("autenticado"):
        if not validate_form(request.form):
            message = flash('Preencha um valor para sacar!')
            return render_template('saque.html', name=session['nameUser'], agencia=session['agencyUser'], conta=session['numberAccount'], saldo=session['totalbalance'], idAccount=session['idAccount'], message=message), 400
        else:
            valor = float(request.form['fvalor'])
            if valor <= 0:
                message = flash('Valor de saque deve ser maior que R$00,00!')
                return render_template('saque.html', name=session['nameUser'], agencia=session['agencyUser'], conta=session['numberAccount'], saldo=session['totalbalance'], idAccount=session['idAccount'], message=message), 400
            try:
                cursor = connection.cursor()
                query = "SELECT totalbalance FROM taccount WHERE idAccount = ?"
                contaUser = session['idAccount']
                parameters = (contaUser,)
                print(parameters)
                cursor.execute(query, parameters)
                balance = float(cursor.fetchone()[0])
                print(balance)
                if balance >= valor:
                    query = "SELECT U.idUser AS idUser, U.cpfUser AS cpfUser, A.idAccount AS idAccount, A.totalbalance AS totalbalance, A.idAccountUser AS idAccountUser, A.numberAccount AS numberAccount FROM tuser AS U INNER JOIN taccount AS A ON idUser = idAccountUser WHERE idAccount = ?"
                    # query = "SELECT total FROM users WHERE BINARY cpf = ?"
                    contaUser = session['idAccount']
                    parameters = (contaUser,)
                    print(parameters)
                    cursor.execute(query, parameters)
                    balanceUser = float(cursor.fetchone()[0])
                    novoSaldoUser = balanceUser - valor
                    novoSaldo = balance - valor
                    query = "UPDATE taccount SET totalbalance = ? WHERE idAccount = ?"
                    parameters = (novoSaldo, session.get("idAccount"))
                    print(parameters)
                    cursor.execute(query, parameters)
                    connection.commit()
                    session['totalbalance'] = float(novoSaldo)
                    import time    
                    today = time.strftime('%Y-%m-%d %H:%M:%S')
                    query = "INSERT INTO textract (userExtract, depositExtract, withdrawExtract, dateExtract) values (?, 0, ?, ?);"
                    print(valor)
                    parameters = (session.get("idUser"), valor, today)
                    print(parameters)
                    cursor.execute(query, parameters)
                    connection.commit()
                    message = flash(f'Saque de R${valor} efetuado com sucesso! Saldo: R${novoSaldo}')
                    return render_template('saque.html', name=session['nameUser'], agencia=session['agencyUser'], conta=session['numberAccount'], saldo=session['totalbalance'], idAccount=session['idAccount'], message=message), 200
                else:
                    message = flash('Valor maior que o saldo disponível!')
                    return render_template('saque.html', name=session['nameUser'], agencia=session['agencyUser'], conta=session['numberAccount'], saldo=session['totalbalance'], idAccount=session['idAccount'], message=message), 400
            except mariadb.Error as e:
                print(e)
                return "Erro ao sacar valor desejado!", 400
    else:
        session['autenticado']=False
        return render_template('login.html'), 200

@app.route('/depositform')
def depositform():
    if session.get("autenticado"):
        return render_template('deposito.html', id=session['idUser'], name=session['nameUser'], agencia=session['agencyUser'], conta=session['numberAccount'], saldo=session['totalbalance']), 200
    else:
        session['autenticado']=False
        return render_template('login.html'), 200

@app.route('/deposit', methods = ['POST'])
def deposit():
    if session.get("autenticado"):
        if not validate_form(request.form):
            message = flash('Preencha um valor para depositar!')
            return render_template('deposito.html', name=session['nameUser'], agencia=session['agencyUser'], conta=session['numberAccount'], saldo=session['totalbalance'], message=message), 400
        valor = float(request.form['fvalor'])
        if valor <= 0:
            message = flash('Valor de depósito deve ser maior que R$00,00!')
            return render_template('deposito.html', name=session['nameUser'], agencia=session['agencyUser'], conta=session['numberAccount'], saldo=session['totalbalance'], message=message), 400
        try:
                cursor = connection.cursor()
                query = "SELECT totalbalance FROM taccount WHERE idAccount = ?"
                contaUser = session['idAccount']
                parameters = (contaUser,)
                print(parameters)
                cursor.execute(query, parameters)
                balance = float(cursor.fetchone()[0])
                print(balance)
                query = "SELECT U.idUser AS idUser, U.cpfUser AS cpfUser, A.idAccount AS idAccount, A.totalbalance AS totalbalance, A.idAccountUser AS idAccountUser, A.numberAccount AS numberAccount FROM tuser AS U INNER JOIN taccount AS A ON idUser = idAccountUser WHERE idAccount = ?"
                # query = "SELECT total FROM users WHERE BINARY cpf = ?"
                contaUser = session['idAccount']
                parameters = (contaUser,)
                print(parameters)
                cursor.execute(query, parameters)
                balanceUser = float(cursor.fetchone()[0])
                novoSaldo = balance + valor
                query = "UPDATE taccount SET totalbalance = ? WHERE idAccount = ?"
                parameters = (novoSaldo, session.get("idAccount"))
                print(parameters)
                cursor.execute(query, parameters)
                connection.commit()
                session['totalbalance'] = float(novoSaldo)
                import time    
                today = time.strftime('%Y-%m-%d %H:%M:%S')
                query = "INSERT INTO textract (userExtract, depositExtract, withdrawExtract, dateExtract) values (?, ?, 0, ?);"
                parameters = (session.get("idUser"), valor, today)
                print(parameters)
                print(valor)
                cursor.execute(query, parameters)
                connection.commit()
                message = flash(f'Depósito de R${valor} efetuado com sucesso! Saldo: R${novoSaldo}')
                return render_template('deposito.html', name=session['nameUser'], agencia=session['agencyUser'], conta=session['numberAccount'], saldo=session['totalbalance'], idAccount=session['idAccount'], message=message), 200

        except mariadb.Error as e:
            print(e)
            message = flash('Falha ao depositar')
            return render_template('deposito.html', name=session['nameUser'], agencia=session['agencyUser'], conta=session['numberAccount'], saldo=session['totalbalance'], message=message), 400
    else:
        session['autenticado']=False
        return render_template('login.html'), 200

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

def update_bank_balance(bank_id, valor):
    cursor = connection.cursor()
    query = "SELECT totalbalance FROM taccount WHERE idAccount = ?"
    parameters = (bank_id,)
    cursor.execute(query, parameters)
    balance = float(cursor.fetchone()[0])
    new_bank_balance = balance + valor
    query = "UPDATE taccount SET totalbalance = ? WHERE idAccount = ?"
    parameters = (new_bank_balance, bank_id,)
    cursor.execute(query, parameters)
    connection.commit()

def update_user_balance(user_account, valor):
    cursor = connection.cursor()
    query = "SELECT totalbalance FROM taccount WHERE numberAccount = ?"
    parameters = (user_account,)
    cursor.execute(query, parameters)
    balance = float(cursor.fetchone()[0])
    new_user_balance = balance + valor
    query = "UPDATE taccount SET totalbalance = ? WHERE numberAccount = ?"
    parameters = (new_user_balance, user_account,)
    cursor.execute(query, parameters)
    connection.commit()
    session['totalbalance'] = float(new_user_balance)

@app.route('/extract',methods = ['GET'])
def extract():
    if session.get("autenticado"):
        try:
            cursor= connection.cursor()
            query = "SELECT E.userExtract AS userExtract, E.depositExtract AS depositExtract, E.withdrawExtract AS withdrawExtract, E.dateExtract AS dateExtract, U.idUser AS idUser, U.nameUser AS nameUser FROM tuser AS U INNER JOIN textract AS E ON idUser=userExtract WHERE userExtract = ?"
            contaUser = session['idUser']
            parameters = (contaUser,)
            print(parameters)
            cursor.execute(query, parameters)
            rows =cursor.fetchall()
            print(rows)
            if cursor.rowcount > 0:
                print(cursor.rowcount)
                for user in rows:
                    print(user)
                while user[0] > 0:
                        session['depositExtract']=user[1]
                        session['withdrawExtract']=user[2]
                        session['dateExtract']=user[3]
                        session['nameUser']=user[5]
                        return render_template('extrato.html', name=session['nameUser'],saldo=session['totalbalance'], agencia=session['agencyUser'], conta=session['numberAccount'], deposit=session['depositExtract'], withdraw=session['withdrawExtract'], extractDetails=rows),200
        except mariadb.Error as e:
            message = flash('Falha ao verificar extrato')
            return render_template('extrato.html', name=session['nameUser'], agencia=session['agencyUser'], conta=session['numberAccount'],  message=message ), 400
    else:
        session['autenticado']=False                                  
        return render_template('login.html'), 200

if __name__ == "__main__":

    app.run(debug=True)
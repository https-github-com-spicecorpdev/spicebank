from crypt import methods
from flask import Flask, request, render_template, session, flash, redirect, url_for
from flask_session import Session
import mariadb
import sys

try:
    connection = mariadb.connect(
        user="root",
        password="123456",
        host="127.0.0.1",
        port=3308,
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
        return render_template('home.html', name=session['name'], agencia=session['agency'], conta=session['account'], saldo=session['balance']), 200
    else:
        return render_template('login.html'), 200

@app.route('/login', methods = ['POST'])
def login():
    if not validate_form(request.form):
            message = flash('Preencha todos os campos!')
            return render_template('login.html', message=message), 400
    cursor = connection.cursor()
    query = "SELECT name, cpf, agency, account, balance FROM users WHERE BINARY agency = ? AND account = ? AND password = ?"
    parameters = (request.form['fagency'], request.form['faccount'], request.form['fpassword'], )
    print(parameters)
    cursor.execute(query, parameters)
    user = cursor.fetchone()
    if user and not (user[0] == ''):
        session['autenticado'] = True
        session['name']=user[0]
        session['cpf']=user[1]
        session['agency']=user[2]
        session['account']=user[3]
        session['balance']=float(user[4])
        return render_template('home.html', name=session['name'], agencia=session['agency'], conta=session['account'], saldo=session['balance']), 200
    else:
        session['autenticado']=False
        message = flash(f'Login inválido, verifique os dados de acesso!')
    return render_template('login.html', message=message), 400

@app.route('/logout')
def logout():
    session['autenticado']=False
    session.clear()
    return render_template('login.html'), 200

@app.route('/registerform')
def registerForm():
    return render_template('cadastro.html'), 200

@app.route('/register', methods = ['POST'])
def register():
        cursor = connection.cursor()
        if not validate_form(request.form):
            message = flash('Preencha todos os campos!')
            return render_template('cadastro.html', message=message), 400
        if not userExists(request.form['fcpf']):
            try:
                query = "INSERT INTO users (name, cpf, password, account) values(?, ?, ?, next value for account_number)"
                parameters = (request.form['fname'], request.form['fcpf'], request.form['fpassword'],)
                cursor.execute(query, parameters)
                connection.commit()
                return render_template('login.html'), 201
            except mariadb.Error as e:
                print(e)
                return "Erro ao cadastrar usuário", 400
        else:
            requestCpf = request.form['fcpf']
            message = flash(f'CPF {requestCpf} com cadastrado existente!')
        return render_template('cadastro.html', message=message), 400

@app.route('/withdrawform')
def withdrawform():
    if session.get("autenticado"):
        return render_template('saque.html', name=session['name'], agencia=session['agency'], conta=session['account'], saldo=session['balance']), 200
    else:
        session['autenticado']=False
        return render_template('login.html'), 200

@app.route('/withdraw', methods = ['POST'])
def withdraw():
    if session.get("autenticado"):
        if not validate_form(request.form):
            message = flash('Preencha um valor para sacar!')
            return render_template('saque.html', name=session['name'], agencia=session['agency'], conta=session['account'], saldo=session['balance'], message=message), 400
        valor = float(request.form['fvalor'])
        if valor <= 0:
            message = flash('Valor de saque deve ser maior que R$00,00!')
            return render_template('saque.html', name=session['name'], agencia=session['agency'], conta=session['account'], saldo=session['balance'], message=message), 400
        try:
            cursor = connection.cursor()
            query = "SELECT balance FROM bank WHERE BINARY id = ?"
            parameters = (1,)
            cursor.execute(query, parameters)
            balance = float(cursor.fetchone()[0])
            if balance >= valor:
                query = "SELECT balance FROM users WHERE BINARY cpf = ?"
                parameters = (session.get("cpf"),)
                cursor.execute(query, parameters)
                balanceUser = float(cursor.fetchone()[0])
                novoSaldoUser = balanceUser - valor
                novoSaldo = balance - valor
                query = "UPDATE bank SET balance = ? WHERE id = ?"
                parameters = (novoSaldo, 1,)
                cursor.execute(query, parameters)
                queryuser = "UPDATE users SET balance = ? WHERE account = ?"
                parametersUser = (novoSaldoUser, session.get("account"))
                cursor.execute(queryuser, parametersUser)
                connection.commit()
                session['balance'] = float(novoSaldoUser)
                message = flash(f'Saque efetuado com sucesso! Saldo: R${novoSaldoUser}')
                return render_template('saque.html', name=session['name'], agencia=session['agency'], conta=session['account'], saldo=session['balance'], message=message), 200
            else:
                message = flash('Valor maior que o saldo disponível!')
                return render_template('saque.html', name=session['name'], agencia=session['agency'], conta=session['account'], saldo=session['balance'], message=message), 400
        except mariadb.Error as e:
            print(e)
            return "Erro ao cadastrar usuário", 400
    else:
        session['autenticado']=False
        return render_template('login.html'), 200

@app.route('/depositform')
def depositform():
    if session.get("autenticado"):
        return render_template('deposito.html', name=session['name'], agencia=session['agency'], conta=session['account'], saldo=session['balance']), 200
    else:
        session['autenticado']=False
        return render_template('login.html'), 200

@app.route('/deposit', methods = ['POST'])
def deposit():
    if session.get("autenticado"):
        if not validate_form(request.form):
            message = flash('Preencha um valor para depositar!')
            return render_template('deposito.html', name=session['name'], agencia=session['agency'], conta=session['account'], saldo=session['balance'], message=message), 400
        valor = float(request.form['fvalor'])
        if valor <= 0:
            message = flash('Valor de depósito deve ser maior que R$00,00!')
            return render_template('deposito.html', name=session['name'], agencia=session['agency'], conta=session['account'], saldo=session['balance'], message=message), 400
        try:
            bank_id = 1
            user_account = session.get("account")
            update_bank_balance(bank_id, valor)
            update_user_balance(user_account, valor)
            saldo=session['balance']
            message = flash(f'Depósito efetuado com sucesso! Saldo: R${saldo}')
            return render_template('deposito.html', name=session['name'], agencia=session['agency'], conta=session['account'], saldo=session['balance'], message=message), 200
        except mariadb.Error as e:
            print(e)
            message = flash('Falha ao depositar')
            return render_template('deposito.html', name=session['name'], agencia=session['agency'], conta=session['account'], saldo=session['balance'], message=message), 400
    else:
        session['autenticado']=False
        return render_template('login.html'), 200

def userExists(cpf):
    cursor = connection.cursor()
    query = "SELECT name FROM users WHERE BINARY cpf = ?"
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
    query = "SELECT balance FROM bank WHERE BINARY id = ?"
    parameters = (bank_id,)
    cursor.execute(query, parameters)
    balance = float(cursor.fetchone()[0])
    new_bank_balance = balance + valor
    query = "UPDATE bank SET balance = ? WHERE id = ?"
    parameters = (new_bank_balance, bank_id,)
    cursor.execute(query, parameters)
    connection.commit()

def update_user_balance(user_account, valor):
    cursor = connection.cursor()
    query = "SELECT balance FROM users WHERE BINARY account = ?"
    parameters = (user_account,)
    cursor.execute(query, parameters)
    balance = float(cursor.fetchone()[0])
    new_user_balance = balance + valor
    query = "UPDATE users SET balance = ? WHERE account = ?"
    parameters = (new_user_balance, user_account,)
    cursor.execute(query, parameters)
    connection.commit()
    session['balance'] = float(new_user_balance)

app.run(host='0.0.0.0', port=8081)
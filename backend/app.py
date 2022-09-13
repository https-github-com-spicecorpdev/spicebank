from crypt import methods
from flask import Flask, request, render_template, session
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
        return render_template('login.html'), 20

@app.route('/login', methods = ['POST'])
def login():
    if not validate_form(request.form):
            message = f'Preencha todos os campos!'
            return render_template('error.html', message=message), 400
    cursor = connection.cursor()
    query = "SELECT name, cpf, agency, account, balance FROM users WHERE BINARY cpf = ? AND password = ?"
    parameters = (request.form['fcpf'], request.form['fpassword'], )
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
        requestCpf = request.form['fcpf']
        message = f'Usuário com cpf {requestCpf} não encontrado!'
        return render_template('error.html', message=message), 404

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
            message = f'Preencha todos os campos!'
            return render_template('error.html', message=message), 400
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
            message = f'CPF {requestCpf} já cadastrado!'
            return render_template('error.html', message=message), 404

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
            message = 'Preencha um valor para sacar!'
            return render_template('error.html', message=message), 400
        valor = float(request.form['fvalor'])
        if valor <= 0:
            message = 'Valor de saque deve ser maior que R$00,00!'
            return render_template('error.html', message=message), 400
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
                return render_template('home.html', name=session['name'], agencia=session['agency'], conta=session['account'], saldo=session['balance']), 200
            else:
                message = 'Valor indisponível!'
                return render_template('error.html', message=message), 400
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
        message = 'Não implementado!'
        return render_template('error.html', message=message), 400
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

app.run(host='0.0.0.0', port=8081)
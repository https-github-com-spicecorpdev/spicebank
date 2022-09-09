from crypt import methods
from flask import Flask, request, render_template, session
from flask_session import Session
import mariadb
import sys

try:
    connection = mariadb.connect(
        user="",
        password="",
        host="127.0.0.1",
        port=3308,
        database = ""
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
        return render_template('home.html', name=session['name'], agencia=session['agencia'], conta=session['conta'], saldo=session['saldo']), 200
    else:
        return render_template('login.html'), 20

@app.route('/login', methods = ['POST'])
def login():
    cursor = connection.cursor()
    query = "SELECT name FROM users WHERE BINARY cpf = ? AND password = ?"
    parameters = (request.form['fcpf'], request.form['fpassword'], )
    cursor.execute(query, parameters)
    user = cursor.fetchone()
    if user:
        session['autenticado'] = True
        session['name']=user[0]
        session['agencia']=123
        session['conta']='0001'
        session['saldo']=100
        return render_template('home.html', name=session['name'], agencia=session['agencia'], conta=session['conta'], saldo=session['saldo']), 200
    else:
        session['autenticado']=False
        requestCpf = request.form['fcpf']
        message = f'Usuário com cpf {requestCpf} não encontrado!'
        return render_template('error.html', message=message), 404

@app.route('/logout')
def logout():
    session['autenticado']=False
    return render_template('login.html'), 20

@app.route('/registerform')
def registerForm():
    return render_template('cadastro.html'), 200

@app.route('/register', methods = ['POST'])
def register():
        cursor = connection.cursor()
        if not userExists(request.form['fcpf']):
            try:
                query = "INSERT INTO users (name, cpf, password) values(?, ?, ?)"
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
        return render_template('saque.html', name=session['name'], agencia=session['agencia'], conta=session['conta'], saldo=session['saldo']), 200
    else:
        session['autenticado']=False
        return render_template('login.html'), 200

@app.route('/withdraw', methods = ['POST'])
def withdraw():
    if session.get("autenticado"):
        print(session.get("autenticado"))
        try:
            return f"""
                <h1>{session.get('name')}</h1>
                <h2>Verificar se possui saldo suficiente</h2><br>
                <h3>caso positivo: Realizar update na tabela subtraindo o valor e mostrar uma tela de confirmação (Criar um template.html)</h3>
                <h3>caso negativo: fazer um alert no navegador informando que o saldo é insuficiente.</h3>
                <a href="/">
                    <button type="button">Voltar para home</button>
                </a>
            """, 201
        except mariadb.Error as e:
            print(e)
            return "Erro ao cadastrar usuário", 400
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

app.run(host='0.0.0.0', port=8081)
import logging
from flask import Flask
from flask_login import LoginManager
from . import db
from .user_database import UserDatabase
from .account_database import AccountDatabase
from .statement_database import StatementDatabase
from .manager_database import ManagerDatabase
from .solicitation_database import SolicitationDatabase
from .bank_database import BankDatabase

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
logging.info('Inicializando a configuração da aplicação...')

connection = db.connect()

def create_app():
    app = Flask(__name__)
    app.secret_key = 'secret'
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view='login'
    login_manager.login_message='Realize o login para acessar sua conta'

    logging.info('Aplicação configurada com sucesso!')
    
    return app, login_manager

def create_manager_app():
    manager_app = Flask(__name__)
    manager_app.secret_key = 'secreta'

    manager_login = LoginManager()
    manager_login.init_app(manager_app)
    manager_login.login_view='loginGerente'
    manager_login.login_message='Realize o login para acessar sua conta'

    logging.info('Aplicação configurada com sucesso!')
    
    return manager_app, manager_login

def get_repositories():
    accountDatabase = AccountDatabase(connection)
    statementDatabase = StatementDatabase(connection)
    solicitationDatabase= SolicitationDatabase(connection)
    bankDatabase= BankDatabase(connection)
    userDatabase = UserDatabase(connection)
    return accountDatabase, statementDatabase, solicitationDatabase, bankDatabase, userDatabase

def get_manager_repositories():
    managerDatabase = ManagerDatabase(connection)
    return managerDatabase

def get_connection():
    return connection
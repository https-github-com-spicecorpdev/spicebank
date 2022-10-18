import logging
from flask import Flask
from flask_login import LoginManager
from . import db
from .user_database import UserDatabase
from .account_database import AccountDatabase
from .statement_database import StatementDatabase
from flask_session import Session

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
logging.info('Inicializando a configuração da aplicação...')

# app=None

connection = db.connect()
accountDatabase = AccountDatabase(connection)
userDatabase = UserDatabase(connection)
statementDatabase = StatementDatabase(connection)

def create_app(configuration=None):
    # if app:
    #     return app, login_manager
    app = Flask(__name__)
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view='login'
    login_manager.login_message='Realize o login para acessar sua conta'

    logging.info('Aplicação configurada com sucesso!')
    
    return app, login_manager

def get_db_connection():
    return connection

def get_account_database():
    return accountDatabase

def get_user_database():
    return userDatabase

def get_statement_database():
    return statementDatabase


import logging
from flask import Flask
from flask_login import LoginManager
from . import db
from flask_session import Session

def create_app(configuration=None):
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
    logging.info('Inicializando a configuração da aplicação...')

    connection = db.connect()

    app = Flask(__name__)
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view='login'
    login_manager.login_message='Realize o login para acessar sua conta'

    logging.info('Aplicação configurada com sucesso!')
    
    return app, connection, login_manager

import logging
import mariadb
from .user import User
from .account import Account
from .user_solicitation import Solicitation

class UserRepository:
    def __init__(self, connection):
        self.db = connection
        logging.info('Repositório de usuários inicializado!')

    def findById(self, id):
        cursor = self.db.cursor(dictionary=True)
        query = """
        SELECT USR.*, ACCOUNT.* 
        FROM tuser AS USR INNER JOIN taccount AS ACCOUNT ON USR.idUser = ACCOUNT.idAccountUser
        WHERE USR.idUser = ?
        """
        parameters = (id, )
        cursor.execute(query, parameters) 
        userFromDB = cursor.fetchone()
        if userFromDB:
            account = Account(id=userFromDB['idUser'],accountNumber=userFromDB['numberAccount'], userAgency=userFromDB['agencyUser'], totalBalance=userFromDB['totalbalance'], status=userFromDB['statusAccount'], solicitacao=userFromDB['solicitacao'])
            return User(userFromDB['idUser'], userFromDB['nameUser'], userFromDB['cpfUser'], userFromDB['passwordUser'], userFromDB['birthdateUser'], userFromDB['genreUser'], account=account, applicationProfile=userFromDB['profileUser'])
        else:
            logging.info(f'Usuário com o id: {id} não encontrado!')
            return None
    
    def findByAgencyAccountAndPassword(self, agency, account, password):
        cursor = self.db.cursor(dictionary=True)
        query = """
            SELECT USR.*, ACCOUNT.* 
            FROM tuser AS USR INNER JOIN taccount AS ACCOUNT ON USR.idUser = ACCOUNT.idAccountUser
            WHERE ACCOUNT.agencyUser = ?
            AND ACCOUNT.numberAccount = ?
            AND USR.passwordUser = ?
        """
        parameters = (agency, account, password)
        cursor.execute(query, parameters)
        userFromDB = cursor.fetchone()
        if userFromDB:
            account = Account(id=userFromDB['idUser'],accountNumber=userFromDB['numberAccount'], userAgency=userFromDB['agencyUser'], totalBalance=userFromDB['totalbalance'])
            return User(userFromDB['idUser'], userFromDB['nameUser'], userFromDB['cpfUser'], password, userFromDB['birthdateUser'], userFromDB['genreUser'], account=account, applicationProfile=userFromDB['profileUser'])
        else:
            logging.info(f'Usuário não encontrado!')
            return None

    def findIdByUser(self, user):
        cursor = self.db.cursor(dictionary=True)
        query = """
            SELECT idUser
            FROM tuser 
            WHERE cpfUser = ? and passwordUser = ?;
        """
        parameters = (user.cpf, user.password, )
        try:
            cursor.execute(query, parameters)
            userIdFromDB = cursor.fetchone()
            if userIdFromDB:
                return userIdFromDB['idUser']
            else:
                return None
        except mariadb.Error as e:
            logging.error(e)

    def save(self, user):
        cursor = self.db.cursor()
        query = """
            INSERT INTO tuser (nameUser, cpfUser, roadUser, numberHouseUser, districtUser, cepUser, cityUser, stateUser, birthdateUser, genreUser, passwordUser) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """
        address = user.address
        parameters = (user.name, user.cpf, address.road, address.numberHouse, address.district, address.cep, address.city, address.state, user.birthDate, user.gender, user.password,)
        try:
            cursor.execute(query, parameters)
            self.db.commit()
        except mariadb.Error as e:
            logging.error(e)
        return self.findIdByUser(user)

    def findSolicitationByCpfAndPassword(self, cpf, password):
        cursor = self.db.cursor(dictionary=True)
        query = """
        SELECT USR.*, ACCOUNT.* 
        FROM tuser AS USR INNER JOIN taccount AS ACCOUNT ON idUser = idAccountUser 
        WHERE cpfUser = ? AND passwordUser = ?
        """
        parameters = (cpf, password,)
        try:
            cursor.execute(query, parameters)
            userStatus = cursor.fetchone()
            if userStatus:
                return Solicitation(userStatus['nameUser'], cpf, password, userStatus['solicitacao'], userStatus['numberAccount'], userStatus['agencyUser'])
            else:
                logging.info(f'Solicitação com cpf: {cpf} não encontrada!')
                return None
        except mariadb.Error as e:
            logging.error(e)

    def findByCpf(self, cpf):
        cursor = self.db.cursor(dictionary=True)
        query = """
        SELECT USR.*, ACCOUNT.* 
        FROM tuser AS USR INNER JOIN taccount AS ACCOUNT ON idUser = idAccountUser 
        WHERE cpfUser = ?
        """
        parameters = (cpf,)
        try:
            cursor.execute(query, parameters)
            userFromDB = cursor.fetchone()
            if userFromDB:
                account = Account(id=userFromDB['idUser'],accountNumber=userFromDB['numberAccount'], userAgency=userFromDB['agencyUser'], totalBalance=userFromDB['totalbalance'])
                return User(userFromDB['idUser'], userFromDB['nameUser'], userFromDB['cpfUser'], "fooPassword", userFromDB['birthdateUser'], userFromDB['genreUser'], account=account, applicationProfile=userFromDB['profileUser'])
            else:
                logging.info(f'Usuário com cpf: {cpf} não encontrado!')
                return None
        except mariadb.Error as e:
            logging.error(e)
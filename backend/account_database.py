import logging
import mariadb
from .user import User
from .account import Account

class AccountDatabase:
    def __init__(self, connection):
        self.db = connection
        logging.info('Repositório de contas inicializado!')

    def create(self, userId, manager_agency_id):
        cursor = self.db.cursor()
        query = """
            INSERT INTO taccount (numberAccount, totalbalance, idAccountUser, agencyUser) values (next value for account_number, 0, ?,?);
        """
        parameters = (userId,manager_agency_id )
        cursor.execute(query, parameters)
        self.db.commit()

    def updateBalanceByAccountNumber(self, balance, accountNumber):
        cursor = self.db.cursor()
        query = "UPDATE taccount SET totalbalance = ? WHERE numberAccount = ?"
        parameters = (balance, accountNumber)
        try:
            cursor.execute(query, parameters)
            self.db.commit()
        except mariadb.Error as e:
            logging.error(e)


    def getBalanceByAccountNumber(self, account_number):
        cursor = self.db.cursor(dictionary=True)
        query = """select * from taccount t
                where numberAccount = ?;"""
        parameters = (account_number,)
        try:
            cursor.execute(query, parameters)
            value= cursor.fetchone()
            return value['totalbalance']
        except mariadb.Error as e:
            logging.error(e)

    def getAccountTypeByAccountNumber(self, account_number):
        cursor = self.db.cursor(dictionary=True)
        query = """select * from taccount t
                where numberAccount = ?;"""
        parameters = (account_number,)
        try:
            cursor.execute(query, parameters)
            value= cursor.fetchone()
            return value['account_type']
        except mariadb.Error as e:
            logging.error(e)

    def inactivate_account(self, accountNumber):
        cursor = self.db.cursor()
        query = "UPDATE taccount SET is_active = false WHERE numberAccount = ?"
        parameters = (accountNumber,)
        try:
            cursor.execute(query, parameters)
            self.db.commit()
        except mariadb.Error as e:
            logging.error(e)

    def activate_account(self, accountNumber):
        cursor = self.db.cursor()
        query = "UPDATE taccount SET is_active = true WHERE numberAccount = ?"
        parameters = (accountNumber,)
        try:
            cursor.execute(query, parameters)
            self.db.commit()
        except mariadb.Error as e:
            logging.error(e)

    def findByAccount(self, accountForTransfer, agencyForTransfer):
        cursor = self.db.cursor(dictionary=True)
        query = """
        SELECT USR.*, ACCOUNT.* 
        FROM tuser AS USR INNER JOIN taccount AS ACCOUNT ON idUser = idAccountUser 
        WHERE numberAccount = ? and agencyUser = ?
        """
        parameters = (accountForTransfer, agencyForTransfer,)
        try:
            cursor.execute(query, parameters)
            accountFromDB = cursor.fetchone()
            if accountFromDB:
                account = Account(id=accountFromDB['idAccount'],accountNumber=accountFromDB['numberAccount'], userAgency=accountFromDB['agencyUser'], totalBalance=accountFromDB['totalbalance'], typeAccount=accountFromDB['account_type'])
                return User(accountFromDB['idUser'], accountFromDB['nameUser'], accountFromDB['cpfUser'], "fooPassword", accountFromDB['birthdateUser'], accountFromDB['genreUser'], account=account)
            else:
                logging.info(f'Usuário não encontrado!')
                return None
        except mariadb.Error as e:
            logging.error(e)

    def getBalanceByIdAccount(self, id_account):
        cursor = self.db.cursor(dictionary=True)
        query = """select * from taccount t
                where idAccount = ?;"""
        parameters = (id_account,)
        try:
            cursor.execute(query, parameters)
            value= cursor.fetchone()
            return value['totalbalance']
        except mariadb.Error as e:
            logging.error(e)

    def updateBalanceByIdAccount(self, balance, id_account):
        cursor = self.db.cursor()
        query = "UPDATE taccount SET totalbalance = ? WHERE idAccount = ?"
        parameters = (balance, id_account)
        try:
            cursor.execute(query, parameters)
            self.db.commit()
        except mariadb.Error as e:
            logging.error(e)
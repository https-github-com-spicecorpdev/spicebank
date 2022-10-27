import logging
import mariadb

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
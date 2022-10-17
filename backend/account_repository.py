import logging
import mariadb

class AccountRepository:
    def __init__(self, connection):
        self.db = connection
        logging.info('Repositório de contas inicializado!')

    def create(self, userId):
        cursor = self.db.cursor()
        query = """
            INSERT INTO taccount (numberAccount, totalbalance, idAccountUser, statusAccount, solicitacao) values (next value for account_number, 0, ?, 0, 'pendente');
        """
        parameters = (userId, )
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

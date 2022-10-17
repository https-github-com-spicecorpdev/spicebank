import logging
import mariadb
from .statement import Statement

class StatementRepository:
    def __init__(self, connection):
        self.db = connection
        logging.info('Repositório de extratos inicializado!')

    def save(self, statement):
        cursor = self.db.cursor()
        query = "INSERT INTO bank_statement (id_user, balance, deposit, withdraw, date, operation) values (?, ?, ?, ?, ?, ?)"
        parameters = (statement.userId, statement.balance, statement.deposit, statement.withdraw, statement.date, statement.operation)
        try:
            cursor.execute(query, parameters)
            self.db.commit()
        except mariadb.Error as e:
            logging.error(e)

    def findByUserId(self, userId):
        cursor = self.db.cursor(dictionary=True)
        query = """
            SELECT *
            FROM bank_statement
            WHERE id_user = ?
        """
        parameters = (userId,)
        try:
            cursor.execute(query, parameters)
            statementsFromDB = cursor.fetchall()
            if statementsFromDB:
                return statementsFromDB
            else:
                logging.info(f'Nenhum dado encontrado no extrato!')
                return []
        except mariadb.Error as e:
            logging.error(e)

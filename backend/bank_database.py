import logging
import mariadb
from .manager import Manager

class BankDatabase:
    def __init__(self, connection):
        self.db = connection
        logging.info('Repositório de gerente de agência inicializado!')

    def update_bank_balance(self, bank_id, value):
        cursor = self.db.cursor()
        query = "SELECT capital FROM bank WHERE id = ?"
        parameters = (bank_id,)
        cursor.execute(query, parameters)
        bankBalance = float(cursor.fetchone()[0])
        newBankBalance = bankBalance + value
        query = "UPDATE bank SET capital = ? WHERE id = ?"
        parameters = (newBankBalance, bank_id,)
        try:
            cursor.execute(query, parameters)
            self.db.commit()
        except mariadb.Error as e:
            logging.error(e)

    def withdraw_bank_balance_by_id(self, bank_id, value):
        cursor = self.db.cursor()
        query = "SELECT capital FROM bank WHERE id = ?"
        parameters = (bank_id,)
        cursor.execute(query, parameters)
        bankBalance = float(cursor.fetchone()[0])
        newBankBalance = bankBalance - value
        query = "UPDATE bank SET capital = ? WHERE id = ?"
        parameters = (newBankBalance, bank_id,)
        try:
            cursor.execute(query, parameters)
            self.db.commit()
        except mariadb.Error as e:
            logging.error(e)
import logging
import mariadb
import time
from .datetime import DateTime

class DateTimeDatabase:
    def __init__(self, connection):
        self.db = connection
        logging.info('Data inicializada!')

    def today(self):
        cursor = self.db.cursor(dictionary=True)
        query = """
            select * from datesystem;
        """
        cursor.execute(query)
        today = cursor.fetchone()
        logging.info(f'{today}')
        today = today['datetimeSystem']
        if today == None:
            logging.info(f'Nenhuma horário encontrado!')
            today = time.strftime('%d/%m/%Y %H:%M:%S')
            return today
        else:
            #return today.iddateSystem
            #today = today['datetimeSystem']
            logging.info(f'{today}')
            return today


    def alterday(self, dataEscolhida):
        cursor = self.db.cursor(dictionary=True)
        query = """
            update datesystem set datetimeSystem = ? where iddateSystem = 1;
        """
        parameters = (dataEscolhida,)
        try:
            cursor.execute(query, parameters)
            self.db.commit()
        except mariadb.Error as e:
            logging.error(e)

    def backday(self):
        cursor = self.db.cursor(dictionary=True)
        query = """
            update datesystem set datetimeSystem = 0 where iddateSystem = 2;
        """
        try:
            cursor.execute(query)
            self.db.commit()
        except mariadb.Error as e:
            logging.error(e)
import logging
import mariadb

class AgencyDatabase:
    def __init__(self, connection):
        self.db = connection
        logging.info('Repositório de usuários inicializado!')

    def find_all_agencies(self):
        cursor = self.db.cursor(dictionary=True)
        query = """
            select a.*, m.*, t.* from agency a
            inner join manager m on m.work_agency_id = a.id
            INNER join tuser t on t.idUser = m.id_user
            where m.profile_user = 2
        """
        cursor.execute(query)
        agencies = cursor.fetchall()
        if agencies:
            return agencies
        else:
            logging.info(f'Nenhuma agência encontrada!')
            return []

    def create_agency(self, bank_id):
        cursor = self.db.cursor(dictionary=True)
        query = """
            INSERT INTO agency (`number`, bank_id)
            VALUES(nextval(agency_number), ?);
        """
        parameters = (bank_id,)
        try:
            cursor.execute(query, parameters)
            self.db.commit()
            return cursor.lastrowid
        except mariadb.Error as e:
            logging.error(e)
            return None
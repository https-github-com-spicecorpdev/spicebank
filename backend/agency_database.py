import logging
import mariadb

class AgencyDatabase:
    def __init__(self, connection):
        self.db = connection
        logging.info('Repositório de usuários inicializado!')

    def find_all_agencies(self):
        cursor = self.db.cursor(dictionary=True)
        query = """
            select a.`number`, m.*, u.* from agency a
            right join manager m on a.id = m.work_agency_id 
            left join tuser u on m.id_user = u.idUser 
            where m.work_agency_id <> ''
            UNION 
            select a.`number`, m.*, u.* from agency a 
            left join manager m on a.id = m.work_agency_id 
            left join tuser u on m.id_user = u.idUser ;
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

    def find_empty_agencies(self):
        cursor = self.db.cursor(dictionary=True)
        query = """
            select a.* from agency a 
            left join manager m on a.id = m.work_agency_id
            where m.id is null ;
        """
        cursor.execute(query)
        agencies = cursor.fetchall()
        if agencies:
            return agencies
        else:
            logging.info(f'Nenhuma agência encontrada!')
            return []
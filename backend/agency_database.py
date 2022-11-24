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
            and a.`number` <> 1
            UNION 
            select a.`number`, m.*, u.* from agency a 
            left join manager m on a.id = m.work_agency_id 
            left join tuser u on m.id_user = u.idUser
            where a.`number` <> 1
            ORDER BY `number`;
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

    def find_next_agency_id_by_amount_users(self):
        cursor = self.db.cursor(dictionary=True)
        query = """
            select a.id, a.`number`, t.agencyUser, count(t.agencyUser) "amount of agencies" from agency a
            left join taccount t  on t.agencyUser  = a.id 
            where a.id <> 1
            group by a.id, a.`number`, t.agencyUser
            ORDER BY count(t.agencyUser) asc LIMIT 1;
        """
        cursor.execute(query)
        agency = cursor.fetchone()
        if agency:
            return agency['id']
        else:
            logging.info(f'Nenhuma agência encontrada!')
            return None
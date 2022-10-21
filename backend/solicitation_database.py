import logging
import mariadb

class SolicitationDatabase:
    def __init__(self, connection):
        self.db = connection
        logging.info('Repositório de solicitações inicializado!')

    def find_by_work_agency_id(self, work_agency_id):
        cursor = self.db.cursor(dictionary=True)
        query = """
            SELECT USR.*, ACCOUNT.*, s.*
       FROM tuser AS USR left JOIN taccount AS ACCOUNT ON USR.idUser = ACCOUNT.idAccountUser
       inner join solicitation s on USR.idUser = s.id_user 
       where  s.status = 'Pendente' and (ACCOUNT.agencyUser = ? or solicitation_type in ('Abertura de conta', 'Encerrar conta'));
        """
        parameters = (work_agency_id,)
        try:
            cursor.execute(query, parameters)
            solicitations_from_db = cursor.fetchall()
            if solicitations_from_db:
                return solicitations_from_db
            else:
                logging.info(f'Nenhuma solicitação encontrada!')
                return []
        except mariadb.Error as e:
            logging.error(e)

    def update_status_by_id(self, id, status):
        cursor = self.db.cursor()
        query = """
        UPDATE solicitation SET status = ? WHERE id = ?
        """
        parameters = (status, id,)
        try:
            cursor.execute(query, parameters)
            self.db.commit()
        except mariadb.Error as e:
            logging.error(e)
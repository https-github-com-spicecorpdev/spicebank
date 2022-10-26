import logging
import mariadb
from .solicitation import DepositSolicitation

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

    def open_account_solicitation(self, user_id, solicitation_type, account_type='Conta Corrente'):
        cursor = self.db.cursor()
        solicitation_query = """
            INSERT INTO solicitation (id_user, status, solicitation_type) VALUES(?, 'Pendente', ?)
        """
        account_solicitation_query = """
            INSERT INTO account_solicitation (id_solicitation, account_type) VALUES(?, ?)
        """
        solicitation_parameters = (user_id, solicitation_type,)

        try:
            cursor.execute(solicitation_query, solicitation_parameters)
            self.db.commit()
            account_solicitation_parameters = (cursor.lastrowid, account_type)
            cursor.execute(account_solicitation_query, account_solicitation_parameters)
            self.db.commit()
            
            logging.info('Solicitação de abertura de conta concluída')
        except mariadb.Error as e:
            logging.error(e)

    def open_deposit_solicitation(self, user_id, account_number, solicitation_type, value):
        cursor = self.db.cursor()
        solicitation_query = """
            INSERT INTO solicitation (id_user, status, solicitation_type) VALUES(?, 'Pendente', ?)
        """
        deposit_solicitation_query = """
            INSERT INTO deposit_solicitation (id_solicitation, account_number, deposit_value) VALUES(?, ?, ?)
        """
        solicitation_parameters = (user_id, solicitation_type,)

        try:
            cursor.execute(solicitation_query, solicitation_parameters)
            self.db.commit()
            deposit_solicitation_parameters = (cursor.lastrowid, account_number, value)
            cursor.execute(deposit_solicitation_query, deposit_solicitation_parameters)
            self.db.commit()
            
            logging.info('Solicitação de abertura de conta concluída')
        except mariadb.Error as e:
            logging.error(e)

    def find_deposit_solicitation_by_id_solicitation(self,id_solicitation):
        cursor = self.db.cursor(dictionary=True)
        query = """select * from deposit_solicitation ds 
                   where id_solicitation = ?;"""
        parameters = (id_solicitation,)
        try:
            cursor.execute(query, parameters)
            result= cursor.fetchone()
            if result:
                return DepositSolicitation(id_solicitation, result['account_number'],result ['deposit_value'],id=result['id'])
            else:
                logging.info (f'Solicitação com o id: {id_solicitation} não encontrado!')
                return None
        except mariadb.Error as e:
            logging.error(e)
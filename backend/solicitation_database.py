import logging
import mariadb
from .solicitation import CloseAccountSolicitation, DepositSolicitation, UpdateDataSolicitation, SimpleSolicitation


class SolicitationDatabase:
    def __init__(self, connection):
        self.db = connection
        logging.info('Repositório de solicitações inicializado!')

    def find_by_id(self, id):
        cursor = self.db.cursor(dictionary=True)
        query = """
            SELECT *
            FROM solicitation 
            WHERE id = ?
        """
        parameters = (id,)
        try:
            cursor.execute(query, parameters)
            result = cursor.fetchone()
            if result:
                solicitation = SimpleSolicitation(result['id_user'], result['status'], result['solicitation_type'], result['created_time'], result['updated_time'], id=result['id'])
                return solicitation
            else:
                logging.info(f'Nenhuma solicitação com id {id} encontrado!')
                return None
        except mariadb.Error as e:
            logging.error(e)

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

    def find_solicitation_id_by_user_id_and_solicitation_type(self,user_id, type):
        cursor = self.db.cursor(dictionary=True)
        query = """select * from solicitation 
                   where id_user = ?
                   AND solicitation_type = ?;"""
        parameters = (user_id, type,)
        try:
            cursor.execute(query, parameters)
            result= cursor.fetchone()
            if result:
                return result['id']
            else:
                logging.info (f'Solicitação com o user_id: {user_id} não encontrado!')
                return None
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
            logging.info('Solicitação de depósito realizada!')
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

    def find_update_user_solicitation_by_id_solicitation(self,id_solicitation, user_id):
        cursor = self.db.cursor(dictionary=True)
        query = """select * from update_user_solicitation  
                   where id_solicitation = ?;"""
        parameters = (id_solicitation,)
        try:
            cursor.execute(query, parameters)
            result= cursor.fetchone()
            if result:
                logging.info(f'{result["name"]}, {result ["road"]}')
                return UpdateDataSolicitation(result['name'], result['road'], result['number_house'], result['district'], result['cep'], result['city'], result['state'], result['genre'],id=result['id'], id_solicitation=result['id_solicitation'], user_id= user_id)    
            else:
                logging.info (f'Solicitação com o id: {id_solicitation} não encontrado!')
                return None
        except mariadb.Error as e:
            logging.error(e)

    def open_update_data_solicitation(self,user_id,solicitation ):
        cursor = self.db.cursor()
        solicitation_query = """
            INSERT INTO solicitation (id_user, status, solicitation_type) VALUES(?, 'Pendente', ?)
        """
        update_data_solicitation_query = """
            INSERT INTO update_user_solicitation
            (id_solicitation, name, road, number_house, district, cep, city, state, genre)
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);
        """
        solicitation_parameters = (user_id,'Alteração de dados cadastrais' ,)

        try:
            cursor.execute(solicitation_query, solicitation_parameters)
            self.db.commit()
            update_data_solicitation_parameters = (cursor.lastrowid, solicitation.name, solicitation.road, solicitation.number_house, solicitation.district, solicitation.cep, solicitation.city, solicitation.state, solicitation.genre)
            cursor.execute(update_data_solicitation_query, update_data_solicitation_parameters)
            self.db.commit()
            logging.info('Solicitação de atualização dos dados cadastrais criada!')
        except mariadb.Error as e:
            logging.error(e)

    def find_close_account_solicitation_by_id_solicitation(self,id_solicitation, user_id):
        cursor = self.db.cursor(dictionary=True)
        query = """select * from account_close_solicitation 
                   where id_solicitation = ?;"""
        parameters = (id_solicitation,)
        try:
            cursor.execute(query, parameters)
            result= cursor.fetchone()
            if result:
                logging.info(f'{result["name"]}, {result ["road"]}')
                return CloseAccountSolicitation(result['id_account'], result['name'], result['cpf'], result['birthdate'], result['road'], result['number_house'], result['district'], result['cep'], result['city'], result['state'], result['genre'],id=result['id'], id_solicitation=result['id_solicitation'], user_id= user_id)
            else:
                logging.info (f'Solicitação com o id: {id_solicitation} não encontrado!')
                return None
        except mariadb.Error as e:
            logging.error(e)

    def open_close_account_solicitation(self, user_id, solicitation):
        cursor = self.db.cursor()
        solicitation_query = """
            INSERT INTO solicitation (id_user, status, solicitation_type) VALUES(?, 'Pendente', ?)
        """
        close_account_solicitation_query = """
            INSERT INTO account_close_solicitation
            (id_solicitation, id_account, name, cpf, birthdate, road, number_house, district, cep, city, state, genre)
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """
        solicitation_parameters = (user_id, 'Encerrar conta',)
        try:
            cursor.execute(solicitation_query, solicitation_parameters)
            self.db.commit()
            close_account_solicitation_parameters = (cursor.lastrowid, solicitation.id_account, solicitation.name, solicitation.cpf, solicitation.birthdate, solicitation.road, solicitation.number_house, solicitation.district, solicitation.cep, solicitation.city, solicitation.state, solicitation.genre,)
            cursor.execute(close_account_solicitation_query, close_account_solicitation_parameters)
            self.db.commit()
            logging.info('Solicitação de encerramento de conta criada!')
        except mariadb.Error as e:
            logging.error(e)

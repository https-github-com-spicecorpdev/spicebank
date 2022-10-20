import logging
import mariadb
from .manager import Manager

class ManagerDatabase:
    def __init__(self, connection):
        self.db = connection
        logging.info('Repositório de gerente de agência inicializado!')
    
    def findById(self, id):
        cursor = self.db.cursor(dictionary=True)
        query="""
            SELECT TUSER.*, MANAGER.* 
            from manager as MANAGER 
            INNER JOIN tuser as TUSER ON MANAGER.id_user = TUSER.idUser
            WHERE MANAGER.id = ?;
        """
        parameters = (id,)
        cursor.execute(query, parameters) 
        managerFromDB = cursor.fetchone()
        if managerFromDB:
           return Manager(managerFromDB['nameUser'], managerFromDB['cpfUser'], managerFromDB['passwordUser'], managerFromDB['birthdateUser'], managerFromDB['genreUser'], managerFromDB['registration_number'], managerFromDB['work_agency_id'],managerFromDB['profile_user'], userId=managerFromDB['idUser'], managerId=managerFromDB['id'])
        else:
            logging.info(f'Gerente de Agência com o id: {id} não encontrado!')
            return None

    def findByRegistrationNumberAndPassword(self, registrationNumber, password ):
        cursor = self.db.cursor(dictionary=True)
        query="""
            SELECT TUSER.*, MANAGER.* 
            from manager as MANAGER 
            INNER JOIN tuser as TUSER ON MANAGER.id_user = TUSER.idUser
            WHERE MANAGER.registration_number = ? and TUSER.passwordUser = ?;
        """
        parameters = (registrationNumber, password,)
        cursor.execute(query, parameters) 
        managerFromDB = cursor.fetchone()
        if managerFromDB:
           return Manager(managerFromDB['nameUser'], managerFromDB['cpfUser'], managerFromDB['passwordUser'], managerFromDB['birthdateUser'], managerFromDB['genreUser'], managerFromDB['registration_number'], managerFromDB['work_agency_id'], managerFromDB['profile_user'], userId=managerFromDB['idUser'], managerId=managerFromDB['id'])
        else:
            logging.info(f'Gerente de Agência com matricula : {registrationNumber} não encontrada!')
            return None

    def find_by_user_id(self, user_id):
        cursor=self.db.cursor(dictionary=True)
        query= """
        SELECT TUSER.*, MANAGER.*
        FROM manager as  MANAGER
        INNER JOIN tuser as TUSER ON MANAGER.id_user = TUSER.idUser WHERE TUSER.idUser = ?;
        """
        parameters = (user_id, )
        cursor.execute(query, parameters)
        manager_from_db = cursor.fetchone()
        if manager_from_db:
            return Manager(manager_from_db['nameUser'], manager_from_db['cpfUser'], manager_from_db['passwordUser'], manager_from_db['birthdateUser'], manager_from_db['genreUser'], manager_from_db['registration_number'], manager_from_db['work_agency_id'], manager_from_db['profile_user'], userId=manager_from_db['idUser'], managerId=manager_from_db['id'])
        else:
            logging.info(f'Gerente de Agência com o id: {user_id} não encontrado!')
            return None

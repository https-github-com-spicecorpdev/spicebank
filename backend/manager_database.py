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
           return Manager(managerFromDB['nameUser'], managerFromDB['cpfUser'], managerFromDB['passwordUser'], managerFromDB['birthdateUser'], managerFromDB['genreUser'], managerFromDB['registration_number'], managerFromDB['work_agency_id'], userId=managerFromDB['idUser'])
        else:
            logging.info(f'Gerente de Agência com o id: {id} não encontrado!')
            return None
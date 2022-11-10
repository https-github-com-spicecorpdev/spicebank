import logging
import mariadb
from .manager import Manager
from .account import Account
from .address import Address

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
            address = Address(manager_from_db['roadUser'], manager_from_db['numberHouseUser'], manager_from_db['districtUser'], manager_from_db['cityUser'], manager_from_db['stateUser'], manager_from_db['cepUser'])
            return Manager(manager_from_db['nameUser'], manager_from_db['cpfUser'], manager_from_db['passwordUser'], manager_from_db['birthdateUser'], manager_from_db['genreUser'], manager_from_db['registration_number'], manager_from_db['work_agency_id'], manager_from_db['profile_user'], userId=manager_from_db['idUser'], managerId=manager_from_db['id'], address=address)
        else:
            logging.info(f'Gerente de Agência com o id: {user_id} não encontrado!')
            return None

    def find_all_agency_manager(self):
        cursor=self.db.cursor(dictionary=True)
        query = """
            SELECT m.*, a.*, u.*
            FROM manager m
            INNER JOIN agency a on a.id = m.work_agency_id
            INNER JOIN tuser u on u.idUser = m.id_user 
            where m.profile_user = 2;
        """
        cursor.execute(query,)
        manager_from_db = cursor.fetchall()
        if manager_from_db:
            return manager_from_db
        else:
            logging.info(f'Nenhum gerente de agência encontrado')
            return None

    def find_all_agency_manager_without_work_agency(self):
        cursor=self.db.cursor(dictionary=True)
        query = """
            SELECT m.id as manager_id, m.*, a.*, u.*
            FROM manager m
            left JOIN agency a on a.id = m.work_agency_id
            INNER JOIN tuser u on u.idUser = m.id_user 
            where m.profile_user = 2 and a.id is null;
        """
        cursor.execute(query,)
        manager_from_db = cursor.fetchall()
        if manager_from_db:
            return manager_from_db
        else:
            logging.info(f'Nenhum gerente de agência encontrado')
            return []

    def update_work_agency_id_by_maganer_id(self, work_agency_id, manager_id):
        cursor = self.db.cursor()
        query = """
        UPDATE manager
        SET work_agency_id = ?
        WHERE id = ?;
        """
        parameters = (work_agency_id, manager_id, )
        try:
            cursor.execute(query, parameters)
            self.db.commit()
        except mariadb.Error as e:
            logging.error(e)

    def save_user_manager(self, user):
        cursor = self.db.cursor()
        user_query = """
            INSERT INTO tuser (nameUser, cpfUser, roadUser, numberHouseUser, districtUser, cepUser, cityUser, stateUser, birthdateUser, genreUser, passwordUser) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """
        manager_query = """
            INSERT INTO manager
            (id_user, registration_number, profile_user, bank_id)
            VALUES(?, NEXTVAL(manager_registration_number), 2, 1);
        """
        address = user.address
        user_parameters = (user.name, user.cpf, address.road, address.numberHouse, address.district, address.cep, address.city, address.state, user.birthDate, user.gender, user.password,)
        try:
            cursor.execute(user_query, user_parameters)
            self.db.commit()
            manager_parameters = (cursor.lastrowid,)
            cursor.execute(manager_query, manager_parameters)
            self.db.commit()
        except mariadb.Error as e:
            logging.error(e)
        return self.findById(user.id)
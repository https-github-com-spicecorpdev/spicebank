import logging
import mariadb
from .user import User
from .account import Account
from .address import Address
from .solicitation import Solicitation
from .manager import Manager

class UserDatabase:
    def __init__(self, connection):
        self.db = connection
        logging.info('Repositório de usuários inicializado!')

    def findById(self, id):
        cursor = self.db.cursor(dictionary=True)
        query = """
        SELECT USR.*, ACCOUNT.* 
       FROM tuser AS USR left JOIN taccount AS ACCOUNT ON USR.idUser = ACCOUNT.idAccountUser
       WHERE USR.idUser = ?
       union    
        SELECT USR.*, ACCOUNT.* 
       FROM tuser AS USR right JOIN taccount AS ACCOUNT ON USR.idUser = ACCOUNT.idAccountUser
       WHERE USR.idUser = ?;
        """
        parameters = (id,id,)
        cursor.execute(query, parameters) 
        userFromDB = cursor.fetchone()
        if userFromDB:
            address = Address(userFromDB['roadUser'], userFromDB['numberHouseUser'], userFromDB['districtUser'], userFromDB['cityUser'], userFromDB['stateUser'], userFromDB['cepUser'])
            account = Account(id=userFromDB['idAccount'],accountNumber=userFromDB['numberAccount'], userAgency=userFromDB['agencyUser'], totalBalance=userFromDB['totalbalance'], typeAccount=userFromDB['account_type'])
            return User(userFromDB['idUser'], userFromDB['nameUser'], userFromDB['cpfUser'], userFromDB['passwordUser'], userFromDB['birthdateUser'], userFromDB['genreUser'], account=account, address=address)
        else:
            logging.info(f'Usuário com o id: {id} não encontrado!')
            return None

    def find_by_account_id(self, account_id):
        cursor = self.db.cursor(dictionary=True)
        query = """
        SELECT USR.*, ACCOUNT.* 
       FROM tuser AS USR left JOIN taccount AS ACCOUNT ON USR.idUser = ACCOUNT.idAccountUser
       WHERE ACCOUNT.idAccount = ?
       union    
        SELECT USR.*, ACCOUNT.* 
       FROM tuser AS USR right JOIN taccount AS ACCOUNT ON USR.idUser = ACCOUNT.idAccountUser
       WHERE ACCOUNT.idAccount = ?;
        """
        parameters = (account_id, account_id,)
        cursor.execute(query, parameters) 
        userFromDB = cursor.fetchone()
        if userFromDB:
            address = Address(userFromDB['roadUser'], userFromDB['numberHouseUser'], userFromDB['districtUser'], userFromDB['cityUser'], userFromDB['stateUser'], userFromDB['cepUser'])
            account = Account(id=userFromDB['idAccount'],accountNumber=userFromDB['numberAccount'], userAgency=userFromDB['agencyUser'], totalBalance=userFromDB['totalbalance'], typeAccount=userFromDB['account_type'])
            return User(userFromDB['idUser'], userFromDB['nameUser'], userFromDB['cpfUser'], userFromDB['passwordUser'], userFromDB['birthdateUser'], userFromDB['genreUser'], account=account, address=address)
        else:
            logging.info(f'Usuário com o id: {id} não encontrado!')
            return None
    
    def findById_and_id_solicitation(self, id):
        cursor = self.db.cursor(dictionary=True)
        query = """
            select account.*, s.*, u.*,a.* from account_solicitation account 
            inner join solicitation s on s.id  = account.id_solicitation
            inner join taccount a on a.idAccount = account.account_id 
            inner join tuser u on u.idUser = a.idAccountUser 
            where account.id_solicitation = ? ;
        """
        parameters = (id,)
        cursor.execute(query, parameters) 
        userFromDB = cursor.fetchone()
        if userFromDB:
            address = Address(userFromDB['roadUser'], userFromDB['numberHouseUser'], userFromDB['districtUser'], userFromDB['cityUser'], userFromDB['stateUser'], userFromDB['cepUser'])
            account = Account(id=userFromDB['idUser'],accountNumber=userFromDB['numberAccount'], userAgency=userFromDB['agencyUser'], totalBalance=userFromDB['totalbalance'], typeAccount=userFromDB['account_type'])
            return User(userFromDB['idUser'], userFromDB['nameUser'], userFromDB['cpfUser'], userFromDB['passwordUser'], userFromDB['birthdateUser'], userFromDB['genreUser'], account=account, address=address)
        else:
            logging.info(f'Usuário com o id: {id} não encontrado!')
            return None

    def findByIdAndNumberAccount(self, id):
        cursor = self.db.cursor(dictionary=True)
        query = """
        SELECT USR.*, ACCOUNT.* 
       FROM tuser AS USR left JOIN taccount AS ACCOUNT ON USR.idUser = ACCOUNT.idAccountUser
       WHERE ACCOUNT.numberAccount = ?
       union    
        SELECT USR.*, ACCOUNT.* 
       FROM tuser AS USR right JOIN taccount AS ACCOUNT ON USR.idUser = ACCOUNT.idAccountUser
       WHERE ACCOUNT.numberAccount = ? ;
        """
        parameters = (id,id,)
        cursor.execute(query, parameters) 
        userFromDB = cursor.fetchone()
        if userFromDB:
            address = Address(userFromDB['roadUser'], userFromDB['numberHouseUser'], userFromDB['districtUser'], userFromDB['cityUser'], userFromDB['stateUser'], userFromDB['cepUser'])
            account = Account(id=userFromDB['idUser'],accountNumber=userFromDB['numberAccount'], userAgency=userFromDB['agencyUser'], totalBalance=userFromDB['totalbalance'], typeAccount=userFromDB['account_type'])
            return User(userFromDB['idUser'], userFromDB['nameUser'], userFromDB['cpfUser'], userFromDB['passwordUser'], userFromDB['birthdateUser'], userFromDB['genreUser'], account=account, address=address)
        else:
            logging.info(f'Usuário com o id: {id} não encontrado!')
            return None

    def findByIdaccount(self, idAccount):
        cursor = self.db.cursor(dictionary=True)
        query = """
         SELECT USR.*, ACCOUNT.* 
            FROM tuser AS USR left JOIN taccount AS ACCOUNT ON USR.idUser = ACCOUNT.idAccountUser
            WHERE ACCOUNT.idAccount  = ?
            union    
                SELECT USR.*, ACCOUNT.* 
            FROM tuser AS USR right JOIN taccount AS ACCOUNT ON USR.idUser = ACCOUNT.idAccountUser
            WHERE ACCOUNT.idAccount  = ?;
        """
        parameters = (idAccount,idAccount,)
        cursor.execute(query, parameters) 
        userFromDB = cursor.fetchone()
        if userFromDB:
            address = Address(userFromDB['roadUser'], userFromDB['numberHouseUser'], userFromDB['districtUser'], userFromDB['cityUser'], userFromDB['stateUser'], userFromDB['cepUser'])
            account = Account(id=userFromDB['idUser'],accountNumber=userFromDB['numberAccount'], userAgency=userFromDB['agencyUser'], totalBalance=userFromDB['totalbalance'], typeAccount=userFromDB['account_type'])
            return User(userFromDB['idUser'], userFromDB['nameUser'], userFromDB['cpfUser'], userFromDB['passwordUser'], userFromDB['birthdateUser'], userFromDB['genreUser'], account=account, address=address)
        else:
            logging.info(f'Usuário com o id: {id} não encontrado!')
            return None

    def findByManagerId(self, id):
        cursor = self.db.cursor(dictionary=True)
        query = """
        SELECT USR.*,  MANAGER.* 
       FROM tuser AS USR left JOIN manager AS MANAGER ON USR.idUser = MANAGER.id_user
       WHERE USR.idUser = ?
       union    
        SELECT USR.*, MANAGER.*  
       FROM tuser AS USR right JOIN taccount AS MANAGER ON USR.idUser = MANAGER.id_user
       WHERE USR.idUser = ?;
        """
        parameters = (id,id,)
        cursor.execute(query, parameters) 
        userFromDB = cursor.fetchone()
        if userFromDB:
            address = Address(userFromDB['roadUser'], userFromDB['numberHouseUser'], userFromDB['districtUser'], userFromDB['cityUser'], userFromDB['stateUser'], userFromDB['cepUser'])
            account = Account(id=userFromDB['idUser'],accountNumber=userFromDB['numberAccount'], userAgency=userFromDB['agencyUser'], totalBalance=userFromDB['totalbalance'], typeAccount=userFromDB['account_type'])
            return Manager(userFromDB['idUser'], userFromDB['nameUser'], userFromDB['cpfUser'], userFromDB['passwordUser'], userFromDB['birthdateUser'], userFromDB['genreUser'], userFromDB['registration_number'], userFromDB['work_agency_id'], userFromDB['profile_user'], account=account, address=address)
        else:
            logging.info(f'Usuário com o id: {id} não encontrado!')
            return None

    def find_all_users(self, manager): 
        cursor = self.db.cursor(dictionary=True)
        if manager.is_general_manager():
            query = """
                SELECT USR.*, ACCOUNT.* 
                FROM tuser AS USR left 
                JOIN taccount AS ACCOUNT ON USR.idUser = ACCOUNT.idAccountUser
                where ACCOUNT.is_active = true;
            """
            parameters = ()
        else:
            query = """
            SELECT USR.*, ACCOUNT.* 
            FROM tuser AS USR left 
            JOIN taccount AS ACCOUNT ON USR.idUser = ACCOUNT.idAccountUser 
            where ACCOUNT.agencyUser = ? and ACCOUNT.is_active = true;
        """
            parameters = (manager.workAgency,)
        try:
            cursor.execute(query, parameters)
            user_from_db = cursor.fetchall()
            if user_from_db:
                return user_from_db
            else:
                logging.info(f'Nenhum usuário encontrado')
                return []
        except mariadb.Error as e:
            logging.error(e)

    # def findByAgencyAccountAndPassword(self, agency, account, password):
    #     cursor = self.db.cursor(dictionary=True)
    #     query = """
    #         SELECT USR.*, ACCOUNT.* 
    #         FROM tuser AS USR INNER JOIN taccount AS ACCOUNT ON USR.idUser = ACCOUNT.idAccountUser
    #         WHERE ACCOUNT.agencyUser = ?
    #         AND ACCOUNT.numberAccount = ?
    #         AND USR.passwordUser = ?
    #         AND ACCOUNT.is_active = true 
    #     """
    #     parameters = (agency, account, password)
    #     cursor.execute(query, parameters)
    #     userFromDB = cursor.fetchone()
    #     if userFromDB:
    #         user =  User(userFromDB['idUser'], userFromDB['nameUser'], userFromDB['cpfUser'], password, userFromDB['birthdateUser'], userFromDB['genreUser'])
    #         return Account(id=userFromDB['idUser'],accountNumber=userFromDB['numberAccount'], userAgency=userFromDB['agencyUser'], totalBalance=userFromDB['totalbalance'], typeAccount=userFromDB['account_type'], user=user)
    #     else:
    #         logging.info(f'Usuário não encontrado!')
    #         return None

    def findByAgencyAccountAndPassword(self, agency, account_number, password):
        cursor = self.db.cursor(dictionary=True)
        query = """
            SELECT USR.*, ACCOUNT.* 
            FROM tuser AS USR INNER JOIN taccount AS ACCOUNT ON USR.idUser = ACCOUNT.idAccountUser
            WHERE ACCOUNT.agencyUser = ?
            AND ACCOUNT.numberAccount = ?
            AND USR.passwordUser = ?
            AND ACCOUNT.is_active = true 
        """
        parameters = (agency, account_number, password)
        cursor.execute(query, parameters)
        userFromDB = cursor.fetchone()
        if userFromDB:
            account = Account(id=userFromDB['idAccount'],accountNumber=account_number, userAgency=agency, totalBalance=userFromDB['totalbalance'], typeAccount=userFromDB['account_type'])
            return User(userFromDB['idUser'], userFromDB['nameUser'], userFromDB['cpfUser'], password, userFromDB['birthdateUser'], userFromDB['genreUser'], account=account)
        else:
            logging.info(f'Usuário não encontrado!')
            return None

    def findIdByUser(self, user):
        cursor = self.db.cursor(dictionary=True)
        query = """
            SELECT idUser
            FROM tuser 
            WHERE cpfUser = ? and passwordUser = ?;
        """
        parameters = (user.cpf, user.password, )
        try:
            cursor.execute(query, parameters)
            userIdFromDB = cursor.fetchone()
            if userIdFromDB:
                return userIdFromDB['idUser']
            else:
                return None
        except mariadb.Error as e:
            logging.error(e)

    def save(self, user):
        cursor = self.db.cursor()
        query = """
            INSERT INTO tuser (nameUser, cpfUser, roadUser, numberHouseUser, districtUser, cepUser, cityUser, stateUser, birthdateUser, genreUser, passwordUser) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """
        address = user.address
        parameters = (user.name, user.cpf, address.road, address.numberHouse, address.district, address.cep, address.city, address.state, user.birthDate, user.gender, user.password,)
        try:
            cursor.execute(query, parameters)
            self.db.commit()
        except mariadb.Error as e:
            logging.error(e)
        return self.findIdByUser(user)



    def findSolicitationByCpfAndPassword(self, cpf, password):
        cursor = self.db.cursor(dictionary=True)
        query = """
        SELECT USR.*, ACCOUNT.* , SOLICITATION.*
        FROM tuser AS USR LEFT JOIN taccount AS ACCOUNT ON idUser = idAccountUser 
        INNER JOIN solicitation AS SOLICITATION ON USR.idUser = SOLICITATION.id_user
	    WHERE cpfUser = ? AND passwordUser = ?
        AND SOLICITATION.solicitation_type = 'Abertura de conta'
        """
        parameters = (cpf, password,)

        try:
            cursor.execute(query, parameters)
            userStatus = cursor.fetchone()
            if userStatus:
                return Solicitation(userStatus['nameUser'], cpf, password, userStatus['status'], userStatus['numberAccount'], userStatus['agencyUser'], user_id=userStatus['idUser'])
            else:
                logging.info(f'Solicitação com cpf: {cpf} não encontrada!')
                return None
        except mariadb.Error as e:
            logging.error(e)

    def find_all_accounts_by_cpf_and_password(self, cpf, password):
        cursor = self.db.cursor(dictionary=True)
        query = """
        SELECT USR.*, ACCOUNT.*
        FROM tuser AS USR LEFT JOIN taccount AS ACCOUNT ON idUser = idAccountUser
	    WHERE cpfUser = ? AND passwordUser = ?;
        """
        parameters = (cpf, password,)
        try:
            cursor.execute(query, parameters)
            return cursor.fetchall()
        except mariadb.Error as e:
            logging.error(e)

    def findByCpf(self, cpf):
        cursor = self.db.cursor(dictionary=True)
        query = """
        SELECT USR.*, ACCOUNT.* 
        FROM tuser AS USR INNER JOIN taccount AS ACCOUNT ON idUser = idAccountUser 
        WHERE cpfUser = ?
        """
        parameters = (cpf,)
        try:
            cursor.execute(query, parameters)
            userFromDB = cursor.fetchone()
            if userFromDB:
                account = Account(id=userFromDB['idUser'],accountNumber=userFromDB['numberAccount'], userAgency=userFromDB['agencyUser'], totalBalance=userFromDB['totalbalance'], typeAccount=userFromDB['account_type'])
                return User(userFromDB['idUser'], userFromDB['nameUser'], userFromDB['cpfUser'], "fooPassword", userFromDB['birthdateUser'], userFromDB['genreUser'], account=account)
            else:
                logging.info(f'Usuário com cpf: {cpf} não encontrado!')
                return None
        except mariadb.Error as e:
            logging.error(e)


    def update_by_user_solicitation(self, solicitation):
        cursor = self.db.cursor()
        query = """
        UPDATE tuser
        SET nameUser=?, roadUser=?, numberHouseUser=?, districtUser=?, cepUser=?, cityUser=?, stateUser=?, genreUser=?
        WHERE idUser=?;
        """
        parameters = (solicitation.name, solicitation.road, solicitation.number_house, solicitation.district, solicitation.cep, solicitation.city, solicitation.state, solicitation.genre, solicitation.user_id)
        try:
            cursor.execute(query, parameters)
            self.db.commit()
        except mariadb.Error as e:
            logging.error(e) 

    def update_user_data_by_manager(self, user):
        cursor = self.db.cursor()
        query = """
        UPDATE tuser
        SET nameUser=?, roadUser=?, numberHouseUser=?, districtUser=?, cepUser=?, cityUser=?, stateUser=?, genreUser=?
        WHERE idUser=?;
        """
        address = user.address
        parameters = (user.name, address.road, address.numberHouse, address.district, address.cep, address.city, address.state, user.gender, user.id)
        try:
            cursor.execute(query, parameters)
            self.db.commit()
        except mariadb.Error as e:
            logging.error(e)
        return self.findIdByUser(user)

    def find_taxa(self, tipotaxa):
        cursor = self.db.cursor(dictionary=True)
        query = """
            select * from taxas
            where tiptaxa = ?
        """
        parameters = (tipotaxa,)
        try:
            cursor.execute(query, parameters)
            result= cursor.fetchone()
            if result:
                return result['valortaxa']
            else:
                logging.info (f'Taxa não encontrada!')
                return None
        except mariadb.Error as e:
            logging.error(e)
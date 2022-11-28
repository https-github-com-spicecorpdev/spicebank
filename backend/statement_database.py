import logging
import mariadb

class StatementDatabase:
    def __init__(self, connection):
        self.db = connection
        logging.info('Repositório de extratos inicializado!')

    def save(self, statement):
        cursor = self.db.cursor()
        query = "INSERT INTO bank_statement (id_account, balance, deposit, withdraw, operation, situation) values (?, ?, ?, ?, ?, ?)"
        parameters = (statement.accountId, statement.balance, statement.deposit, statement.withdraw, statement.operation, statement.situation)
        try:
            cursor.execute(query, parameters)
            self.db.commit()
        except mariadb.Error as e:
            logging.error(e)

    def findByUserId(self, userId):
        cursor = self.db.cursor(dictionary=True)
        query = """
            SELECT *
            FROM bank_statement
            WHERE id_user = ?
        """
        parameters = (userId,)
        try:
            cursor.execute(query, parameters)
            statementsFromDB = cursor.fetchall()
            if statementsFromDB:
                logging.info(statementsFromDB)
                return statementsFromDB
            else:
                logging.info(f'Nenhum dado encontrado no extrato!')
                return []
        except mariadb.Error as e:
            logging.error(e)

    def find_by_account_id(self, account_id):
        cursor = self.db.cursor(dictionary=True)
        query = """
            SELECT *
            FROM bank_statement
            WHERE id_account = ?
        """
        parameters = (account_id,)
        try:
            cursor.execute(query, parameters)
            statementsFromDB = cursor.fetchall()
            if statementsFromDB:
                return statementsFromDB
            else:
                logging.info(f'Não há extrato para a conta {account_id}')
                return []
        except mariadb.Error as e:
            logging.error(e)

    #Função para buscar os dados sugeridos
    def searchStatement(self, pesquisarOperacao, user_id, accountType, dataInicio, dataFinal):
        cursor = self.db.cursor(dictionary=True)
        query = ("""
                    SELECT USR.*, ACCOUNT.*, STRATEMENT.* 
                    FROM tuser AS USR INNER JOIN taccount AS ACCOUNT ON USR.idUser = ACCOUNT.idAccountUser
                    INNER JOIN bank_statement AS STRATEMENT ON USR.idUser = STRATEMENT.id_user
                    WHERE
                    STRATEMENT.operation LIKE ? AND USR.idUser = ? AND ACCOUNT.account_type = ? AND
                    date(created_time) between ? and ? order by created_time
        """)
        parameters = (pesquisarOperacao, user_id, accountType, dataInicio, dataFinal,)
        logging.info(f'{parameters}')
        try:
            cursor.execute(query, parameters)
            search_statement = cursor.fetchall()
            logging.info(f'{search_statement}')
            if search_statement:
                return search_statement
            else:
                logging.info(f'Nenhum usuário encontrado')
                return []
        except mariadb.Error as e:
            logging.error(e)

    #Função para buscar os dados sugeridos
    def searchOperation(self, pesquisarOperacao, user_id, accountType):
        cursor = self.db.cursor(dictionary=True)
        query = ("""
                    SELECT USR.*, ACCOUNT.*, STRATEMENT.* 
                    FROM tuser AS USR INNER JOIN taccount AS ACCOUNT ON USR.idUser = ACCOUNT.idAccountUser
                    INNER JOIN bank_statement AS STRATEMENT ON USR.idUser = STRATEMENT.id_user
                    WHERE
                    STRATEMENT.operation LIKE ? AND USR.idUser = ? AND ACCOUNT.account_type = ? order by created_time
        """)
        parameters = (pesquisarOperacao, user_id, accountType,)
        logging.info(f'{parameters}')
        try:
            cursor.execute(query, parameters)
            search_statement = cursor.fetchall()
            logging.info(f'{search_statement}')
            if search_statement:
                return search_statement
            else:
                logging.info(f'Nenhum usuário encontrado')
                return []
        except mariadb.Error as e:
            logging.error(e)

    def searchDate(self, user_id, accountType, dataInicio, dataFinal):
        cursor = self.db.cursor(dictionary=True)
        query = ("""
                    SELECT USR.*, ACCOUNT.*, STRATEMENT.* 
                    FROM tuser AS USR INNER JOIN taccount AS ACCOUNT ON USR.idUser = ACCOUNT.idAccountUser
                    INNER JOIN bank_statement AS STRATEMENT ON USR.idUser = STRATEMENT.id_user
                    WHERE
                    USR.idUser = ? AND ACCOUNT.account_type = ? AND
                    date(created_time) between ? and ? order by created_time
        """)
        parameters = (user_id, accountType, dataInicio, dataFinal,)
        logging.info(f'{parameters}')
        try:
            cursor.execute(query, parameters)
            search_statement = cursor.fetchall()
            logging.info(f'{search_statement}')
            if search_statement:
                return search_statement
            else:
                logging.info(f'Nenhum usuário encontrado')
                return []
        except mariadb.Error as e:
            logging.error(e)
class Solicitation:
    def __init__(self, name, cpf, password, status, account, agency, user_id=None):
        self.user_id = user_id
        self.name = name
        self.cpf = cpf
        self.password = password
        self.status = status
        self.account = account
        self.agency = agency

    def __str__(self):
        return f'name: {self.name}, cpf: {self.cpf}, secret: {self.password}, status: {self.status}, account:{self.account}, agency:{self.agency}'

class OpenAccountSolicitation:
    def __init__(self, user_id, solicitation_type, account_type):
        self.user_id = user_id
        self.solicitation_type = solicitation_type
        self.account_type = account_type

class DepositSolicitation:
    def __init__(self, id_solicitation, account_number, deposit_value, id=None):
        self.id=id
        self.id_solicitation= id_solicitation
        self.account_number= account_number
        self.deposit_value= deposit_value
    
class UpdateDataSolicitation:
    def __init__(self, name, road, number_house, district, cep, city, state, genre, id=None, id_solicitation=None, user_id=None):
        self.id=id
        self.id_solicitation=id_solicitation
        self.user_id=user_id
        self.name=name
        self.road=road
        self.number_house=number_house
        self.district=district
        self.cep=cep
        self.city=city
        self.state=state
        self.genre=genre

class CloseAccountSolicitation:
    def __init__(self, id_account, name, cpf, birthdate, road, number_house, district, cep, city, state, genre, id=None, id_solicitation=None, user_id=None):
        self.id = id
        self.id_solicitation = id_solicitation
        self.user_id = user_id
        self.id_account = id_account
        self.name = name
        self.cpf = cpf
        self.birthdate = birthdate
        self.road = road
        self.number_house = number_house
        self.district = district
        self.cep = cep
        self.city = city
        self.state = state
        self.genre = genre

class SimpleSolicitation:
    def __init__(self, id_user, status, solicitation_type, created_time, updated_time, id=None):
        self.id = id
        self.id_user = id_user
        self.status = status
        self.solicitation_type = solicitation_type
        self.created_time = created_time
        self.updated_time = updated_time
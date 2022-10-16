class User:
    def __init__(self, userId, fullName, cpfNumber, secret, dateOfBirth, identificationGender, accountNumber, userAgency, totalBalance, applicationProfile='3'):
        print(userId)
        self.id = userId
        self.name = fullName
        self.cpf = cpfNumber
        self.password = secret
        self.birthDate = dateOfBirth
        self.gender = identificationGender
        self.profile = applicationProfile
        self.account = accountNumber
        self.agency = userAgency
        self.balance = totalBalance

    def setAddress(self, roadAvenue, numberOfHouse, districtVillage, actualCity, actualState, cepCode):
        self.road = roadAvenue
        self.numberHouse = numberOfHouse
        self.district = districtVillage
        self.city = actualCity
        self.state = actualState
        self.cep = cepCode

    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True

    def is_anonymous(self):
        return False
    
    def get_id(self):
        return str(self.id)

    def __str__(self):
        return f'Id: {self.id}, name: {self.name}, cpf: {self.cpf}, secret: {self.password}, nascimento:{self.birthDate}, genero: {self.gender}, perfil:{self.profile}'

    def withdraw(self, value):
        self.balance = self.balance - value
   
    def deposit(self, value):
        self.balance = self.balance + value

class User:
    def __init__(self, userId, fullName, cpfNumber, secret, dateOfBirth, identificationGender, account=None, address=None):
        self.id = userId
        self.name = fullName
        self.cpf = cpfNumber
        self.password = secret
        self.birthDate = dateOfBirth
        self.gender = identificationGender
        self.account = account
        self.address = address

    def balance(self):
        return self.account.balance

    def agency(self):
        return self.account.agency

    def accountNumber(self):
        return self.account.account

    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True

    def is_anonymous(self):
        return False
    
    def get_id(self):
        return str(self.id)

    def __str__(self):
        return f'Id: {self.id}, name: {self.name}, cpf: {self.cpf}, secret: {self.password}, nascimento:{self.birthDate}, genero: {self.gender} :: account {self.account}'

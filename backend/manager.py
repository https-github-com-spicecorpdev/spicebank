from .user import User
class Manager(User):
    def __init__(self, fullName, cpfNumber, secret, dateOfBirth, identificationGender, registrationNumber, workAgency, account=None, address=None, userId=None, id=None):
        super().__init__(userId, fullName, cpfNumber, secret, dateOfBirth, identificationGender, account, address)
        self.registrationNumber = registrationNumber
        self.workAgency = workAgency
        self.managerId = id

    def __str__(self):
        return f'MANAGER: userId: {self.managerId}, name: {self.name}, cpf: {self.cpf}, secret: {self.password}, nascimento:{self.birthDate}, genero: {self.gender} :: account {self.account}, registrationNumber: {self.registrationNumber}, workAgency: {self.workAgency}'
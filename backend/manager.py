from .user import User
class Manager(User):
    def __init__(self, fullName, cpfNumber, secret, dateOfBirth, identificationGender, registrationNumber, workAgency, profile, account=None, address=None, userId=None, managerId=None):
        super().__init__(userId, fullName, cpfNumber, secret, dateOfBirth, identificationGender, account, address)
        self.registrationNumber = registrationNumber
        self.workAgency = workAgency
        self.managerId = managerId
        self.profile= profile

    def __str__(self):
        return f'MANAGER: managerId: {self.managerId}, name: {self.name}, cpf: {self.cpf}, secret: {self.password}, nascimento:{self.birthDate}, genero: {self.gender} :: account {self.account}, registrationNumber: {self.registrationNumber}, workAgency: {self.workAgency}, profileUser: {self.profile}'

    def is_general_manager(self):
        return self.profile==1

    def is_manager(self):
        return self.profile==1 or self.profile == 2
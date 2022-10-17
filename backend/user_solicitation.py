class Solicitation:
    def __init__(self, name, cpf, password, status, account, agency):
        self.name = name
        self.cpf = cpf
        self.password = password
        self.status = status
        self.account = account
        self.agency = agency

    def __str__(self):
        return f'name: {self.name}, cpf: {self.cpf}, secret: {self.password}, status: {self.status}, account:{self.account}, agency:{self.agency}'
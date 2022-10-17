class Account:
    def __init__(self, id=None, accountNumber=None, userAgency=None, totalBalance=None, status=0, solicitacao='pendente'):
        self.id = id
        self.account = accountNumber
        self.agency = userAgency
        self.balance = totalBalance
        self.status = status
        self.solicitacao = solicitacao
    
    def withdraw(self, value):
        self.balance = self.balance - value
   
    def deposit(self, value):
        self.balance = self.balance + value

    def __str__(self):
        return f'Id: {self.id}, account: {self.account}, agency: {self.agency}, balance: {self.balance}, status:{self.status}, solicitacao: {self.solicitacao}'
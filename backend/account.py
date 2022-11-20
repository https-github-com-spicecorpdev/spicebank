class Account:
    def __init__(self, id=None, accountNumber=None, userAgency=None, totalBalance=None, typeAccount=None, status = 'Pendente'):
        self.id = id
        self.account = accountNumber
        self.agency = userAgency
        self.balance = totalBalance
        self.typeAccount = typeAccount
        self.status = status
        
    
    def withdraw(self, value):
        self.balance = self.balance - value
   
    def deposit(self, value):
        self.balance = self.balance + value

    def __str__(self):
        return f'Id: {self.id}, account: {self.account}, agency: {self.agency}, balance: {self.balance}, typeAccount: {self.typeAccount}, status: {self.status}'
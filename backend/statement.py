class Statement:
    def __init__(self, operation, id=None, userId=None, balance=None, deposit=None, withdraw=None, date=None):
        self.id = id
        self.operation = operation
        self.userId = userId
        self.balance = balance
        self.deposit = deposit
        self.withdraw = withdraw
        self.date = date

    def __str__(self):
        return f'Id: {self.id}, userId: {self.userId}, operation: {self.operation}, balance: {self.balance}, deposit: {self.deposit}, withdraw:{self.withdraw}, date: {self.date}'
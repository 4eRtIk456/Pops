class Account:

    def __init__(self, balance, owner):
        self.balance = balance
        self.owner = owner

    def deposit(self, newBalance):
        self.balance += newBalance
        print(f"The operation was successful. Your new balance: {self.balance}")

    def withdraw(self, money):
        if money > self.balance:
            print("The operation is not possible because there are less funds in the account")
        else:
            self.balance -= money
            print(f"The operation was successful. Your new balance: {self.balance}")

a = Account(10000, "Kim Alina")
a.deposit(15000)
a.withdraw(2000)
a.withdraw(24000)

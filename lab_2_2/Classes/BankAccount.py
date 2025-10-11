# Classes/BankAccount.py

# Создаем исключения прямо в этом файле
class InvalidTransactionError(Exception):
    """Исключение для невалидных транзакций"""
    pass

class InsufficientFundsError(Exception):
    """Исключение для недостатка средств"""
    pass


class BankAccount:
    def __init__(self, account_number, account_type, currency, initial_balance=0):
        self.account_number = account_number
        self.account_type = account_type
        self.currency = currency
        self.balance = initial_balance
        self.owner = None
        self.corporate_owner = None
        self.transactions = []
        self.overdraft_limit = 0
        self.interest_rate = 0.01

    def deposit(self, amount):
        """Внести средства на счет"""
        if amount <= 0:
            raise InvalidTransactionError("Сумма должна быть положительной")
        self.balance += amount
        return self.balance

    def withdraw(self, amount):
        """Снять средства со счета"""
        if amount <= 0:
            raise InvalidTransactionError("Сумма должна быть положительной")
        if self.balance + self.overdraft_limit < amount:
            raise InsufficientFundsError("Недостаточно средств")
        self.balance -= amount
        return self.balance
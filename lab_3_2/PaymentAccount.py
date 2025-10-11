from InsufficientFundsError import InsufficientFundsError
from PaymentProcessingError import PaymentProcessingError


class PaymentAccount:
    def __init__(self, account_id, account_type, currency, balance):
        self.account_id = account_id
        self.account_type = account_type
        self.currency = currency
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        return self.balance

    def withdraw(self, amount):
        if self.balance < amount:
            raise InsufficientFundsError("Недостаточно средств")
        self.balance -= amount
        return self.balance

    def transfer_money(self, target_account, amount):
        if self.balance < amount:
            raise InsufficientFundsError("Недостаточно средств для перевода")
        if self.currency != target_account.currency:
            raise PaymentProcessingError("Несовпадение валют")

        self.balance -= amount
        target_account.balance += amount
        return f"Перевод {amount} {self.currency} выполнен успешно"

    def set_spending_limit(self, limit):
        self.spending_limit = limit
        return f"Лимит расходов установлен: {limit}"

    def generate_statement(self, start_date, end_date):
        return f"Выписка с {start_date} по {end_date}. Баланс: {self.balance}"
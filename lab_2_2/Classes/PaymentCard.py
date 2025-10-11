from exceptions.SecurityBreachError import SecurityBreachError
from exceptions.InsufficientFundsError import InsufficientFundsError
from exceptions.InvalidCardError import InvalidCardError

class PaymentCard:
    def __init__(self, card_number, card_holder, expiration_date, cvv, issue_date, balance=0.0, currency="RUB"):
        self.card_number = card_number
        self.card_holder = card_holder
        self.expiration_date = expiration_date
        self.cvv = cvv
        self.balance = balance
        self.currency = currency
        self.status = "active"
        self.daily_limit = 50000
        self.linked_account = None
        self.transaction_history = []

    def check_balance(self):
        return self.balance

    def change_pin(self, new_pin):
        """Изменить ПИН-код"""
        if len(new_pin) != 4:
            raise SecurityBreachError("ПИН-код должен содержать 4 цифры")
        return "PIN changed successfully"

    def transfer_money(self, target_card, amount):
        #Перевести деньги на другую карту
        if self.balance < amount:
            raise InsufficientFundsError("Недостаточно средств для перевода")
        if target_card.status != "active":
            raise InvalidCardError("Целевая карта не активна")

        self.balance -= amount
        target_card.balance += amount
        self.transaction_history.append(f"Transfer to {target_card.card_number}: {amount}")
        return "Transfer successful"


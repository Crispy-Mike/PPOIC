import PaymentCard
from exceptions.InvalidTransactionError import InvalidTransactionError

class CreditCard(PaymentCard):
    def __init__(self, card_number, card_holder, expiration_date, cvv, issue_date, credit_limit=100000, balance=0.0,
                 currency="RUB"):
        super().__init__(card_number, card_holder, expiration_date, cvv, issue_date, balance, currency)
        self.credit_limit = credit_limit
        self.card_type = "Кредитная"
        self.interest_rate = 0.25
        self.minimum_payment = 0

    def make_payment(self, amount):
        """Внести платеж по кредиту"""
        if amount < self.minimum_payment:
            raise InvalidTransactionError("Сумма меньше минимального платежа")
        self.balance -= amount
        return f"Payment of {amount} {self.currency} made"


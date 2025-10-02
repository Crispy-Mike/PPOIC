import MoneyTransfer

class InternationalTransfer(MoneyTransfer):
    def __init__(self, transaction_id, amount, currency, description, sender, receiver, swift_code):
        super().__init__(transaction_id, amount, currency, description, sender, receiver)
        self.swift_code = swift_code
        self.transfer_type = "international"
        self.exchange_rate = None

    def apply_exchange_rate(self, rate):
        """Применить курс обмена"""
        self.exchange_rate = rate
        self.amount *= rate


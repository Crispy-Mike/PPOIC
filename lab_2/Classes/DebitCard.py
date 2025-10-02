import PaymentCard

class DebitCard(PaymentCard):
    def __init__(self, card_number, card_holder, expiration_date, cvv, issue_date, balance=0.0, currency="RUB"):
        super().__init__(card_number, card_holder, expiration_date, cvv, issue_date, balance, currency)
        self.card_type = "Дебетовая"
        self.overdraft_protection = False


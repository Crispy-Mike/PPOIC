import Transaction

class Payment(Transaction):
    def __init__(self, transaction_id, amount, currency, description, payer, payee):
        super().__init__(transaction_id, amount, currency, description)
        self.payer = payer
        self.payee = payee
        self.payment_method = "bank_transfer"

    def check(self):
        if self.payment_method=="bank_transfer":
            pass


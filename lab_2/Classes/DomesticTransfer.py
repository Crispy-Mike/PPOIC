import MoneyTransfer

class DomesticTransfer(MoneyTransfer):
    def __init__(self, transaction_id, amount, currency, description, sender, receiver, bank_code):
        super().__init__(transaction_id, amount, currency, description, sender, receiver)
        self.bank_code = bank_code
        self.transfer_type = "domestic"

    def get_info(self):
        return self.transfer_type
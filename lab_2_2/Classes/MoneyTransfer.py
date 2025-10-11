import Transaction
from exceptions.InsufficientFundsError import InsufficientFundsError

class MoneyTransfer(Transaction):
    def __init__(self, transaction_id, amount, currency, description, sender, receiver):
        super().__init__(transaction_id, amount, currency, description)
        self.sender = sender
        self.receiver = receiver
        self.transfer_type = "internal"

    def validate_transfer(self):
        #Проверить валидность перевода
        if self.sender.balance < self.amount:
            raise InsufficientFundsError("Недостаточно средств у отправителя")
        return True
from InsufficientFundsError import InsufficientFundsError

class MoneyTransfer:
    def __init__(self, transfer_id, amount, currency, description, from_account, to_account):
        self.transfer_id = transfer_id
        self.amount = amount
        self.currency = currency
        self.description = description
        self.from_account = from_account
        self.to_account = to_account

    def validate_transfer(self):
        if self.from_account.balance < self.amount:
            raise InsufficientFundsError("Недостаточно средств")
        return True
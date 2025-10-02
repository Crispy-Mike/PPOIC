from exceptions.InsufficientFundsError import InsufficientFundsError


class ATM:
    def __init__(self, atm_id, location, cash_balance, status):
        self.atm_id = atm_id
        self.location = location
        self.cash_balance = cash_balance
        self.status = status
        self.branch = None
        self.transactions = []

    def dispense_cash(self, amount):
        """Выдать наличные"""
        if self.cash_balance < amount:
            raise InsufficientFundsError("В банкомате недостаточно средств")
        self.cash_balance -= amount
        return f"Выдано {amount} наличных"


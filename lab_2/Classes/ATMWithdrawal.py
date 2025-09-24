import Withdrawal

class ATMWithdrawal(Withdrawal):
    def __init__(self, transaction_id, amount, currency, description, account, atm):
        super().__init__(transaction_id, amount, currency, description, account, atm)
        self.withdrawal_type = "atm"
        self.atm = atm
        self.fee = 0 if account.bank == atm.bank else 1.5


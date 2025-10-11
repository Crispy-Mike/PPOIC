import Withdrawal

class CashWithdrawal(Withdrawal):
    def __init__(self, transaction_id, amount, currency, description, account, branch):
        super().__init__(transaction_id, amount, currency, description, account, branch)
        self.withdrawal_type = "cash"
        self.branch = branch

    def get_info(self):
        return self.withdrawal_type


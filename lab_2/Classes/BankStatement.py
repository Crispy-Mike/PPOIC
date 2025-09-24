
class BankStatement:
    def __init__(self, statement_id, account, period_start, period_end, transactions):
        self.statement_id = statement_id
        self.account = account
        self.period_start = period_start
        self.period_end = period_end
        self.transactions = transactions
        self.opening_balance = 0
        self.closing_balance = 0

    def generate_statement(self):
        """Сгенерировать выписку"""
        self.closing_balance = self.opening_balance + sum(t.amount for t in self.transactions)
        return f"Выписка для счета {self.account.account_number}"


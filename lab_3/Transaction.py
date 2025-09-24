class Transaction:
    def __init__(self, transaction_id, amount, currency, description):
        self.transaction_id = transaction_id
        self.amount = amount
        self.currency = currency
        self.description = description
        self.status = "pending"

    def execute(self):
        self.status = "completed"
        return "Transaction executed"
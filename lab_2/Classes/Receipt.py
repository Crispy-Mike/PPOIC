
class Receipt:
    def __init__(self, receipt_id, transaction, amount, currency, timestamp):
        self.receipt_id = receipt_id
        self.transaction = transaction
        self.amount = amount
        self.currency = currency
        self.timestamp = timestamp
        self.merchant = None

    def print_receipt(self):
        """Распечатать квитанцию"""
        return f"Квитанция #{self.receipt_id} на сумму {self.amount} {self.currency}"


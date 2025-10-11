from PaymentProcessingError import PaymentProcessingError

class Payment:
    def __init__(self, payment_id, amount, currency, payment_date, payment_method):
        self.payment_id = payment_id
        self.amount = amount
        self.currency = currency
        self.payment_date = payment_date
        self.payment_method = payment_method
        self.status = "pending"

    def process_payment(self):
        if self.amount <= 0:
            raise PaymentProcessingError("Неверная сумма платежа")
        self.status = "completed"
        return "Платеж за авиабилет обработан"
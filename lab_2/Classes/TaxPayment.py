import Payment
class TaxPayment(Payment):
    def __init__(self, transaction_id, amount, currency, description, payer, payee, tax_type, tax_year):
        super().__init__(transaction_id, amount, currency, description, payer, payee)
        self.tax_type = tax_type
        self.tax_year = tax_year

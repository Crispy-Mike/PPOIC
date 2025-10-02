import Payment

class UtilityPayment(Payment):
    def __init__(self, transaction_id, amount, currency, description, payer, payee, utility_type, account_number):
        super().__init__(transaction_id, amount, currency, description, payer, payee)
        self.utility_type = utility_type
        self.account_number = account_number

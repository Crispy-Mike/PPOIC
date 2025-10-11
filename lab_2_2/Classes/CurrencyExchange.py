import Transaction

class CurrencyExchange(Transaction):
    def __init__(self, transaction_id, amount, from_currency, to_currency, description, account):
        super().__init__(transaction_id, amount, from_currency, description)
        self.from_currency = from_currency
        self.to_currency = to_currency
        self.account = account
        self.exchange_rate = None

    def calculate_conversion(self, rate):
        #раарассчитать конвертацию
        self.exchange_rate = rate
        return self.amount * rate


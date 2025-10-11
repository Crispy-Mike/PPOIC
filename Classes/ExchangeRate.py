
class ExchangeRate:
    def __init__(self, from_currency, to_currency, rate, last_updated):
        self.from_currency = from_currency
        self.to_currency = to_currency
        self.rate = rate
        self.last_updated = last_updated

    def convert(self, amount):
        """Конвертировать сумму"""
        return amount * self.rate

    def get_reverse_rate(self):
        """Получить обратный курс"""
        return ExchangeRate(self.to_currency, self.from_currency, 1 / self.rate, self.last_updated)



class Currency:
    def __init__(self, code, name, symbol, decimal_places=2):
        self.code = code
        self.name = name
        self.symbol = symbol
        self.decimal_places = decimal_places

    def __str__(self):
        return f"{self.code} ({self.name})"

    def format_amount(self, amount):
        """Форматировать сумму"""
        return f"{amount:.{self.decimal_places}f} {self.symbol}"


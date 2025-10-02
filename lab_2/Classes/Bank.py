class Bank:
    def __init__(self, name_bank):
        self.name_bank = name_bank
        self.headquarters = None
        self.branches = []
        self.departments = []
        self.data_centers = []
        self.all_customers = []
        self.all_employees = []
        self.all_cards = []
        self.all_loans = []
        self.security_systems = []
        self.transactions = []
        self.accounts = []
        self.currency_rates = {}

    def __str__(self):
        return f"Банк: {self.name_bank}"

    def add_currency_rate(self, from_currency, to_currency, rate):
        self.currency_rates[(from_currency.code, to_currency.code)] = rate

    def get_currency_rate(self, from_currency, to_currency):
        return self.currency_rates.get((from_currency.code, to_currency.code))


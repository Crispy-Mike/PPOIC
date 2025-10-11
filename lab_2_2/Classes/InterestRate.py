

class InterestRate:
    def __init__(self, rate, rate_type, effective_date, term):
        self.rate = rate
        self.rate_type = rate_type
        self.effective_date = effective_date
        self.term = term

    def calculate_interest(self, principal):
        """Рассчитать проценты"""
        if self.rate_type == "annual":
            return principal * self.rate
        elif self.rate_type == "monthly":
            return principal * self.rate / 12
        return 0


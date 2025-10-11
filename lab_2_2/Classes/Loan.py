from exceptions.InvalidTransactionError import InvalidTransactionError

class Loan:
    def __init__(self, loan_id, customer, amount, interest_rate, term_months):
        self.loan_id = loan_id
        self.customer = customer
        self.amount = amount
        self.interest_rate = interest_rate
        self.term_months = term_months
        self.remaining_amount = amount
        self.status = "active"
        self.monthly_payment = self.calculate_monthly_payment()

    def calculate_monthly_payment(self):
        """Рассчитать ежемесячный платеж"""
        monthly_rate = self.interest_rate / 12
        return (self.amount * monthly_rate) / (1 - (1 + monthly_rate) ** -self.term_months)

    def make_payment(self, amount):
        """Внести платеж по кредиту"""
        if amount < self.monthly_payment:
            raise InvalidTransactionError("Сумма меньше минимального платежа")
        self.remaining_amount -= amount
        return f"Остаток долга: {self.remaining_amount}"


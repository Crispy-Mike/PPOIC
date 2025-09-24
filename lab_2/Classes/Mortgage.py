import Loan

class Mortgage(Loan):
    def __init__(self, loan_id, customer, amount, interest_rate, term_months, property_address, property_value):
        super().__init__(loan_id, customer, amount, interest_rate, term_months)
        self.loan_type = "Ипотека"
        self.property_address = property_address
        self.property_value = property_value
        self.down_payment = amount * 0.2

import Loan

class PersonalLoan(Loan):
    def __init__(self, loan_id, customer, amount, interest_rate, term_months, purpose):
        super().__init__(loan_id, customer, amount, interest_rate, term_months)
        self.loan_type = "Персональный"
        self.purpose = purpose


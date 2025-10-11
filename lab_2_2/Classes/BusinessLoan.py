import Loan

class BusinessLoan(Loan):
    def __init__(self, loan_id, customer, amount, interest_rate, term_months, business_plan, collateral):
        super().__init__(loan_id, customer, amount, interest_rate, term_months)
        self.loan_type = "Бизнес-кредит"
        self.business_plan = business_plan
        self.collateral = collateral

    def get_info(self):
        return self.loan_type
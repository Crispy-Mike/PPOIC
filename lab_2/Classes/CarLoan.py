import Loan

class CarLoan(Loan):
    def __init__(self, loan_id, customer, amount, interest_rate, term_months, car_model, vin):
        super().__init__(loan_id, customer, amount, interest_rate, term_months)
        self.loan_type = "Автокредит"
        self.car_model = car_model
        self.vin = vin
        self.collateral_value = amount * 0.8

    def get_info(self):
        return self.loan_type


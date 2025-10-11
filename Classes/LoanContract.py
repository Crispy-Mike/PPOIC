import Contract
class LoanContract(Contract):
    def __init__(self, contract_id, parties, start_date, end_date, terms, loan_amount, interest_rate):
        super().__init__(contract_id, parties, start_date, end_date, terms)
        self.loan_amount = loan_amount
        self.interest_rate = interest_rate
        self.remaining_balance = loan_amount

    def interest_rate(self, loan_application):
        """Рассмотреть заявку на кредит"""
        return self.interest_rate


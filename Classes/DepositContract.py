import Contract

class DepositContract(Contract):
    def __init__(self, contract_id, parties, start_date, end_date, terms, deposit_amount, interest_rate):
        super().__init__(contract_id, parties, start_date, end_date, terms)
        self.deposit_amount = deposit_amount
        self.interest_rate = interest_rate
        self.maturity_date = end_date

    def get_info(self):
        return self.deposit_amount

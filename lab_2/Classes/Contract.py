
class Contract:
    def __init__(self, contract_id, parties, start_date, end_date, terms):
        self.contract_id = contract_id
        self.parties = parties
        self.start_date = start_date
        self.end_date = end_date
        self.terms = terms
        self.status = "active"

    def terminate_contract(self):
        """Расторгнуть договор"""
        self.status = "terminated"
        return "Contract terminated"


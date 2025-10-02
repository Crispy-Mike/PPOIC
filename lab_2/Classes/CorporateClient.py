from Customer import Customer

class CorporateClient(Customer):
    def __init__(self, name, surname, passport_id, phone_number, email, company_name, tax_id, company_size):
        super().__init__(name, surname, passport_id, phone_number, email)
        self.company_name = company_name
        self.tax_id = tax_id
        self.company_size = company_size
        self.business_accounts = []
        self.commercial_loans = []

    def __str__(self):
        return f"{super().__str__()}, компания: {self.company_name}"

    def open_business_account(self, account):
        """Открыть бизнес-счет"""
        self.business_accounts.append(account)
        account.corporate_owner = self


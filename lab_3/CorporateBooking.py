class CorporateBooking:
    def __init__(self, contact_name, contact_surname, company_id, phone, email, company_name, employee_count):
        self.contact_name = contact_name
        self.contact_surname = contact_surname
        self.company_id = company_id
        self.phone = phone
        self.email = email
        self.company_name = company_name
        self.employee_count = employee_count
        self.employee_accounts = []

    def add_employee_account(self, passenger):
        self.employee_accounts.append(passenger)
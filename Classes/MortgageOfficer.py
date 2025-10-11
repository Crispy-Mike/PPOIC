import LoanOfficer

class MortgageOfficer(LoanOfficer):
    def __init__(self, name, surname, employee_id, salary, hire_date, loan_types_handled, approval_rate,
                 real_estate_license):
        super().__init__(name, surname, employee_id, salary, hire_date, loan_types_handled, approval_rate)
        self.position = "Ипотечный специалист"
        self.real_estate_license = real_estate_license


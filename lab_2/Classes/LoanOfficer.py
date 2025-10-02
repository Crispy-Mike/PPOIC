import Employee

class LoanOfficer(Employee):
    def __init__(self, name, surname, employee_id, salary, hire_date, loan_types_handled, approval_rate):
        super().__init__(name, surname, employee_id, "Кредитный специалист", salary, hire_date)
        self.loan_types_handled = loan_types_handled
        self.approval_rate = approval_rate
        self.loans_processed = []

    def review_application(self, loan_application):
        """Рассмотреть заявку на кредит"""
        return loan_application.review()


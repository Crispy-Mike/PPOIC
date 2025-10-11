from exceptions.LoanDeniedError import LoanDeniedError

class LoanApplication:
    def __init__(self, application_id, customer, loan_type, amount, term_months, purpose):
        self.application_id = application_id
        self.customer = customer
        self.loan_type = loan_type
        self.amount = amount
        self.term_months = term_months
        self.purpose = purpose
        self.status = "pending"
        self.credit_check = None

    def process(self):
        if self.customer.credit_score < 600:
            self.status = "denied"
            raise LoanDeniedError("Низкий кредитный рейтинг")
        self.status = "approved"
        return "Заявка одобрена"

    def review(self):
        """Рассмотреть заявку"""
        return f"Заявка {self.application_id} на рассмотрении"


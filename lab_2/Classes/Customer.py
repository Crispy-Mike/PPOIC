from exceptions.LoanDeniedError import LoanDeniedError

class Customer:
    def __init__(self, name, surname, passport_id, phone_number, email):
        self.name = name
        self.surname = surname
        self.passport_id = passport_id
        self.phone_number = phone_number
        self.email = email
        self.accounts = []
        self.cards = []
        self.loans = []
        self.credit_score = 650
        self.registration_date = None

    def __str__(self):
        return f"Клиент: {self.name} {self.surname}, паспорт: {self.passport_id}"

    def open_account(self, account):
        """Открыть счет"""
        self.accounts.append(account)
        account.owner = self

    def apply_for_loan(self, loan_application):
        """Подать заявку на кредит"""
        if self.credit_score < 600:
            raise LoanDeniedError("Низкий кредитный рейтинг")
        return loan_application.process()

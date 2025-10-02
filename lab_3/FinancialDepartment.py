from exceptions import InsufficientFundsError, PaymentProcessingError


class FinancialDepartment:
    def __init__(self, dept_id, budget, currency, fiscal_year):
        self.dept_id = dept_id
        self.budget = budget
        self.currency = currency
        self.fiscal_year = fiscal_year
        self.transactions = []
        self.salaries = []
        self.invoices = []

    def process_salary_payment(self, employee, amount):
        if self.budget < amount:
            raise InsufficientFundsError("Недостаточно средств в бюджете")

        self.budget -= amount
        transaction = {
            'type': 'salary',
            'employee': employee,
            'amount': amount,
            'date': datetime.now()
        }
        self.transactions.append(transaction)
        return f"Зарплата {amount} выплачена {employee.name}"

    def generate_financial_report(self, start_date, end_date):
        period_transactions = [t for t in self.transactions
                               if start_date <= t['date'] <= end_date]
        total = sum(t['amount'] for t in period_transactions)
        return f"Отчет за период: {total} {self.currency}"
from Employee import Employee

class Cashier(Employee):
    def __init__(self, name, surname, employee_id, salary, hire_date, cash_drawer):
        super().__init__(name, surname, employee_id, "Кассир", salary, hire_date)
        self.cash_drawer = cash_drawer
        self.transactions_processed = 0

    def process_transaction(self, transaction):
        """Обработать транзакцию"""
        self.transactions_processed += 1
        return transaction.execute()

from Employee import Employee

class FinancialAdvisor(Employee):
    def __init__(self, name, surname, employee_id, salary, hire_date, specialization, certifications):
        super().__init__(name, surname, employee_id, "Финансовый советник", salary, hire_date)
        self.specialization = specialization
        self.certifications = certifications
        self.clients = []

    def provide_advice(self, client, advice_type):
        return f"Консультация по {advice_type} для клиента {client.name}"

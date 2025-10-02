from FinancialAdvisor import FinancialAdvisor

class InvestmentAdvisor(FinancialAdvisor):
    def __init__(self, name, surname, employee_id, salary, hire_date, specialization, certifications,
                 investment_license):
        super().__init__(name, surname, employee_id, salary, hire_date, specialization, certifications)
        self.position = "Инвестиционный советник"
        self.investment_license = investment_license

    def get_info(self):
        return self.position

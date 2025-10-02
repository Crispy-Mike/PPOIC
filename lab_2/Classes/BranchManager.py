from .Manager import Manager  # Используем относительный импорт

class BranchManager(Manager):
    def __init__(self, name, surname, employee_id, salary, hire_date, years_of_experience, branch):
        super().__init__(name, surname, employee_id, salary, hire_date, years_of_experience)
        self.position = "Менеджер филиала"
        self.access_level = "branch_manager"
        self.branch = branch

    def approve_loan(self, loan_application):
        """Одобрение кредита"""
        if loan_application.amount <= 5000000:  # Пример лимита
            loan_application.status = "approved"
            return "Кредит одобрен"
        else:
            loan_application.status = "rejected"
            return "Кредит отклонен - превышен лимит"

    def manage_branch_operations(self):
        """Управление операциями филиала"""
        return "Управление операциями филиала"

    def generate_branch_report(self):
        """Генерация отчета по филиалу"""
        return "Отчет по филиалу"
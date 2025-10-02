from Employee import Employee

class SystemAdmin(Employee):
    def __init__(self, name, surname, employee_id, salary, hire_date, admin_rights, systems_managed):
        super().__init__(name, surname, employee_id, "Системный администратор", salary, hire_date)
        self.admin_rights = admin_rights
        self.systems_managed = systems_managed
        self.access_level = "admin"

    def reset_password(self, user, new_password):
        return f"Пароль для {user} сброшен"


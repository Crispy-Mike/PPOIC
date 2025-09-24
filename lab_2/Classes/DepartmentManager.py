from Manager import *

class DepartmentManager(Manager):
    def __init__(self, name, surname, employee_id, salary, hire_date, team_size, department):
        super().__init__(name, surname, employee_id, "Менеджер департамента", salary, hire_date, team_size)
        self.department = department
        self.access_level = "department_manager"

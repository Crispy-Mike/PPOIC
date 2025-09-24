from exceptions.BankException import BankException
from DepartmentManager import DepartmentManager
class Department:
    def __init__(self, name_department, department_type, max_employees=50):
        self.name_department = name_department
        self.department_type = department_type
        self.max_employees = max_employees
        self.employees = []
        self.manager = None

    def set_manager(self, employee):
        if not isinstance(employee, DepartmentManager):
            raise BankException("Только менеджер департамента может быть назначен")
        self.manager = employee

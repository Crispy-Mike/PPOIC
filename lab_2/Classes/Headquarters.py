from exceptions.DepartmentFullError import DepartmentFullError

class Headquarters:
    def __init__(self, name_headquarters, address):
        self.name_headquarters = name_headquarters
        self.address = address
        self.customers = []
        self.employees = []
        self.security_level = "high"
        self.operating_hours = "9:00-18:00"

    def add_employee(self, employee):
        #Добавить сотрудниа в главный офи
        if len(self.employees) >= 100:
            raise DepartmentFullError("Главный офис переполнен")
        self.employees.append(employee)
        employee.workplace = self


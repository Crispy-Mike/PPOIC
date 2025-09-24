from Classes.Employee import Employee

class Manager(Employee):
    def __init__(self, name, surname, employee_id, position, salary, hire_date, team_size):
        super().__init__(name, surname, employee_id, position, salary, hire_date)
        self.team_size = team_size
        self.subordinates = []
        self.access_level = "manager"

    def add_subordinate(self, employee):
       #добавить подчиненного
        self.subordinates.append(employee)


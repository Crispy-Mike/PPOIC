class Employee:
    def __init__(self, name, surname, employee_id, position, salary, hire_date):
        self.name = name
        self.surname = surname
        self.employee_id = employee_id
        self.position = position
        self.salary = salary
        self.hire_date = hire_date
        self.workplace = None
        self.department = None
        self.access_level = "basic"

    def __str__(self):
        return f"Сотрудник: {self.name} {self.surname}, должность: {self.position}"

    def request_vacation(self, start_date, end_date):
        #Запрсить отпуск
        return f"Запрос отпуска с {start_date} по {end_date} для {self.name}"


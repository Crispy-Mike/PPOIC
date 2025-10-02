from Employee import Employee

class SecurityOfficer(Employee):
    def __init__(self, name, surname, employee_id, salary, hire_date, security_clearance, weapons_trained):
        super().__init__(name, surname, employee_id, "Охранник", salary, hire_date)
        self.security_clearance = security_clearance
        self.weapons_trained = weapons_trained
        self.patrol_routes = []

    def perform_patrol(self, route):
        #выполнить патрулирование
        return f"Патрулирование маршрута {route}"


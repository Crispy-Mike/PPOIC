from Cashier import Cashier
class Teller(Cashier):
    def __init__(self, name, surname, employee_id, salary, hire_date, cash_drawer, customer_service_rating):
        super().__init__(name, surname, employee_id, salary, hire_date, cash_drawer)
        self.position = "Кассир-операционист"
        self.customer_service_rating = customer_service_rating

    def check(self):
        if self.position=="Кассир-операционист":
            pass

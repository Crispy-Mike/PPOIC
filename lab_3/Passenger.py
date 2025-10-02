class Passenger:
    def __init__(self, name, surname, passenger_id, phone, email, age, passport_number, frequent_flyer_status="standard"):
        self.name = name
        self.surname = surname
        self.passenger_id = passenger_id
        self.phone = phone
        self.email = email
        self.age = age
        self.passport_number = passport_number
        self.frequent_flyer_status = frequent_flyer_status
        self.booking_status = "active"
        self.credit_score = 700
        self.flights_taken = 0

    def __str__(self):
        return f"Пассажир: {self.name} {self.surname}, ID: {self.passenger_id}"

    def verify_identity(self, document_number):
        return self.passport_number == document_number

    def upgrade_status(self, new_status):
        if new_status in ["standard", "silver", "gold", "platinum"]:
            self.frequent_flyer_status = new_status
            return f"Статус обновлен до {new_status}"
        return "Неверный статус"

    def calculate_flight_discount(self):
        discounts = {"standard": 0, "silver": 5, "gold": 15, "platinum": 25}
        return discounts.get(self.frequent_flyer_status, 0)
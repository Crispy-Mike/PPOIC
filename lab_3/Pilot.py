class Pilot:
    def __init__(self, name, surname, pilot_id, license_type, salary, hire_date, flight_hours):
        self.name = name
        self.surname = surname
        self.pilot_id = pilot_id
        self.license_type = license_type
        self.salary = salary
        self.hire_date = hire_date
        self.flight_hours = flight_hours
        self.schedule = {}
        self.certifications = []

    def __str__(self):
        return f"Пилот: {self.name} {self.surname}, лицензия: {self.license_type}"
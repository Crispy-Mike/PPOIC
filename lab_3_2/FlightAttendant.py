class FlightAttendant:
    def __init__(self, name, surname, attendant_id, languages, hire_date, base_airport):
        self.name = name
        self.surname = surname
        self.attendant_id = attendant_id
        self.languages = languages
        self.hire_date = hire_date
        self.base_airport = base_airport
        self.available = True
        self.flight_hours = 0

    def __str__(self):
        return f"Бортпроводник: {self.name} {self.surname}, языки: {', '.join(self.languages)}"
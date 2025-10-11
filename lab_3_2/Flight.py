from FlightFullError import FlightFullError
from AgeRestrictionError import AgeRestrictionError
class Flight:
    def __init__(self, flight_number, departure_airport, arrival_airport, departure_time, arrival_time, aircraft_type, capacity):
        self.flight_number = flight_number
        self.departure_airport = departure_airport
        self.arrival_airport = arrival_airport
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.aircraft_type = aircraft_type
        self.capacity = capacity
        self.current_passengers = 0
        self.pilots = []
        self.flight_attendants = []

    def add_passenger(self, passenger):
        if self.current_passengers >= self.capacity:
            raise FlightFullError("Рейс переполнен")
        if passenger.age < 2 and not self.has_infant_accommodation():
            raise AgeRestrictionError("Необходимо специальное место для младенца")
        self.current_passengers += 1
        return f"{passenger.name} добавлен на рейс {self.flight_number}"

    def calculate_load_factor(self):
        return (self.current_passengers / self.capacity) * 100

    def check_connection_time(self, connecting_flight):
        time_between = connecting_flight.departure_time - self.arrival_time
        return time_between.total_seconds() >= 3600  # минимум 1 час

    def assign_pilot(self, pilot):
        if pilot.license_type not in ["ATP", "Commercial"]:
            raise Exception("Пилот не имеет необходимой лицензии")
        self.pilots.append(pilot)
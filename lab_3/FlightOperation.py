from exceptions import CrewUnavailableError

class FlightOperation:
    def __init__(self, operation_id, pilot, co_pilot, flight, departure_time, arrival_time, fuel_consumption):
        self.operation_id = operation_id
        self.pilot = pilot
        self.co_pilot = co_pilot
        self.flight = flight
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.fuel_consumption = fuel_consumption
        self.crew_members = []

    def add_crew_member(self, attendant):
        if attendant.available:
            self.crew_members.append(attendant)
            return "Член экипажа добавлен"
        raise CrewUnavailableError("Член экипажа недоступен")
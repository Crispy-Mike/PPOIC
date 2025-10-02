class Airline:
    def __init__(self, airline_code, name, headquarters, founding_year):
        self.airline_code = airline_code
        self.name = name
        self.headquarters = headquarters
        self.founding_year = founding_year
        self.passengers = []
        self.pilots = []
        self.aircrafts = []

    def add_passenger(self, passenger):
        self.passengers.append(passenger)

    def add_pilot(self, pilot):
        self.pilots.append(pilot)
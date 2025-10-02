class Airport:
    def __init__(self, airport_code, name, city, country, capacity, terminals):
        self.airport_code = airport_code
        self.name = name
        self.city = city
        self.country = country
        self.capacity = capacity
        self.terminals = terminals
        self.current_occupancy = 0
        self.runways = []

    def check_capacity(self):
        return self.current_occupancy < self.capacity
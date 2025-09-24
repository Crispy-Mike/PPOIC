class Baggage:
    def __init__(self, baggage_id, passenger, weight, dimensions, flight, special_handling=False):
        self.baggage_id = baggage_id
        self.passenger = passenger
        self.weight = weight
        self.dimensions = dimensions
        self.flight = flight
        self.special_handling = special_handling
        self.tracking_status = "checked_in"

    def calculate_excess_fee(self):
        free_allowance = 23  # кг
        if self.weight > free_allowance:
            return (self.weight - free_allowance) * 50
        return 0
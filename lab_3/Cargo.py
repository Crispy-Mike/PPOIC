class Cargo:
    def __init__(self, cargo_id, description, weight, dimensions, sender, recipient, flight):
        self.cargo_id = cargo_id
        self.description = description
        self.weight = weight
        self.dimensions = dimensions
        self.sender = sender
        self.recipient = recipient
        self.flight = flight
        self.tracking_number = f"CRG{flight.flight_number}{cargo_id}"

    def calculate_shipping_cost(self):
        base_cost = 50
        weight_cost = self.weight * 2
        return base_cost + weight_cost
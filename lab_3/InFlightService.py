class InFlightService:
    def __init__(self, service_id, name, category, price, available_classes):
        self.service_id = service_id
        self.name = name
        self.category = category
        self.price = price
        self.available_classes = available_classes
        self.in_stock = True

    def check_availability(self, flight_class):
        return self.in_stock and flight_class in self.available_classes
class PromotionalOffer:
    def __init__(self, offer_id, name, description, discount_percent, start_date, end_date, eligible_routes):
        self.offer_id = offer_id
        self.name = name
        self.description = description
        self.discount_percent = discount_percent
        self.start_date = start_date
        self.end_date = end_date
        self.eligible_routes = eligible_routes
        self.eligible_passengers = []

    def add_eligible_passenger(self, passenger):
        self.eligible_passengers.append(passenger)
        return f"{passenger.name} добавлен в акцию"
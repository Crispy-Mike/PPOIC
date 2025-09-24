class AircraftRental:
    def __init__(self, rental_id, aircraft, airline, rental_date, return_date, lease_amount):
        self.rental_id = rental_id
        self.aircraft = aircraft
        self.airline = airline
        self.rental_date = rental_date
        self.return_date = return_date
        self.lease_amount = lease_amount
        self.returned = False

    def process_return(self):
        self.returned = True
        return "Аренда самолета завершена"
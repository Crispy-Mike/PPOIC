from datetime import datetime

class Booking:
    def __init__(self, booking_id, passenger, flight, seat_number, booking_date, price):
        self.booking_id = booking_id
        self.passenger = passenger
        self.flight = flight
        self.seat_number = seat_number
        self.booking_date = booking_date
        self.price = price
        self.is_confirmed = True
        self.check_in_status = False

    def check_validity(self):
        return datetime.now() <= self.flight.departure_time and self.is_confirmed
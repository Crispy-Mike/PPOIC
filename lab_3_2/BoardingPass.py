from datetime import datetime


class BoardingPass:
    def __init__(self, pass_id, passenger, flight, seat, gate, boarding_time, qr_code):
        self.pass_id = pass_id
        self.passenger = passenger
        self.flight = flight
        self.seat = seat
        self.gate = gate
        self.boarding_time = boarding_time
        self.qr_code = qr_code
        self.is_checked = False
        self.baggage_tags = []

    def validate_boarding_pass(self):
        current_time = datetime.now()
        return (current_time <= self.boarding_time and
                not self.passenger.booking_status == "cancelled")

    def scan_boarding_pass(self):
        self.is_checked = True
        return f"Посадка подтверждена для {self.passenger.name}"
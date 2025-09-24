from exceptions import FlightFullError, AirportOvercrowdedError

class GroupBooking:
    def __init__(self, group_id, organizer, flight, group_size, discount_percent):
        self.group_id = group_id
        self.organizer = organizer
        self.flight = flight
        self.group_size = group_size
        self.discount_percent = discount_percent
        self.participants = []

    def add_participant(self, passenger):
        if len(self.participants) >= self.group_size:
            raise FlightFullError("Группа переполнена")
        if not self.flight.aircraft.check_capacity():
            raise AirportOvercrowdedError("Самолет переполнен")
        self.participants.append(passenger)
        self.flight.current_passengers += 1
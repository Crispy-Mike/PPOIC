class FlightTracker:
    def __init__(self, tracker_id, flight, departure_time, arrival_time, current_location):
        self.tracker_id = tracker_id
        self.flight = flight
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.current_location = current_location
        self.status = "scheduled"

    def update_status(self, new_status):
        self.status = new_status
        return f"Статус рейса обновлен: {new_status}"
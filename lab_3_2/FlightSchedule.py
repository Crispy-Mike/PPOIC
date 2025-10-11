from ScheduleConflictError import ScheduleConflictError

class FlightSchedule:
    def __init__(self, schedule_id, pilot, aircraft, departure_time, arrival_time, route):
        self.schedule_id = schedule_id
        self.pilot = pilot
        self.aircraft = aircraft
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.route = route

    def check_conflict(self, other_schedule):
        if (self.pilot == other_schedule.pilot and
                self.departure_time < other_schedule.arrival_time and
                self.arrival_time > other_schedule.departure_time):
            raise ScheduleConflictError("Конфликт расписания пилота")
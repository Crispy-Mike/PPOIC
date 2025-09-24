from datetime import datetime, timedelta
from exceptions import ScheduleConflictError, CrewUnavailableError


class CrewScheduling:
    def __init__(self, schedule_id, crew_member, flight, role, report_time):
        self.schedule_id = schedule_id
        self.crew_member = crew_member
        self.flight = flight
        self.role = role
        self.report_time = report_time
        self.duty_duration = timedelta(hours=8)
        self.rest_period = timedelta(hours=12)

    def check_fatigue_risk(self):
        recent_flights = [s for s in self.crew_member.schedule
                          if s.flight.arrival_time > datetime.now() - timedelta(days=1)]
        total_hours = sum((s.duty_duration.total_seconds() / 3600) for s in recent_flights)
        return total_hours > 12

    def assign_to_flight(self):
        if self.check_fatigue_risk():
            raise CrewUnavailableError("Экипаж превысил лимит рабочего времени")
        self.crew_member.schedule.append(self)
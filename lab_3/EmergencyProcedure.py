from datetime import datetime, timedelta

class EmergencyProcedure:
    def __init__(self, procedure_id, aircraft, procedure_type, steps, last_drill_date):
        self.procedure_id = procedure_id
        self.aircraft = aircraft
        self.procedure_type = procedure_type
        self.steps = steps
        self.last_drill_date = last_drill_date

    def needs_refresher(self):
        return datetime.now() > self.last_drill_date + timedelta(days=180)
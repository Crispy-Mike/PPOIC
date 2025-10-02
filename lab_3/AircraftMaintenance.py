class AircraftMaintenance:
    def __init__(self, maintenance_id, aircraft, technician, maintenance_date, cost, maintenance_type):
        self.maintenance_id = maintenance_id
        self.aircraft = aircraft
        self.technician = technician
        self.maintenance_date = maintenance_date
        self.cost = cost
        self.maintenance_type = maintenance_type
        self.status = "scheduled"

    def perform_maintenance(self):
        self.status = "completed"
        self.aircraft.last_maintenance = self.maintenance_date
        self.aircraft.status = "operational"
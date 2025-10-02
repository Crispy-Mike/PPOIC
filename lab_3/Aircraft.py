from datetime import datetime, timedelta

class Aircraft:
    def __init__(self, aircraft_id, model, manufacturer, purchase_date, maintenance_interval, total_seats):
        self.aircraft_id = aircraft_id
        self.model = model
        self.manufacturer = manufacturer
        self.purchase_date = purchase_date
        self.maintenance_interval = maintenance_interval
        self.last_maintenance = purchase_date
        self.status = "operational"
        self.total_seats = total_seats
        self.current_location = "Hangar"

    def needs_maintenance(self):
        next_maintenance = self.last_maintenance + timedelta(days=self.maintenance_interval)
        return datetime.now() > next_maintenance

    def has_infant_accommodation(self):
        return self.total_seats > 100  # Крупные самолеты имеют места для младенцев
class FlightRoute:
    def __init__(self, route_id, origin, destination, distance_km, flight_time, intermediate_stops=[]):
        self.route_id = route_id
        self.origin = origin
        self.destination = destination
        self.distance_km = distance_km
        self.flight_time = flight_time
        self.intermediate_stops = intermediate_stops
        self.weather_conditions = {}
        self.air_traffic = "normal"

    def calculate_fuel_requirement(self, aircraft):
        return self.distance_km * aircraft.fuel_efficiency

    def add_weather_alert(self, alert_type, severity):
        self.weather_conditions[alert_type] = severity
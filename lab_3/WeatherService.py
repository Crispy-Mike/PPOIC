class WeatherService:
    def __init__(self, service_id, airport, temperature, wind_speed, visibility, conditions):
        self.service_id = service_id
        self.airport = airport
        self.temperature = temperature
        self.wind_speed = wind_speed
        self.visibility = visibility
        self.conditions = conditions
        self.forecast = []
        self.weather_alerts = []

    def check_takeoff_conditions(self):
        return (self.wind_speed < 50 and
                self.visibility > 1000 and
                "storm" not in self.conditions.lower())

    def update_weather_data(self, new_temperature, new_wind_speed, new_visibility, new_conditions):
        self.temperature = new_temperature
        self.wind_speed = new_wind_speed
        self.visibility = new_visibility
        self.conditions = new_conditions
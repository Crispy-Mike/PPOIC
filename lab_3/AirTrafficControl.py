from SafetyRiskError import SafetyRiskError


class AirTrafficControl:
    def __init__(self, atc_id, airport, frequency, sector):
        self.atc_id = atc_id
        self.airport = airport
        self.frequency = frequency
        self.sector = sector
        self.active_flights = []
        self.communication_log = []
        self.weather_advisories = []

    def authorize_takeoff(self, flight, runway):
        if len(self.active_flights) > 10:
            raise SafetyRiskError("Слишком много активных рейсов в секторе")

        authorization = {
            'flight': flight,
            'runway': runway,
            'status': 'cleared'
        }
        self.active_flights.append(flight)
        return f"Рейс {flight.flight_number} разрешен к взлету с ВПП {runway}"

    def authorize_landing(self, flight, runway, approach_type):
        return f"Рейс {flight.flight_number} разрешен к посадке на ВПП {runway}"
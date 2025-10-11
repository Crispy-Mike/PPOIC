from SafetyRiskError import SafetyRiskError
from CrewUnavailableError import CrewUnavailableError

class BaggageHandler:
    def __init__(self, handler_id, name, certification_level, current_airport):
        self.handler_id = handler_id
        self.name = name
        self.certification_level = certification_level
        self.current_airport = current_airport
        self.bags_handled_today = 0
        self.max_daily_capacity = 500

    def load_baggage(self, baggage, aircraft):
        if baggage.weight > 32:
            raise SafetyRiskError("Превышен вес багажа")
        if self.bags_handled_today >= self.max_daily_capacity:
            raise CrewUnavailableError("Превышена дневная норма загрузки")

        self.bags_handled_today += 1
        return f"Багаж {baggage.baggage_id} загружен в {aircraft.aircraft_id}"

    def unload_baggage(self, baggage, destination):
        return f"Багаж {baggage.baggage_id} выгружен в {destination}"
from SafetyRiskError import SafetyRiskError


class FuelManagement:
    def __init__(self, fuel_id, aircraft, current_fuel, max_capacity, fuel_type):
        self.fuel_id = fuel_id
        self.aircraft = aircraft
        self.current_fuel = current_fuel
        self.max_capacity = max_capacity
        self.fuel_type = fuel_type
        self.consumption_rate = 0.15  # литров на км
        self.last_refuel_date = None

    def calculate_required_fuel(self, distance):
        required = distance * self.consumption_rate * 1.2  # +20% резерв
        if required > self.max_capacity:
            raise SafetyRiskError("Требуется слишком много топлива")
        return required

    def refuel_aircraft(self, amount):
        if self.current_fuel + amount > self.max_capacity:
            raise SafetyRiskError("Перелив топлива")
        self.current_fuel += amount
        self.last_refuel_date = datetime.now()
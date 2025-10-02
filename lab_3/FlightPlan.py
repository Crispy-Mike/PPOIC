class FlightPlan:
    def __init__(self, plan_id, passenger, flights, total_duration, layovers):
        self.plan_id = plan_id
        self.passenger = passenger
        self.flights = flights
        self.total_duration = total_duration
        self.layovers = layovers
        self.connections = []

    def add_connection(self, connection):
        self.connections.append(connection)
        return "Переconnection добавлена в план"
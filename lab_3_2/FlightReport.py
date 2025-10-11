class FlightReport:
    def __init__(self, report_id, flight, report_date, content, metrics):
        self.report_id = report_id
        self.flight = flight
        self.report_date = report_date
        self.content = content
        self.metrics = metrics

    def generate_summary(self):
        return f"Отчет по рейсу {self.flight.flight_number}: {self.content}"
from exceptions import BookingDeniedError

class BookingApplication:
    def __init__(self, application_id, applicant, flight_class, baggage_allowance, special_requests):
        self.application_id = application_id
        self.applicant = applicant
        self.flight_class = flight_class
        self.baggage_allowance = baggage_allowance
        self.special_requests = special_requests
        self.status = "pending"

    def process(self):
        if self.applicant.credit_score < 600:
            raise BookingDeniedError("Бронирование отклонено")
        self.status = "approved"
        return "Бронирование одобрено"
class FlightReview:
    def __init__(self, review_id, passenger, flight, rating, comment, review_date):
        self.review_id = review_id
        self.passenger = passenger
        self.flight = flight
        self.rating = rating
        self.comment = comment
        self.review_date = review_date

    def add_rating(self):
        return f"Рейтинг {self.rating}/5 добавлен для рейса {self.flight.flight_number}"
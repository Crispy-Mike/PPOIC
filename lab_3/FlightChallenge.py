class FlightChallenge:
    def __init__(self, challenge_id, name, start_date, end_date, target_miles, prize):
        self.challenge_id = challenge_id
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.target_miles = target_miles
        self.prize = prize
        self.participants = []

    def add_participant(self, passenger):
        self.participants.append(passenger)
        return f"{passenger.name} присоединился к авиачелленджу"
class LoyaltyProgram:
    def __init__(self, program_id, passenger, miles_balance, tier, membership_since):
        self.program_id = program_id
        self.passenger = passenger
        self.miles_balance = miles_balance
        self.tier = tier
        self.membership_since = membership_since
        self.bonus_miles = 0

    def add_miles(self, miles_earned):
        self.miles_balance += miles_earned
        if self.tier == "gold":
            self.bonus_miles += miles_earned * 0.5
        return self.miles_balance
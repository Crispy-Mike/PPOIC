class AirlineAlliance:
    def __init__(self, alliance_id, name, founding_year, number_of_members):
        self.alliance_id = alliance_id
        self.name = name
        self.founding_year = founding_year
        self.number_of_members = number_of_members
        self.members = []

    def add_member(self, airline):
        self.members.append(airline)
        return "Авиакомпания добавлена в альянс"

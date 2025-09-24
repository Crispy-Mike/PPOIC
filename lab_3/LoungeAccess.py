class LoungeAccess:
    def __init__(self, lounge_id, name, location, amenities, access_fee):
        self.lounge_id = lounge_id
        self.name = name
        self.location = location
        self.amenities = amenities
        self.access_fee = access_fee
        self.occupied = False
        self.access_granted_to = None

    def grant_access(self, passenger):
        if self.occupied and passenger.frequent_flyer_status != "platinum":
            raise Exception("Лаунж переполнен")
        self.occupied = True
        self.access_granted_to = passenger
        return f"Доступ в лаунж {self.name} предоставлен"
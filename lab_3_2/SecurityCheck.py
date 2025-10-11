from AuthenticationError import AuthenticationError

class SecurityCheck:
    def __init__(self, check_id, status, security_level, max_attempts, timeout_duration):
        self.check_id = check_id
        self.status = status
        self.security_level = security_level
        self.max_attempts = max_attempts
        self.timeout_duration = timeout_duration
        self.failed_attempts = 0

    def authenticate_passenger(self, passport_number, ticket_number):
        if self.failed_attempts >= self.max_attempts:
            raise AuthenticationError("Слишком много попыток")
        if passport_number == "AB123456" and ticket_number == "TK789012":
            self.failed_attempts = 0
            return True
        self.failed_attempts += 1
        return False

    def verify_biometric_data(self, fingerprint, facial_recognition):
        return fingerprint == "match" and facial_recognition == "verified"

    def check_security_clearance(self, passenger, required_level):
        clearances = {"low": 1, "medium": 2, "high": 3, "maximum": 4}
        passenger_level = clearances.get(passenger.frequent_flyer_status, 0)
        return passenger_level >= clearances.get(required_level, 0)

    def log_security_event(self, event_type, details):
        log_entry = {
            'timestamp': datetime.now(),
            'event_type': event_type,
            'details': details,
            'officer': self.check_id
        }
        return "Событие залогировано"
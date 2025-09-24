class InsufficientFundsError(Exception):
    pass

class SecurityBreachError(Exception):
    pass

class BookingDeniedError(Exception):
    pass

class AuthenticationError(Exception):
    pass

class MaintenanceError(Exception):
    pass

class FlightFullError(Exception):
    pass

class CrewUnavailableError(Exception):
    pass

class AgeRestrictionError(Exception):
    pass

class SafetyRiskError(Exception):
    pass

class PaymentProcessingError(Exception):
    pass

class ScheduleConflictError(Exception):
    pass

class AirportOvercrowdedError(Exception):
    pass
import unittest
from datetime import datetime, timedelta
from AgeRestrictionError import AgeRestrictionError
from AirportOvercrowdedError import AirportOvercrowdedError
from AgeRestrictionError import AgeRestrictionError
from BookingDeniedError import BookingDeniedError
from CrewUnavailableError import CrewUnavailableError
from FlightFullError import FlightFullError
from InsufficientFundsError import InsufficientFundsError
from MaintenanceError import MaintenanceError
from AuthenticationError import AuthenticationError
from BookingDeniedError import BookingDeniedError
from SecurityBreachError import SecurityBreachError
from SafetyRiskError import SafetyRiskError
from Passenger import Passenger
from Pilot import Pilot
from Flight import Flight
from Aircraft import Aircraft
from Airport import Airport
from PaymentAccount import PaymentAccount
from SafetyInspection import SafetyInspection
from BookingApplication import BookingApplication
from SecurityCheck import SecurityCheck
from DocumentValidator import DocumentValidator
class TestAirlineSystem(unittest.TestCase):

    def setUp(self):
        self.passenger = Passenger("Иван", "Иванов", "PASS001", "+79991234567", "ivan@mail.com", 25, "AB123456")
        self.pilot = Pilot("Петр", "Петров", "PIL001", "ATP", 150000, "2020-01-01", 5000)
        self.flight = Flight("SU100", "SVO", "JFK", datetime(2024, 6, 1, 10, 0), datetime(2024, 6, 1, 22, 0), "Boeing 777", 300)
        self.aircraft = Aircraft("AC001", "Boeing 777", "Boeing", datetime.now(), 30, 350)
        self.airport = Airport("SVO", "Шереметьево", "Москва", "Россия", 10000, ["A", "B", "C", "D", "E", "F"])
        self.payment_account = PaymentAccount("ACC001", "личный", "RUB", 50000)

    def test_passenger_creation(self):
        self.assertEqual(self.passenger.name, "Иван")
        self.assertEqual(str(self.passenger), "Пассажир: Иван Иванов, ID: PASS001")

    def test_pilot_creation(self):
        self.assertEqual(self.pilot.license_type, "ATP")
        self.assertEqual(str(self.pilot), "Пилот: Петр Петров, лицензия: ATP")

    def test_flight_booking(self):
        result = self.flight.add_passenger(self.passenger)
        self.assertEqual(result, "Иван добавлен на рейс SU100")
        self.assertEqual(self.flight.current_passengers, 1)

    def test_aircraft_maintenance_check(self):
        self.assertFalse(self.aircraft.needs_maintenance())

    def test_payment_account_operations(self):
        new_balance = self.payment_account.deposit(10000)
        self.assertEqual(new_balance, 60000)
        new_balance = self.payment_account.withdraw(15000)
        self.assertEqual(new_balance, 45000)
        with self.assertRaises(InsufficientFundsError):
            self.payment_account.withdraw(100000)

    def test_airport_capacity(self):
        self.assertTrue(self.airport.check_capacity())
        self.airport.current_occupancy = 10000
        self.assertFalse(self.airport.check_capacity())

    def test_safety_inspection(self):
        inspection = SafetyInspection("INS001", self.aircraft, "Иванов", datetime.now(), True)
        result = inspection.assess_safety_risk()
        self.assertEqual(result, "Низкий риск безопасности")
        failed_inspection = SafetyInspection("INS002", self.aircraft, "Петров", datetime.now(), False)
        with self.assertRaises(SafetyRiskError):
            failed_inspection.assess_safety_risk()


    def test_booking_application_approval(self):
        application = BookingApplication("APP001", self.passenger, "business", 2, "окно")
        self.passenger.credit_score = 750
        result = application.process()
        self.assertEqual(result, "Бронирование одобрено")
        self.assertEqual(application.status, "approved")

    def test_booking_application_denial(self):
        application = BookingApplication("APP002", self.passenger, "first", 3, "ряд у выхода")
        self.passenger.credit_score = 550
        with self.assertRaises(BookingDeniedError):
            application.process()
        self.assertEqual(application.status, "pending")


class TestSecuritySystems(unittest.TestCase):

    def setUp(self):
        self.security_check = SecurityCheck("SEC001", "active", "high", 3, 300)

    def test_security_check_success(self):
        result = self.security_check.authenticate_passenger("AB123456", "TK789012")
        self.assertTrue(result)

    def test_security_check_too_many_attempts(self):
        self.security_check.failed_attempts = 3
        with self.assertRaises(AuthenticationError):
            self.security_check.authenticate_passenger("AB123456", "wrong_ticket")

    def test_document_validation(self):
        validator = DocumentValidator("DOC001", "active", "strict", ["паспорт", "виза"])
        future_date = datetime.now() + timedelta(days=365)
        self.assertTrue(validator.validate_documents(future_date))
        expired_date = datetime.now() + timedelta(days=30)
        with self.assertRaises(SecurityBreachError):
            validator.validate_documents(expired_date)


if __name__ == "__main__":
    unittest.main()
"""
Демонстрация 30 ассоциаций между классами
"""

# 1. Passenger имеет Booking
# 2. Flight имеет множество Passenger
# 3. Pilot управляет Aircraft
# 4. Aircraft принадлежит Airline
# 5. Booking ссылается на Flight
# 6. Payment связан с Booking
# 7. Airport обслуживает множество Flight
# 8. FlightAttendant работает на Flight
# 9. SafetyInspection проверяет Aircraft
# 10. GroupBooking содержит множество Passenger
# 11. FlightSchedule планирует Flight
# 12. VIPPassenger наследует Passenger
# 13. CorporateBooking ссылается на Company
# 14. Transaction изменяет PaymentAccount
# 15. MoneyTransfer связывает два PaymentAccount
# 16. SecurityCheck аутентифицирует Passenger
# 17. DocumentValidator проверяет документы Passenger
# 18. BookingApplication создает Booking
# 19. AircraftMaintenance обслуживает Aircraft
# 20. FlightTracker отслеживает Flight
# 21. LoyaltyProgram начисляет мили Passenger
# 22. Cargo перевозится Flight
# 23. FlightChallenge вовлекает Passenger
# 24. LoungeAccess предоставляется Passenger
# 25. InFlightService предлагается во время Flight
# 26. AirlineApp используется Passenger
# 27. FlightPlan содержит множество Flight
# 28. Baggage принадлежит Passenger
# 29. FlightReport анализирует Flight
# 30. EmergencyProcedure тренируется на Aircraft

# Новые ассоциации из добавленных классов:
# 31. FlightRoute определяет маршрут для Flight
# 32. BoardingPass выдается для Passenger на Flight
# 33. FuelManagement управляет топливом Aircraft
# 34. CrewScheduling назначает экипаж на Flight
# 35. WeatherService предоставляет данные для Airport
# 36. BaggageHandler обрабатывает Baggage
# 37. FlightSimulator тренирует Pilot
# 38. CustomerService помогает Passenger
# 39. AirTrafficControl управляет Flight
# 40. FinancialDepartment оплачивает услуги
class VIPPassenger:
    def __init__(self, name, surname, passenger_id, phone, email, age, passport_number, vip_level, personal_assistant):
        self.name = name
        self.surname = surname
        self.passenger_id = passenger_id
        self.phone = phone
        self.email = email
        self.age = age
        self.passport_number = passport_number
        self.vip_level = vip_level
        self.personal_assistant = personal_assistant
        self.exclusive_services = []

    def request_exclusive_service(self, service_name):
        result = f"Услуга {service_name} заказана для VIP пассажира"
        self.exclusive_services.append(service_name)
        return result
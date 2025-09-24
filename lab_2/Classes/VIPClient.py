from Customer import Customer
from datetime import datetime, timedelta


class VIPClient(Customer):
    def __init__(self, name, surname, passport_id, phone_number, email, vip_status, personal_manager):
        super().__init__(name, surname, passport_id, phone_number, email)
        self.vip_status = vip_status  # platinum, gold, silver
        self.personal_manager = personal_manager
        self.exclusive_services = []
        self.priority_support = True
        # ДОБАВЛЕННЫЕ ПОЛЯ:
        self.vip_since = datetime.now().date()
        self.wealth_tier = "high"  # high, ultra-high, premium
        self.concierge_available = True
        self.private_banker = None
        self.vip_lounge_access = True
        self.investment_portfolio_value = 0.0
        self.family_members = []  # Семейные счета
        self.dedicated_phone_line = f"+7-800-VIP-{passport_id[-4:]}"
        self.travel_benefits = {
            'airport_lounge': True,
            'private_jet_discount': False,
            'hotel_upgrades': True
        }
        self.entertainment_benefits = {
            'event_tickets': 4,  # Билетов в месяц
            'fine_dining_discount': True,
            'yacht_rental': False
        }
        self.credit_limit_multiplier = 3.0  # Множитель стандартного лимита
        self.emergency_contact_24_7 = True
        self.financial_advisor = None
        self.estate_planning_included = False

    # ДОБАВЛЕННЫЕ МЕТОДЫ:
    def assign_private_banker(self, banker):
        """Назначить персонального банкира"""
        self.private_banker = banker
        return f"Персональный банкир {banker.name} назначен"

    def activate_concierge_service(self, service_type="premium"):
        """Активировать консьерж-сервис"""
        self.concierge_available = True
        exclusive_services = {
            "premium": ["билеты на мероприятия", "бронирование ресторанов", "организация путешествий"],
            "ultra": ["доступ к частным клубам", "персональный шоппер", "организация ивентов"]
        }
        self.exclusive_services.extend(exclusive_services.get(service_type, []))
        return f"Консьерж-сервис уровня {service_type} активирован"

    def request_wealth_management(self, portfolio_size):
        """Запросить управление состоянием"""
        if portfolio_size < 10000000:  # 10 млн минимально
            raise ValueError("Минимальный портфель для управления - 10 млн")

        self.investment_portfolio_value = portfolio_size
        self.financial_advisor = self.personal_manager
        return f"Управление портфелем {portfolio_size} руб. активировано"

    def add_family_member(self, family_member):
        """Добавить члена семьи для семейного банкинга"""
        if len(self.family_members) >= 5:
            raise ValueError("Превышен лимит членов семьи")
        self.family_members.append(family_member)
        return f"Член семьи {family_member.name} добавлен"

    def request_emergency_support(self, emergency_type):
        """Запросить экстренную поддержку 24/7"""
        if not self.emergency_contact_24_7:
            raise ValueError("Экстренная поддержка не доступна для вашего тарифа")

        responses = {
            "lost_card": "Блокировка карты выполнена, новая карта будет доставлена в течение 2 часов",
            "cash_emergency": "Доступ к наличным до 500,000 руб. в любом отделении",
            "travel_assistance": "Организована помощь в поездке, контакты местного банка предоставлены"
        }
        return responses.get(emergency_type, "Экстренная помощь активирована")

    def upgrade_vip_status(self, new_status):
        """Повысить VIP статус"""
        status_hierarchy = ["silver", "gold", "platinum", "diamond"]
        current_index = status_hierarchy.index(self.vip_status)
        new_index = status_hierarchy.index(new_status)

        if new_index <= current_index:
            raise ValueError("Можно повысить только на более высокий статус")

        self.vip_status = new_status
        self.credit_limit_multiplier += 0.5
        return f"Статус повышен до {new_status}. Новый кредитный лимит: x{self.credit_limit_multiplier}"

    def schedule_private_meeting(self, meeting_topic, preferred_date):
        """Запланировать приватную встречу"""
        available_topics = ["инвестиции", "наследство", "бизнес-планирование", "налоги"]
        if meeting_topic not in available_topics:
            raise ValueError("Тема встречи не доступна")

        return f"Приватная встреча на тему '{meeting_topic}' запланирована на {preferred_date}"

    def calculate_vip_benefits_value(self):
        """Рассчитать стоимость VIP benefits"""
        benefits_value = {
            "platinum": 500000,  # руб/год
            "gold": 250000,
            "silver": 100000
        }
        base_value = benefits_value.get(self.vip_status, 0)
        additional_value = len(self.exclusive_services) * 50000
        return base_value + additional_value

    def request_event_tickets(self, event_name, quantity=2):
        """Запросить билеты на мероприятие"""
        if quantity > self.entertainment_benefits['event_tickets']:
            raise ValueError(f"Превышен лимит билетов. Доступно: {self.entertainment_benefits['event_tickets']}")

        self.entertainment_benefits['event_tickets'] -= quantity
        return f"Билеты на {event_name} (x{quantity}) зарезервированы"

    def __str__(self):
        return f"{super().__str__()}, VIP статус: {self.vip_status}, Менеджер: {self.personal_manager.name}"

    # Дополнительные свойства
    @property
    def vip_duration_days(self):
        """Количество дней как VIP клиент"""
        return (datetime.now().date() - self.vip_since).days

    @property
    def total_benefits_value(self):
        """Общая стоимость benefits"""
        return self.calculate_vip_benefits_value()
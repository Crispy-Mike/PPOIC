class AirlineApp:
    def __init__(self, app_id, name, version, supported_platforms):
        self.app_id = app_id
        self.name = name
        self.version = version
        self.supported_platforms = supported_platforms
        self.users = []

    def add_user(self, passenger):
        self.users.append(passenger)
        return f"Пользователь {passenger.name} добавлен в приложение"
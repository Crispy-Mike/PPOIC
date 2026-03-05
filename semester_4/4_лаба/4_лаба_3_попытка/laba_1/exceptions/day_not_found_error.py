
class DayNotFoundError(Exception):

    def __init__(self, day_name):
        self.day_name = day_name
        super().__init__(f"День '{day_name}' не найден в расписании")
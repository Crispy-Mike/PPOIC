
class InvalidMarkError(Exception):

    def __init__(self, mark_value):
        self.mark_value = mark_value
        super().__init__(f"Некорректная оценка: {mark_value}. Оценка должна быть от 1 до 10")
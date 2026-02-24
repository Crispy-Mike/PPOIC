
class InvalidMenuChoiceError(Exception):

    def __init__(self, choice, valid_choices):
        self.choice = choice
        self.valid_choices = valid_choices
        super().__init__(f"Неверный выбор: '{choice}'. Ожидается: {valid_choices}")
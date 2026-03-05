
class EmptyNameError(Exception):


    def __init__(self, field_name):
        self.field_name = field_name
        super().__init__(f"Поле '{field_name}' не может быть пустым")

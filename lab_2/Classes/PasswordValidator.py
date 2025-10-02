import SecuritySystem
from exceptions.SecurityBreachError import SecurityBreachError
class PasswordValidator(SecuritySystem):
    def __init__(self, system_id, status, security_level, min_length, require_complexity):
        super().__init__(system_id, "password_validation", status, security_level)
        self.min_length = min_length
        self.require_complexity = require_complexity

    def validate_password(self, password):
        if len(password) < self.min_length:
            raise SecurityBreachError("Пароль слишком короткий")
        return True


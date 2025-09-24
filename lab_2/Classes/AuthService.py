# Classes/AuthService.py

from .SecuritySystem import SecuritySystem  # Используйте относительный импорт

class AuthenticationError(Exception):
    """Исключение для ошибок аутентификации"""
    pass

class AuthService(SecuritySystem):
    def __init__(self, system_id, status, security_level, max_attempts, timeout_duration):
        super().__init__(system_id, "authentication", status, security_level)
        self.max_attempts = max_attempts
        self.timeout_duration = timeout_duration
        self.two_factor_enabled = True
        self.failed_attempts = 0

    def authenticate_user(self, username, password):
        if self.failed_attempts >= self.max_attempts:
            raise AuthenticationError("Слишком много неудачных попыток")
        # Логика аутентификации
        return True
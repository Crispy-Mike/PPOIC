import SecuritySystem
from exceptions.SecurityBreachError import SecurityBreachError
class AccessControl(SecuritySystem):
    def __init__(self, system_id, status, security_level, access_levels):
        super().__init__(system_id, "access_control", status, security_level)
        self.access_levels = access_levels
        self.access_log = []

    def grant_access(self, user, area):
        """Предоставить доступ"""
        if user.access_level not in self.access_levels.get(area, []):
            raise SecurityBreachError("Доступ запрещен")
        self.access_log.append(f"{user} accessed {area}")
        return "Access granted"

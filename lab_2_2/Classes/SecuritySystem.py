
class SecuritySystem:
    def __init__(self, system_id, system_type, status, security_level):
        self.system_id = system_id
        self.system_type = system_type
        self.status = status
        self.security_level = security_level
        self.last_maintenance = None

    def perform_maintenance(self):
       #Выполнить техническое обслужива
        self.last_maintenance = "now"
        return "Maintenance performed"


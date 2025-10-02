import SystemAdmin

class NetworkAdmin(SystemAdmin):
    def __init__(self, name, surname, employee_id, salary, hire_date, admin_rights, systems_managed,
                 network_certifications):
        super().__init__(name, surname, employee_id, salary, hire_date, admin_rights, systems_managed)
        self.position = "Сетевой администратор"
        self.network_certifications = network_certifications


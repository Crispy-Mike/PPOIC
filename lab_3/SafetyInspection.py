from exceptions import SafetyRiskError

class SafetyInspection:
    def __init__(self, inspection_id, aircraft, inspector, inspection_date, passed):
        self.inspection_id = inspection_id
        self.aircraft = aircraft
        self.inspector = inspector
        self.inspection_date = inspection_date
        self.passed = passed
        self.notes = ""

    def assess_safety_risk(self):
        if not self.passed:
            raise SafetyRiskError("Самолет не прошел проверку безопасности")
        return "Низкий риск безопасности"
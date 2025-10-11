import SecuritySystem
from exceptions.SecurityBreachError import SecurityBreachError


class FraudDetector(SecuritySystem):
    def __init__(self, system_id, status, security_level, detection_threshold):
        super().__init__(system_id, "fraud_detection", status, security_level)
        self.detection_threshold = detection_threshold
        self.suspicious_activities = []

    def detect_fraud(self, transaction):
        """Обнаружить мошенничество"""
        if transaction.amount > self.detection_threshold:
            self.suspicious_activities.append(transaction)
            raise SecurityBreachError("Подозрительная транзакция обнаружена")
        return "Transaction safe"


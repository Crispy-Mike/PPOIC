from datetime import datetime, timedelta
from exceptions import SecurityBreachError

class DocumentValidator:
    def __init__(self, validator_id, status, validation_level, required_documents):
        self.validator_id = validator_id
        self.status = status
        self.validation_level = validation_level
        self.required_documents = required_documents
        self.min_passport_validity = 6  # месяцев

    def validate_documents(self, passport_expiry, visa_required=False, visa_valid=False):
        if (datetime.now() + timedelta(days=30*self.min_passport_validity)) > passport_expiry:
            raise SecurityBreachError("Паспорт истекает слишком скоро")
        if visa_required and not visa_valid:
            raise SecurityBreachError("Требуется действительная виза")
        return True
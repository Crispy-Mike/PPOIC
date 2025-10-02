import Transaction
from datetime import datetime


class Withdrawal(Transaction):
    def __init__(self, transaction_id, amount, currency, description, account, location):
        super().__init__(transaction_id, amount, currency, description)
        self.account = account
        self.location = location
        # ДОБАВЛЕННЫЕ ПОЛЯ:
        self.withdrawal_method = "cash"  # cash, transfer, check
        self.transaction_fee = 0.0
        self.receipt_number = f"RCP{transaction_id}"
        self.is_verified = False
        self.verification_method = None  # signature, pin, biometric
        self.daily_withdrawal_count = 1
        self.atm_id = None if not hasattr(location, 'atm_id') else location.atm_id
        self.branch_code = None if not hasattr(location, 'branch_code') else location.branch_code
        self.cash_denominations = {}  # {1000: 5, 500: 10} - номиналы выданных купюр
        self.withdrawal_purpose = "personal"  # personal, business, travel
        self.exchange_rate_applied = 1.0
        self.tax_reference = None
        self.is_urgent = False
        self.confirmation_code = None

    # ДОБАВЛЕННЫЕ МЕТОДЫ:
    def apply_transaction_fee(self, fee_percentage=0.01):
        """Применить комиссию за снятие"""
        fee = self.amount * fee_percentage
        self.transaction_fee = fee
        self.amount += fee  # Комиссия добавляется к сумме снятия
        return f"Комиссия {fee} {self.currency} применена"

    def verify_withdrawal(self, verification_method="pin"):
        """Верифицировать операцию снятия"""
        self.is_verified = True
        self.verification_method = verification_method
        return f"Снятие верифицировано методом: {verification_method}"

    def set_cash_denominations(self, denominations_dict):
        """Установить номиналы выданных купюр"""
        self.cash_denominations = denominations_dict
        total = sum(denom * count for denom, count in denominations_dict.items())
        if total != self.amount:
            raise ValueError("Сумма номиналов не совпадает с суммой снятия")
        return "Номиналы установлены"

    def generate_receipt(self):
        """Сгенерировать детализированный чек"""
        receipt = f"""
        Чек операции снятия #{self.receipt_number}
        Счет: {self.account.account_number}
        Сумма: {self.amount} {self.currency}
        Комиссия: {self.transaction_fee} {self.currency}
        Место: {self.location}
        Время: {self.timestamp if self.timestamp else datetime.now()}
        Метод верификации: {self.verification_method}
        Номиналы: {self.cash_denominations}
        """
        return receipt

    def check_daily_limit(self, daily_limit=100000):
        """Проверить не превышен ли дневной лимит"""
        today_withdrawals = [w for w in self.account.transactions
                             if
                             isinstance(w, Withdrawal) and w.timestamp and w.timestamp.date() == datetime.now().date()]
        total_today = sum(w.amount for w in today_withdrawals)

        if total_today + self.amount > daily_limit:
            raise ValueError(f"Превышен дневной лимит снятия. Доступно: {daily_limit - total_today}")
        return f"Лимит проверен, можно снять {self.amount}"

    def process_urgent_withdrawal(self, urgency_reason):
        """Обработать срочное снятие"""
        self.is_urgent = True
        self.transaction_fee *= 2  # Удвоенная комиссия за срочность
        return f"Срочное снятие обработано. Причина: {urgency_reason}"

    def cancel_withdrawal(self):
        """Отменить операцию снятия"""
        if self.status == "completed":
            raise ValueError("Невозможно отменить завершенную операцию")
        self.status = "cancelled"
        return "Снятие отменено"

    def get_tax_information(self):
        """Получить налоговую информацию по операции"""
        if self.amount > 600000:  # Лимит для налоговой отчетности
            self.tax_reference = f"TAX{self.transaction_id}"
            return f"Требуется налоговая отчетность. Референс: {self.tax_reference}"
        return "Налоговая отчетность не требуется"

    def __str__(self):
        return f"Снятие {self.amount} {self.currency} со счета {self.account.account_number}"
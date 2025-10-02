import Report

class FinancialReport(Report):
    def __init__(self, report_id, generation_date, data, period):
        super().__init__(report_id, "financial", generation_date, data)
        self.period = period
        self.revenue = 0
        self.expenses = 0

    def calculate_profit(self):
        """Рассчитать прибыль"""
        return self.revenue - self.expenses

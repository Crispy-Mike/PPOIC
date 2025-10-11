
class Report:
    def __init__(self, report_id, report_type, generation_date, data):
        self.report_id = report_id
        self.report_type = report_type
        self.generation_date = generation_date
        self.data = data

    def generate_report(self):
        """Сгенерировать отчет"""
        return f"Отчет {self.report_type} сгенерирован"

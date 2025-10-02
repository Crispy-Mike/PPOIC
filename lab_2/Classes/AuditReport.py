from Classes.Report import Report

class AuditReport(Report):
    def __init__(self, report_id, generation_date, data, auditor):
        super().__init__(report_id, "audit", generation_date, data)
        self.auditor = auditor
        self.findings = []
        self.recommendations = []

    def add_finding(self, finding):
        """Добавить находку аудита"""
        self.findings.append(finding)


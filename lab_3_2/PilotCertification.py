from datetime import datetime

class PilotCertification:
    def __init__(self, certification_id, pilot, certification_name, issuing_authority, issue_date, expiry_date):
        self.certification_id = certification_id
        self.pilot = pilot
        self.certification_name = certification_name
        self.issuing_authority = issuing_authority
        self.issue_date = issue_date
        self.expiry_date = expiry_date
        self.valid = True

    def check_validity(self):
        if datetime.now() > self.expiry_date:
            self.valid = False
        return self.valid
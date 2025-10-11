
class EmailNotification(Notification):
    def __init__(self, notification_id, recipient, message, email_address):
        super().__init__(notification_id, recipient, message, "Email")
        self.email_address = email_address

    def send_email(self):
        """Отправить email"""
        return f"Email отправлен на {self.email_address}"


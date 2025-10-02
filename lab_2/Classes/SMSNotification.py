import Notification
class SMSNotification(Notification):
    def __init__(self, notification_id, recipient, message, phone_number):
        super().__init__(notification_id, recipient, message, "SMS")
        self.phone_number = phone_number

    def send_sms(self):
        """Отправить SMS"""
        return f"SMS отправлено на {self.phone_number}"


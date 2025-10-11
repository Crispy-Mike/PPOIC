
class Notification:
    def __init__(self, notification_id, recipient, message, notification_type):
        self.notification_id = notification_id
        self.recipient = recipient
        self.message = message
        self.notification_type = notification_type
        self.status = "sent"

    def send_notification(self):
        """Отправить уведомление"""
        return f"Уведомление отправлено {self.recipient}"

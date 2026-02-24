import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import string


class EmailSender:
    def __init__(self, smtp_server="smtp.gmail.com", smtp_port=587,
                 sender_email="your_email@gmail.com", sender_password="your_app_password"):

        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password

    def send_verification_code(self, recipient_email, code):
        """Отправка кода подтверждения на email"""
        subject = "Hangman Game - Подтверждение регистрации"

        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; background-color: white; 
                        border-radius: 10px; padding: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                <h1 style="color: #333; text-align: center; border-bottom: 2px solid #4CAF50; padding-bottom: 10px;">
                    Hangman Game
                </h1>

                <p style="font-size: 16px; color: #555; line-height: 1.6;">
                    Здравствуйте!
                </p>

                <p style="font-size: 16px; color: #555; line-height: 1.6;">
                    Благодарим вас за регистрацию в игре Hangman. 
                    Для подтверждения вашего email-адреса используйте следующий код:
                </p>

                <div style="background-color: #f0f8ff; border-left: 4px solid #4CAF50; 
                            padding: 15px; margin: 20px 0; text-align: center;">
                    <span style="font-size: 32px; font-weight: bold; color: #333; 
                                 letter-spacing: 5px; font-family: monospace;">
                        {code}
                    </span>
                </div>

                <p style="font-size: 16px; color: #555; line-height: 1.6;">
                    Код действителен в течение 24 часов. Если вы не регистрировались в игре, 
                    просто проигнорируйте это письмо.
                </p>

                <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">

                <p style="font-size: 14px; color: #999; text-align: center;">
                    © 2024 Hangman Game. Все права защищены.
                </p>
            </div>
        </body>
        </html>
        """

        return self.send_email(recipient_email, subject, body)

    def send_email(self, recipient_email, subject, body):
        """Отправка email"""
        try:
            # Создаем сообщение
            msg = MIMEMultipart('alternative')
            msg['From'] = self.sender_email
            msg['To'] = recipient_email
            msg['Subject'] = subject

            # Добавляем HTML версию письма
            html_part = MIMEText(body, 'html')
            msg.attach(html_part)

            # Подключаемся к серверу и отправляем
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)

            return {"success": True, "message": "Email отправлен"}

        except Exception as e:
            print(f"Ошибка отправки email: {e}")
            return {"success": False, "error": str(e)}

    def send_test_email(self, recipient_email):
        """Отправка тестового email (для демо-режима)"""
        print(f"\n=== ТЕСТОВЫЙ РЕЖИМ: Email отправлен на {recipient_email} ===")
        print("Код подтверждения: 123456")
        print("=========================================\n")

        return {"success": True, "code": "123456"}


# Функция для создания демо-отправителя (без реальной отправки)
def create_demo_email_sender():
    """Создает отправитель email в демо-режиме"""

    class DemoEmailSender:
        def send_verification_code(self, recipient_email, code):
            print(f"\n=== ДЕМО РЕЖИМ: Код подтверждения для {recipient_email} ===")
            print(f"Код: {code}")
            print("=========================================\n")
            return {"success": True, "code": code}

    return DemoEmailSender()
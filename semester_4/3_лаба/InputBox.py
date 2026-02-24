import pygame
#НАДО БУДЕТ ЗАМЕНИТЬ НА БАЗУ ДАННЫХ
#ЭТИ ПЕРЕМЕННЫЕ СНИЗУ
MAILS=[]
LOGINS=[]
class InputBox:
    def __init__(self, x, y, width, height, screen, field_type="text", placeholder=""):
        self.rect = pygame.Rect(x, y, width, height)
        self.placeholder = placeholder
        self.field_type = field_type
        self.text = ""
        self.screen = screen
        self.active = False
        self.error = False
        self.error_message = ""
        self.max_length = 20
        self.is_password = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            return  # Добавил return для ясности

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:  # ИСПРАВЛЕНО: было event.type
                self.text = self.text[:-1]
            elif len(self.text) < self.max_length and event.unicode.isprintable():
                self.text += event.unicode

    def draw(self, font):
        # Цвет рамки
        if self.error:
            border_color = (255, 100, 100)  # красный при ошибке
        elif self.active:
            border_color = (100, 255, 100)  # зеленый при активации
        else:
            border_color = (200, 200, 200)  # серый обычно

        # Рисуем фон и рамку
        pygame.draw.rect(self.screen, (255, 255, 255), self.rect)
        pygame.draw.rect(self.screen, border_color, self.rect, 2)

        # Рисуем текст
        if self.text:
            if self.is_password:
                display_text = "*" * len(self.text)
            else:
                display_text = self.text
            text_surface = font.render(display_text, True, (0, 0, 0))
        else:
            text_surface = font.render(self.placeholder, True, (150, 150, 150))

        self.screen.blit(text_surface, (self.rect.x + 10, self.rect.y + 15))

    def check_mail(self, email):
        all_domains = [
            "mail.ru",
            "bk.ru",
            "list.ru",
            "inbox.ru",
            "gmail.com",
            "yandex.ru",
            "ya.ru",
            "rambler.ru",
            "lenta.ru",
            "outlook.com",
            "hotmail.com",
            "live.com",
            "msn.com",
            "yahoo.com",
            "icloud.com",
            "me.com",
            "mac.com",
            "aol.com",
            "protonmail.com",
            "proton.me",
            "zoho.com",
            "tutanota.com",
            "gmx.com",
            "mail.com",
            "inbox.com",
            "yandex.ua",
            "yandex.by",
            "yandex.kz",
            "ukr.net",
            "meta.ua",
            "i.ua",
            "mail.ua",
            "bigmir.net",
            "tut.by",
            "mail.ru",
            "inbox.ru",
            "list.ru",
            "bk.ru",
            "internet.ru",
            "mail.ua"
        ]
        if not any (email.endswith(domain) for domain in all_domains):
            self.error = True
        if email in MAILS:
            self.error=True
        else:
            self.error=False


    def check_password(self):
        pass

    def check_login(self,login):
        if login in LOGINS:
            self.error = True
        self.error = False
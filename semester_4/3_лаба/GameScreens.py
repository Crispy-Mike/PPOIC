import pygame
import random


class GameScreens:
    def __init__(self, screen):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()

    # ========== ГЛАВНОЕ МЕНЮ ==========
    def draw_main_menu(self, buttons):
        # Футуристический фон для главного меню
        self.screen.fill((20, 20, 40))  # темно-синий

        # Звезды
        for _ in range(100):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            brightness = random.randint(100, 255)
            pygame.draw.circle(self.screen, (brightness, brightness, brightness), (x, y), 1)

        # Падающие звезды (анимация)
        time = pygame.time.get_ticks() / 1000
        for i in range(3):
            x = (time * 50 + i * 200) % self.width
            y = (time * 30 + i * 100) % self.height
            pygame.draw.line(self.screen, (255, 255, 150), (x, y), (x - 20, y + 20), 2)

        # Заголовок
        font_big = pygame.font.Font(None, 72)
        title = font_big.render("HANGMAN", True, (255, 215, 0))  # золотой
        title_shadow = font_big.render("HANGMAN", True, (100, 50, 0))

        title_rect = title.get_rect(center=(self.width // 2, 100))
        shadow_rect = title_rect.copy()
        shadow_rect.x += 5
        shadow_rect.y += 5

        self.screen.blit(title_shadow, shadow_rect)
        self.screen.blit(title, title_rect)

        # Подзаголовок
        font_small = pygame.font.Font(None, 36)
        subtitle = font_small.render("Classic Word Guessing Game", True, (200, 200, 255))
        subtitle_rect = subtitle.get_rect(center=(self.width // 2, 170))
        self.screen.blit(subtitle, subtitle_rect)

        # Рисуем кнопки (будут переданы из основного кода)
        for button in buttons:
            button.draw(self.screen)

    # ========== ВЫБОР ОФФЛАЙН УРОВНЯ ==========
    def draw_offline_level_selection(self, buttons):
        # Теплый, уютный фон для оффлайн игры
        self.screen.fill((255, 248, 220))  # цвет слоновой кости

        # Книжные полки на заднем плане
        for i in range(0, self.width, 120):
            # Корешки книг
            colors = [(139, 69, 19), (128, 0, 0), (85, 107, 47), (70, 130, 180)]
            for j, color in enumerate(colors):
                pygame.draw.rect(self.screen, color,
                                 (i + j * 5, 250, 20, 150))
                # Названия книг (белые линии)
                pygame.draw.line(self.screen, (255, 255, 255),
                                 (i + j * 5 + 5, 300), (i + j * 5 + 15, 300), 2)

        # Парящие буквы
        font = pygame.font.Font(None, 40)
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        for i, letter in enumerate(letters):
            x = (i * 30) % self.width
            y = 400 + (i * 10) % 100
            if random.random() > 0.7:  # некоторые буквы парят
                text = font.render(letter, True, (200, 200, 200, 100))
                self.screen.blit(text, (x, y))

        # Заголовок
        font_big = pygame.font.Font(None, 60)
        title = font_big.render("OFFLINE MODE", True, (50, 50, 50))
        title_rect = title.get_rect(center=(self.width // 2, 100))
        self.screen.blit(title, title_rect)

        subtitle = pygame.font.Font(None, 30).render("Choose Difficulty", True, (100, 100, 100))
        subtitle_rect = subtitle.get_rect(center=(self.width // 2, 150))
        self.screen.blit(subtitle, subtitle_rect)

        # Рисуем кнопки уровней
        for button in buttons:
            button.draw(self.screen)

    # ========== ВЫБОР ОНЛАЙН УРОВНЯ ==========
    def draw_online_level_selection(self, buttons):
        # Технологичный фон для онлайн игры
        self.screen.fill((0, 0, 20))  # почти черный

        # Сетка как в киберпространстве
        for i in range(0, self.width, 50):
            color = (0, random.randint(50, 100), random.randint(100, 200))
            pygame.draw.line(self.screen, color, (i, 0), (i, self.height), 1)
            pygame.draw.line(self.screen, color, (0, i), (self.width, i), 1)

        # Движущиеся точки по сетке
        time = pygame.time.get_ticks() / 500
        for i in range(10):
            x = (time * 30 + i * 80) % self.width
            y = (time * 20 + i * 60) % self.height
            pygame.draw.circle(self.screen, (0, 255, 255), (int(x), int(y)), 3)

        # Заголовок
        font_big = pygame.font.Font(None, 60)
        title = font_big.render("ONLINE MODE", True, (0, 255, 255))  # циан
        title_rect = title.get_rect(center=(self.width // 2, 100))

        # Эффект мерцания
        if random.random() > 0.5:
            glow = font_big.render("ONLINE MODE", True, (255, 255, 255))
            self.screen.blit(glow, (title_rect.x - 2, title_rect.y - 2))

        self.screen.blit(title, title_rect)

        subtitle = pygame.font.Font(None, 30).render("Select Server Region", True, (100, 255, 255))
        subtitle_rect = subtitle.get_rect(center=(self.width // 2, 150))
        self.screen.blit(subtitle, subtitle_rect)

        # Рисуем кнопки
        for button in buttons:
            button.draw(self.screen)

    # ========== ПОИСК ПРОТИВНИКА ==========
    def draw_searching_opponent(self):
        # Анимированный фон поиска
        self.screen.fill((0, 0, 30))

        # Радар
        center_x = self.width // 2
        center_y = self.height // 2 - 50

        # Круги радара
        for radius in [50, 100, 150, 200]:
            pygame.draw.circle(self.screen, (0, 100, 0), (center_x, center_y), radius, 1)

        # Линии радара
        pygame.draw.line(self.screen, (0, 100, 0), (center_x - 200, center_y), (center_x + 200, center_y), 1)
        pygame.draw.line(self.screen, (0, 100, 0), (center_x, center_y - 200), (center_x, center_y + 200), 1)

        # Вращающаяся линия радара
        time = pygame.time.get_ticks() / 1000
        angle = time * 2  # скорость вращения
        end_x = center_x + 180 * pygame.math.Vector2(1, 0).rotate(angle * 57.3)[0]
        end_y = center_y + 180 * pygame.math.Vector2(1, 0).rotate(angle * 57.3)[1]
        pygame.draw.line(self.screen, (0, 255, 0), (center_x, center_y), (end_x, end_y), 2)

        # "Противники" на радаре (мигающие точки)
        if random.random() > 0.7:
            for i in range(3):
                x = center_x + random.randint(-150, 150)
                y = center_y + random.randint(-150, 150)
                pygame.draw.circle(self.screen, (255, 0, 0), (x, y), 5)

        # Текст поиска
        font_big = pygame.font.Font(None, 48)
        searching_text = font_big.render("SEARCHING FOR OPPONENT", True, (0, 255, 0))
        text_rect = searching_text.get_rect(center=(self.width // 2, self.height - 150))
        self.screen.blit(searching_text, text_rect)

        # Анимированные точки
        dots = "." * (int(time * 2) % 4)
        dots_text = font_big.render(dots, True, (0, 255, 0))
        dots_rect = dots_text.get_rect(center=(self.width // 2 + 150, self.height - 150))
        self.screen.blit(dots_text, dots_rect)

        # Статистика поиска
        font_small = pygame.font.Font(None, 30)
        stats = [
            f"Players Online: {random.randint(100, 1000)}",
            f"Your Rank: #{random.randint(1, 100)}",
            f"Est. Time: {random.randint(5, 30)}s"
        ]
        for i, stat in enumerate(stats):
            text = font_small.render(stat, True, (100, 255, 100))
            text_rect = text.get_rect(center=(self.width // 2, self.height - 80 + i * 25))
            self.screen.blit(text, text_rect)

    # ========== ФОН ДЛЯ ОФФЛАЙН ИГРЫ ==========
    def draw_offline_game_background(self):
        # Уютный фон для самой игры
        self.screen.fill((245, 245, 220))  # бежевый

        # Тетрадные линии
        for i in range(0, self.height, 30):
            pygame.draw.line(self.screen, (200, 200, 255), (0, i), (self.width, i), 1)

        # Красная линия полей
        pygame.draw.line(self.screen, (255, 100, 100), (50, 0), (50, self.height), 2)

        # Рисунки в углах (для уюта)
        # Лампочка в углу
        pygame.draw.circle(self.screen, (255, 255, 200), (50, 50), 20)
        pygame.draw.line(self.screen, (100, 100, 100), (50, 70), (50, 100), 3)

        # Карандаши
        for i in range(3):
            x = 700 + i * 30
            pygame.draw.rect(self.screen, (255, 215, 0), (x, 500, 10, 60))
            pygame.draw.polygon(self.screen, (0, 0, 0), [(x, 500), (x + 5, 490), (x + 10, 500)])

    # ========== ФОН ДЛЯ ОНЛАЙН ИГРЫ ==========
    def draw_online_game_background(self):
        # Киберпанк фон для онлайн игры
        self.screen.fill((10, 10, 20))

        # Цифровой дождь (как в Матрице)
        font = pygame.font.Font(None, 20)
        time = pygame.time.get_ticks() / 100

        for i in range(0, self.width, 20):
            length = random.randint(5, 15)
            for j in range(length):
                y = (time * 2 + i + j * 20) % self.height
                if random.random() > 0.95:
                    char = random.choice("01")
                    text = font.render(char, True, (0, 255, 0))
                    self.screen.blit(text, (i, y))

        # Горизонтальные линии сканирования
        for i in range(0, self.height, 50):
            alpha = random.randint(0, 50)
            pygame.draw.line(self.screen, (0, 255, 255, alpha), (0, i), (self.width, i), 1)
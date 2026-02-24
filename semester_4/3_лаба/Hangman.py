import pygame

class Hangman:
    def __init__(self, x, y, screen):
        self.x = x
        self.y = y
        self.screen = screen
        self.errors = 0
        self.max_errors = 7  # По умолчанию

    def add_error(self):
        self.errors += 1

    def draw_gallows_base(self):
        # Основание
        pygame.draw.line(self.screen, (0, 0, 0), (50 + self.x, 250 + self.y),
                         (200 + self.x, 250 + self.y), 3)
        # Столб
        pygame.draw.line(self.screen, (0, 0, 0), (100 + self.x, 250 + self.y),
                         (100 + self.x, 50 + self.y), 3)
        # Перекладина
        pygame.draw.line(self.screen, (0, 0, 0), (100 + self.x, 50 + self.y),
                         (200 + self.x, 50 + self.y), 3)
        # Веревка
        pygame.draw.line(self.screen, (0, 0, 0), (200 + self.x, 50 + self.y),
                         (200 + self.x, 80 + self.y), 3)

    def draw_head(self):
        pygame.draw.circle(self.screen, (0, 0, 0),
                           (200 + self.x, 100 + self.y), 15, 2)

    def draw_body(self):
        pygame.draw.line(self.screen, (0, 0, 0),
                         (200 + self.x, 115 + self.y),
                         (200 + self.x, 170 + self.y), 2)

    def draw_left_arm(self):
        pygame.draw.line(self.screen, (0, 0, 0),
                         (200 + self.x, 130 + self.y),
                         (170 + self.x, 150 + self.y), 2)

    def draw_right_arm(self):
        pygame.draw.line(self.screen, (0, 0, 0),
                         (200 + self.x, 130 + self.y),
                         (230 + self.x, 150 + self.y), 2)

    def draw_left_leg(self):
        pygame.draw.line(self.screen, (0, 0, 0),
                         (200 + self.x, 170 + self.y),
                         (170 + self.x, 210 + self.y), 2)

    def draw_right_leg(self):
        pygame.draw.line(self.screen, (0, 0, 0),
                         (200 + self.x, 170 + self.y),
                         (230 + self.x, 210 + self.y), 2)
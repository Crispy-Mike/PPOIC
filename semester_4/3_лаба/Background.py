import pygame
import random


class Background:
    def draw_background_notebook(screen):
        # Основной фон (светло-желтый, как старая бумага)
        screen.fill((245, 245, 220))  # цвет бежевый

        # Линии как в тетради
        for i in range(0, 600, 30):
            pygame.draw.line(screen, (200, 200, 255), (0, i), (800, i), 1)  # голубые линии

        # Вертикальная красная линия (поля)
        pygame.draw.line(screen, (255, 100, 100), (50, 0), (50, 600), 2)

    def draw_background_wood(screen):
        # Основной цвет дерева
        screen.fill((139, 69, 19))  # коричневый

        # Текстура дерева (горизонтальные линии)
        for i in range(0, 600, 5):
            color_variation = (150 + i % 50, 80 + i % 30, 30 + i % 20)
            pygame.draw.line(screen, color_variation, (0, i), (800, i), 2)

        # Добавляем "сучки" (круги разного размера)
        for x in range(100, 700, 150):
            for y in range(100, 500, 150):
                pygame.draw.circle(screen, (101, 67, 33), (x, y), 15)
                pygame.draw.circle(screen, (160, 82, 45), (x + 5, y - 3), 5)

    def draw_background_chalkboard(screen):
        # Основной цвет доски
        screen.fill((0, 50, 0))  # темно-зеленый

        # Текстура мела (случайные белые точки)
        for _ in range(1000):
            x = random.randint(0, 800)
            y = random.randint(0, 600)
            pygame.draw.circle(screen, (200, 255, 200), (x, y), 1)

        # Рамка как у доски
        pygame.draw.rect(screen, (139, 69, 19), (0, 0, 800, 600), 10)

    def draw_background_parchment(screen):
        # Основной цвет пергамента
        screen.fill((222, 184, 135))  # цвет пергамента

        # Эффект старой бумаги
        for x in range(0, 800, 10):
            for y in range(0, 600, 10):
                # Случайные пятна и потертости
                if random.random() > 0.95:
                    color = (200, 160, 120)  # темные пятна
                    pygame.draw.rect(screen, color, (x, y, 10, 10))
                elif random.random() > 0.97:
                    color = (250, 235, 215)  # светлые пятна
                    pygame.draw.rect(screen, color, (x, y, 10, 10))

        # Края как у старого свитка
        for i in range(0, 800, 20):
            pygame.draw.arc(screen, (139, 69, 19), (i - 10, -10, 40, 40), 0, 3.14, 2)

    def draw_background_kids(screen):
        # Яркий фон
        screen.fill((135, 206, 235))  # небесно-голубой

        # Трава внизу
        pygame.draw.rect(screen, (124, 252, 0), (0, 450, 800, 150))

        # Облака
        for cloud in [(100, 100), (300, 70), (500, 120), (700, 90)]:
            pygame.draw.circle(screen, (255, 255, 255), cloud, 30)
            pygame.draw.circle(screen, (255, 255, 255), (cloud[0] + 30, cloud[1] - 10), 25)
            pygame.draw.circle(screen, (255, 255, 255), (cloud[0] - 20, cloud[1] - 5), 25)

        # Солнце
        pygame.draw.circle(screen, (255, 255, 0), (700, 80), 40)

        # Рамка как в детском рисунке
        for i in range(0, 800, 20):
            pygame.draw.rect(screen, (255, 105, 180), (i, 0, 10, 10))
            pygame.draw.rect(screen, (255, 105, 180), (i, 590, 10, 10))
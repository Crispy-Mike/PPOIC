import pygame
import sys
import random
import time
from Database import Database
from EmailSender import create_demo_email_sender
from Button import Button
from InputBox import InputBox
from Hangman import Hangman
from GameScreens import GameScreens
from Letters import Letters
from GameManager import GameManager
from WORDS_BY_LENGTH import WORDS_BY_LENGTH

# Инициализация Pygame
pygame.init()
pygame.mixer.init()  # Для звуков

# Константы
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
LIGHT_BLUE = (173, 216, 230)
GOLD = (255, 215, 0)

# Состояния игры
STATE_SPLASH = -1
STATE_ENTRANCE = 0
STATE_REGISTRATION = 1
STATE_CONFIRMATION = 2
STATE_MAIN_MENU = 3
STATE_OFFLINE_LEVELS = 4
STATE_ONLINE_LEVELS = 5
STATE_SEARCHING = 6
STATE_GAME = 7
STATE_GAME_ONLINE = 8
STATE_HELP = 9
STATE_RECORDS = 10
STATE_GAME_OVER = 11

# Настройки сложности
DIFFICULTY_SETTINGS = {
    "easy": {"name": "Легкий", "max_errors": 7, "time": None},
    "medium": {"name": "Средний", "max_errors": 5, "time": None},
    "hard": {"name": "Сложный", "max_errors": 5, "time": 180}  # 3 минуты
}


class HangmanGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Hangman Game")
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 36)
        self.font_tiny = pygame.font.Font(None, 24)

        # Инициализация компонентов
        self.db = Database()
        self.email_sender = create_demo_email_sender()  # Для демо-режима
        self.game_screens = GameScreens(self.screen)

        # Состояние игры
        self.current_state = STATE_SPLASH
        self.current_difficulty = "easy"
        self.current_mode = "offline"

        # Данные пользователя
        self.current_user = None
        self.temp_user_data = {}

        # Игровые объекты
        self.game_manager = None
        self.hangman = None
        self.letters_display = None
        self.alphabet_buttons = []

        # Элементы интерфейса (инициализируем пустыми списками)
        self.entrance_buttons = []
        self.entrance_inputs = []
        self.registration_buttons = []
        self.registration_inputs = []
        self.confirmation_buttons = []
        self.confirmation_inputs = []

        # Звуки
        self.load_sounds()

        # Анимация
        self.splash_alpha = 255
        self.splash_time = 0

        # Таблица рекордов
        self.records = []

        # Кнопки меню
        self.menu_buttons = {}

        # Таймер для онлайн поиска
        self.search_start_time = 0
        self.search_animation_time = 0

        # Создаем кнопки после инициализации всех атрибутов
        self.create_alphabet_buttons()
        self.create_menu_buttons()
        self.create_entrance_screen()  # Сразу создаем экран входа

    def load_sounds(self):
        """Загрузка звуковых эффектов"""
        try:
            # В реальном проекте здесь должны быть пути к звуковым файлам
            # self.correct_sound = pygame.mixer.Sound("sounds/correct.wav")
            # self.wrong_sound = pygame.mixer.Sound("sounds/wrong.wav")
            # self.win_sound = pygame.mixer.Sound("sounds/win.wav")
            # self.lose_sound = pygame.mixer.Sound("sounds/lose.wav")
            # pygame.mixer.music.load("sounds/background.mp3")
            pass
        except:
            print("Звуковые файлы не найдены")

    def create_alphabet_buttons(self):
        """Создание кнопок алфавита"""
        self.alphabet_buttons = []
        letters = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
        start_x = 100
        start_y = 450
        button_size = 40
        spacing = 10

        for i, letter in enumerate(letters):
            x = start_x + (i % 10) * (button_size + spacing)
            y = start_y + (i // 10) * (button_size + spacing)
            button = Button(x, y, button_size, button_size, letter, self.screen)
            button.font = pygame.font.Font(None, 30)
            button.text_color = BLACK
            button.color = LIGHT_BLUE
            self.alphabet_buttons.append(button)

    def create_menu_buttons(self):
        """Создание кнопок меню"""
        # Кнопки главного меню
        self.menu_buttons = {
            "main": [
                Button(300, 200, 50, 200, "Оффлайн игра", self.screen),
                Button(300, 270, 50, 200, "Онлайн игра", self.screen),
                Button(300, 340, 50, 200, "Таблица рекордов", self.screen),
                Button(300, 410, 50, 200, "Справка", self.screen),
                Button(300, 480, 50, 200, "Выход", self.screen)
            ],
            "offline_levels": [
                Button(200, 200, 50, 150, "Легкий", self.screen),
                Button(400, 200, 50, 150, "Средний", self.screen),
                Button(600, 200, 50, 150, "Сложный", self.screen),
                Button(300, 350, 50, 200, "Назад", self.screen)
            ],
            "online_levels": [
                Button(200, 200, 50, 150, "Легкий", self.screen),
                Button(400, 200, 50, 150, "Средний", self.screen),
                Button(600, 200, 50, 150, "Сложный", self.screen),
                Button(300, 350, 50, 200, "Назад", self.screen)
            ]
        }

        # Настройка цветов кнопок
        for category in self.menu_buttons:
            for button in self.menu_buttons[category]:
                if "Легкий" in button.text:
                    button.color = (144, 238, 144)  # Светло-зеленый
                elif "Средний" in button.text:
                    button.color = (255, 255, 224)  # Светло-желтый
                elif "Сложный" in button.text:
                    button.color = (255, 182, 193)  # Светло-красный

    def create_entrance_screen(self):
        """Создание экрана входа"""
        button_ready = Button(300, 350, 50, 200, "Войти", self.screen)
        button_registration = Button(300, 420, 50, 200, "Регистрация", self.screen)
        button_exit = Button(300, 490, 50, 200, "Выход", self.screen)

        input_box_name = InputBox(250, 200, 300, 40, self.screen, "text", "Введите логин или email")
        input_box_password = InputBox(250, 270, 300, 40, self.screen, "password", "Введите пароль")
        input_box_password.is_password = True

        self.entrance_buttons = [button_ready, button_registration, button_exit]
        self.entrance_inputs = [input_box_name, input_box_password]

    def create_registration_screen(self):
        """Создание экрана регистрации"""
        button_ready = Button(250, 500, 50, 300, "Зарегистрироваться", self.screen)
        button_entrance = Button(300, 560, 50, 200, "Назад к входу", self.screen)

        input_box_login = InputBox(250, 200, 300, 40, self.screen, "text", "Введите логин")
        input_box_email = InputBox(250, 270, 300, 40, self.screen, "email", "Введите email")
        input_box_password = InputBox(250, 340, 300, 40, self.screen, "password", "Введите пароль")
        input_box_double_password = InputBox(250, 410, 300, 40, self.screen, "password", "Повторите пароль")

        input_box_password.is_password = True
        input_box_double_password.is_password = True

        self.registration_buttons = [button_ready, button_entrance]
        self.registration_inputs = [input_box_login, input_box_email, input_box_password, input_box_double_password]

    def create_confirmation_screen(self):
        """Создание экрана подтверждения"""
        button_ready = Button(300, 350, 50, 200, "Подтвердить", self.screen)
        input_box_code = InputBox(250, 250, 300, 40, self.screen, "text", "Введите код из email")

        self.confirmation_buttons = [button_ready]
        self.confirmation_inputs = [input_box_code]

    def run(self):
        """Главный цикл игры"""
        running = True

        # Показываем заставку
        self.show_splash()

        while running:
            # Обработка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.handle_escape()

                self.handle_events(event)

            # Отрисовка в зависимости от состояния
            self.draw()

            pygame.display.flip()
            self.clock.tick(FPS)

        self.db.close()
        pygame.quit()
        sys.exit()

    def show_splash(self):
        """Показ заставки"""
        start_time = time.time()
        while time.time() - start_time < 3:  # 3 секунды
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.current_state = STATE_ENTRANCE
                        return

            # Анимация заставки
            self.screen.fill((0, 0, 20))

            # Звезды
            for _ in range(100):
                x = random.randint(0, WIDTH)
                y = random.randint(0, HEIGHT)
                brightness = random.randint(100, 255)
                pygame.draw.circle(self.screen, (brightness, brightness, brightness), (x, y), 1)

            # Текст
            title = self.font_large.render("HANGMAN", True, GOLD)
            title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
            self.screen.blit(title, title_rect)

            subtitle = self.font_medium.render("Classic Word Game", True, WHITE)
            sub_rect = subtitle.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
            self.screen.blit(subtitle, sub_rect)

            press_text = self.font_small.render("Press SPACE to continue", True, GRAY)
            press_rect = press_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
            self.screen.blit(press_text, press_rect)

            pygame.display.flip()
            self.clock.tick(FPS)

        self.current_state = STATE_ENTRANCE

    def handle_escape(self):
        """Обработка нажатия ESC"""
        if self.current_state == STATE_GAME:
            self.current_state = STATE_MAIN_MENU
        elif self.current_state in [STATE_OFFLINE_LEVELS, STATE_ONLINE_LEVELS, STATE_HELP, STATE_RECORDS]:
            self.current_state = STATE_MAIN_MENU
        elif self.current_state == STATE_ENTRANCE:
            pass  # Ничего не делаем
        else:
            self.current_state = STATE_ENTRANCE

    def handle_events(self, event):
        """Обработка событий в зависимости от состояния"""
        if self.current_state == STATE_SPLASH:
            return

        elif self.current_state == STATE_ENTRANCE:
            self.handle_entrance_events(event)

        elif self.current_state == STATE_REGISTRATION:
            self.handle_registration_events(event)

        elif self.current_state == STATE_CONFIRMATION:
            self.handle_confirmation_events(event)

        elif self.current_state == STATE_MAIN_MENU:
            self.handle_main_menu_events(event)

        elif self.current_state == STATE_OFFLINE_LEVELS:
            self.handle_offline_levels_events(event)

        elif self.current_state == STATE_ONLINE_LEVELS:
            self.handle_online_levels_events(event)

        elif self.current_state == STATE_SEARCHING:
            self.handle_searching_events(event)

        elif self.current_state == STATE_GAME:
            self.handle_game_events(event)

        elif self.current_state == STATE_GAME_ONLINE:
            self.handle_online_game_events(event)

        elif self.current_state == STATE_HELP:
            self.handle_help_events(event)

        elif self.current_state == STATE_RECORDS:
            self.handle_records_events(event)

        elif self.current_state == STATE_GAME_OVER:
            self.handle_game_over_events(event)

    # === ОБРАБОТЧИКИ СОБЫТИЙ ===

    def handle_entrance_events(self, event):
        """Обработка событий на экране входа"""
        # Обработка кнопок
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.entrance_buttons:
                if button.rect.collidepoint(event.pos):
                    if button.text == "Войти":
                        self.handle_login()
                    elif button.text == "Регистрация":
                        self.current_state = STATE_REGISTRATION
                        self.create_registration_screen()
                    elif button.text == "Выход":
                        pygame.quit()
                        sys.exit()

        # Обработка полей ввода
        for input_box in self.entrance_inputs:
            input_box.handle_event(event)

    def handle_registration_events(self, event):
        """Обработка событий на экране регистрации"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.registration_buttons:
                if button.rect.collidepoint(event.pos):
                    if button.text == "Зарегистрироваться":
                        self.handle_registration()
                    elif button.text == "Назад к входу":
                        self.current_state = STATE_ENTRANCE
                        self.create_entrance_screen()

        for input_box in self.registration_inputs:
            input_box.handle_event(event)

    def handle_confirmation_events(self, event):
        """Обработка событий на экране подтверждения"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.confirmation_buttons:
                if button.rect.collidepoint(event.pos):
                    if button.text == "Подтвердить":
                        self.handle_confirmation()

        for input_box in self.confirmation_inputs:
            input_box.handle_event(event)

    def handle_main_menu_events(self, event):
        """Обработка событий главного меню"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.menu_buttons["main"]:
                if button.rect.collidepoint(event.pos):
                    if button.text == "Оффлайн игра":
                        self.current_state = STATE_OFFLINE_LEVELS
                    elif button.text == "Онлайн игра":
                        self.current_state = STATE_ONLINE_LEVELS
                    elif button.text == "Таблица рекордов":
                        self.load_records()
                        self.current_state = STATE_RECORDS
                    elif button.text == "Справка":
                        self.current_state = STATE_HELP
                    elif button.text == "Выход":
                        pygame.quit()
                        sys.exit()

    def handle_offline_levels_events(self, event):
        """Обработка событий выбора уровня оффлайн"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.menu_buttons["offline_levels"]:
                if button.rect.collidepoint(event.pos):
                    if button.text == "Назад":
                        self.current_state = STATE_MAIN_MENU
                    else:
                        # Запуск оффлайн игры с выбранной сложностью
                        difficulty = "easy"
                        if button.text == "Средний":
                            difficulty = "medium"
                        elif button.text == "Сложный":
                            difficulty = "hard"

                        self.start_offline_game(difficulty)

    def handle_online_levels_events(self, event):
        """Обработка событий выбора уровня онлайн"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.menu_buttons["online_levels"]:
                if button.rect.collidepoint(event.pos):
                    if button.text == "Назад":
                        self.current_state = STATE_MAIN_MENU
                    else:
                        # Запуск поиска онлайн игры
                        difficulty = "easy"
                        if button.text == "Средний":
                            difficulty = "medium"
                        elif button.text == "Сложный":
                            difficulty = "hard"

                        self.start_online_search(difficulty)

    def handle_searching_events(self, event):
        """Обработка событий во время поиска противника"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.current_state = STATE_ONLINE_LEVELS

    def handle_game_events(self, event):
        """Обработка событий во время игры"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Проверка нажатия на буквы
            for i, button in enumerate(self.alphabet_buttons):
                if button.rect.collidepoint(event.pos) and not button.active:
                    letter = button.text
                    self.make_guess(letter)
                    break

    def handle_online_game_events(self, event):
        """Обработка событий во время онлайн игры"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Проверка нажатия на буквы (только если наш ход)
            if self.game_manager and self.game_manager.my_turn:
                for i, button in enumerate(self.alphabet_buttons):
                    if button.rect.collidepoint(event.pos) and not button.active:
                        letter = button.text
                        self.make_online_guess(letter)
                        break

    def handle_help_events(self, event):
        """Обработка событий на экране справки"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.current_state = STATE_MAIN_MENU

    def handle_records_events(self, event):
        """Обработка событий на экране рекордов"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.current_state = STATE_MAIN_MENU

    def handle_game_over_events(self, event):
        """Обработка событий на экране окончания игры"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Играть снова
                if self.current_mode == "offline":
                    self.start_offline_game(self.current_difficulty)
                else:
                    self.start_online_search(self.current_difficulty)
            elif event.key == pygame.K_ESCAPE:
                self.current_state = STATE_MAIN_MENU

    # === ОБРАБОТКА ДЕЙСТВИЙ ===

    def handle_login(self):
        """Обработка входа"""
        login = self.entrance_inputs[0].text
        password = self.entrance_inputs[1].text

        if not login or not password:
            self.show_message("Заполните все поля")
            return

        result = self.db.login_user(login, password)

        if result["success"]:
            self.current_user = result
            self.current_state = STATE_MAIN_MENU
            self.show_message(f"Добро пожаловать, {result['login']}!", GREEN)
        else:
            self.show_message(result["error"], RED)

    def handle_registration(self):
        """Обработка регистрации"""
        login = self.registration_inputs[0].text
        email = self.registration_inputs[1].text
        password = self.registration_inputs[2].text
        password2 = self.registration_inputs[3].text

        # Валидация
        if not login or not email or not password:
            self.show_message("Заполните все поля")
            return

        if len(login) < 3:
            self.show_message("Логин должен быть минимум 3 символа")
            return

        if '@' not in email or '.' not in email:
            self.show_message("Некорректный email")
            return

        if password != password2:
            self.show_message("Пароли не совпадают")
            return

        if len(password) < 6:
            self.show_message("Пароль должен быть минимум 6 символов")
            return

        # Регистрация в БД
        result = self.db.register_user(login, email, password)

        if result["success"]:
            # Отправка кода подтверждения
            code = result["code"]
            email_result = self.email_sender.send_verification_code(email, code)

            if email_result["success"]:
                self.temp_user_data = {
                    "email": email,
                    "code": code,
                    "login": login
                }
                self.current_state = STATE_CONFIRMATION
                self.create_confirmation_screen()
                self.show_message(f"Код подтверждения отправлен на {email}", GREEN)
            else:
                self.show_message("Ошибка отправки email")
        else:
            self.show_message(result["error"], RED)

    def handle_confirmation(self):
        """Обработка подтверждения email"""
        code = self.confirmation_inputs[0].text

        if not code:
            self.show_message("Введите код")
            return

        result = self.db.verify_user(self.temp_user_data["email"], code)

        if result["success"]:
            self.show_message("Регистрация успешна! Теперь вы можете войти.", GREEN)
            self.current_state = STATE_ENTRANCE
            self.create_entrance_screen()
        else:
            self.show_message(result["error"], RED)

    def start_offline_game(self, difficulty):
        """Запуск оффлайн игры"""
        self.current_mode = "offline"
        self.current_difficulty = difficulty

        # Создаем менеджер игры
        self.game_manager = GameManager(mode="offline", difficulty=difficulty)

        # Создаем виселицу
        self.hangman = Hangman(100, 100, self.screen)
        self.hangman.errors = 0
        self.hangman.max_errors = self.game_manager.max_errors

        # Создаем отображение слова
        word_x = 300
        word_y = 350
        self.letters_display = Letters(self.screen, self.game_manager.word, word_x, word_y, 48, 50)

        # Сбрасываем кнопки алфавита
        for button in self.alphabet_buttons:
            button.color = LIGHT_BLUE
            button.active = False

        # Запускаем игру
        self.game_manager.start_game()
        self.current_state = STATE_GAME

    def start_online_search(self, difficulty):
        """Поиск противника для онлайн игры"""
        self.current_mode = "online"
        self.current_difficulty = difficulty

        # Имитация поиска
        self.search_start_time = time.time()
        self.current_state = STATE_SEARCHING

    def start_online_game(self):
        """Запуск онлайн игры"""
        # Создаем менеджер игры
        self.game_manager = GameManager(mode="online", difficulty=self.current_difficulty)

        # Устанавливаем слово противника (длина ±1)
        self.game_manager.set_opponent_word(len(self.game_manager.word))

        # Создаем виселицу
        self.hangman = Hangman(100, 100, self.screen)
        self.hangman.errors = 0
        self.hangman.max_errors = self.game_manager.max_errors

        # Создаем отображение слова
        word_x = 300
        word_y = 350
        self.letters_display = Letters(self.screen, self.game_manager.word, word_x, word_y, 48, 50)

        # Сбрасываем кнопки алфавита
        for button in self.alphabet_buttons:
            button.color = LIGHT_BLUE
            button.active = False

        # Запускаем игру
        self.game_manager.start_game()
        self.current_state = STATE_GAME_ONLINE

    def make_guess(self, letter):
        """Обработка попытки угадать букву"""
        if not self.game_manager or self.game_manager.game_over:
            return

        # Отключаем кнопку
        for button in self.alphabet_buttons:
            if button.text == letter:
                button.active = True
                break

        # Проверяем букву
        result = self.game_manager.guess_letter(letter)

        if result["success"]:
            # Правильная буква
            self.letters_display.guessed_letters.append(letter)
            for button in self.alphabet_buttons:
                if button.text == letter:
                    button.color = GREEN
        else:
            # Неправильная буква
            self.hangman.add_error()
            for button in self.alphabet_buttons:
                if button.text == letter:
                    button.color = RED

        # Проверяем окончание игры
        if result.get("game_over", False):
            self.end_game()

    def make_online_guess(self, letter):
        """Обработка попытки в онлайн режиме"""
        if not self.game_manager or not self.game_manager.my_turn:
            return

        # Отключаем кнопку
        for button in self.alphabet_buttons:
            if button.text == letter:
                button.active = True
                break

        result = self.game_manager.guess_letter(letter)

        if result["success"]:
            # Правильная буква
            self.letters_display.guessed_letters.append(letter)
            for button in self.alphabet_buttons:
                if button.text == letter:
                    button.color = GREEN
            # Наш ход продолжается, если угадали
            self.game_manager.my_turn = result.get("continue_turn", True)
        else:
            # Неправильная буква
            self.hangman.add_error()
            for button in self.alphabet_buttons:
                if button.text == letter:
                    button.color = RED
            # Ход переходит к противнику
            self.game_manager.my_turn = False

            # Имитация хода противника
            self.simulate_opponent_turn()

        # Проверяем окончание игры
        if result.get("game_over", False):
            self.end_game()

    def simulate_opponent_turn(self):
        """Имитация хода противника"""
        # В реальной онлайн игре здесь был бы обмен данными по сети
        # Для демо просто имитируем

        # Небольшая задержка для имитации мышления противника
        pygame.time.wait(500)

        # Случайная буква
        letters = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
        letter = random.choice(letters)

        # Противник делает ход
        result = self.game_manager.opponent_guess(letter)

        if result.get("continue_turn", False):
            # Противник продолжает ход
            self.game_manager.my_turn = False
        else:
            # Ход переходит к нам
            self.game_manager.my_turn = True

    def end_game(self):
        """Завершение игры"""
        if self.game_manager.won:
            # Сохраняем результат
            if self.current_user:
                self.db.save_record(
                    self.current_user["user_id"],
                    self.current_user["login"],
                    self.game_manager.score,
                    f"{self.current_mode}_{self.current_difficulty}",
                    len(self.game_manager.word)
                )

            self.show_message(f"Победа! Счет: {self.game_manager.score}", GREEN)
        else:
            self.show_message(f"Поражение! Загаданное слово: {self.game_manager.word}", RED)

        self.current_state = STATE_GAME_OVER

    def load_records(self):
        """Загрузка таблицы рекордов"""
        self.records = self.db.get_top_records(10)

    def show_message(self, text, color=WHITE):
        """Показ временного сообщения"""
        # В реальном проекте здесь можно сделать всплывающее уведомление
        print(f"MESSAGE: {text}")

    # === ОТРИСОВКА ===

    def draw(self):
        """Отрисовка в зависимости от состояния"""
        if self.current_state == STATE_SPLASH:
            return

        elif self.current_state == STATE_ENTRANCE:
            self.draw_entrance()

        elif self.current_state == STATE_REGISTRATION:
            self.draw_registration()

        elif self.current_state == STATE_CONFIRMATION:
            self.draw_confirmation()

        elif self.current_state == STATE_MAIN_MENU:
            self.draw_main_menu()

        elif self.current_state == STATE_OFFLINE_LEVELS:
            self.draw_offline_levels()

        elif self.current_state == STATE_ONLINE_LEVELS:
            self.draw_online_levels()

        elif self.current_state == STATE_SEARCHING:
            self.draw_searching()

        elif self.current_state == STATE_GAME:
            self.draw_game()

        elif self.current_state == STATE_GAME_ONLINE:
            self.draw_online_game()

        elif self.current_state == STATE_HELP:
            self.draw_help()

        elif self.current_state == STATE_RECORDS:
            self.draw_records()

        elif self.current_state == STATE_GAME_OVER:
            self.draw_game_over()

    def draw_entrance(self):
        """Отрисовка экрана входа"""
        self.game_screens.draw_main_menu([])

        # Заголовок
        title = self.font_medium.render("Вход в игру", True, WHITE)
        title_rect = title.get_rect(center=(WIDTH // 2, 100))
        self.screen.blit(title, title_rect)

        # Поля ввода
        for input_box in self.entrance_inputs:
            input_box.draw(self.font_small)

        # Кнопки
        for button in self.entrance_buttons:
            button.draw()

    def draw_registration(self):
        """Отрисовка экрана регистрации"""
        self.game_screens.draw_main_menu([])

        # Заголовок
        title = self.font_medium.render("Регистрация", True, WHITE)
        title_rect = title.get_rect(center=(WIDTH // 2, 100))
        self.screen.blit(title, title_rect)

        # Поля ввода
        for input_box in self.registration_inputs:
            input_box.draw(self.font_small)

        # Кнопки
        for button in self.registration_buttons:
            button.draw()

    def draw_confirmation(self):
        """Отрисовка экрана подтверждения"""
        self.game_screens.draw_main_menu([])

        # Заголовок
        title = self.font_medium.render("Подтверждение email", True, WHITE)
        title_rect = title.get_rect(center=(WIDTH // 2, 100))
        self.screen.blit(title, title_rect)

        # Информация
        if self.temp_user_data:
            info = self.font_small.render(f"Код отправлен на {self.temp_user_data['email']}", True, GRAY)
            info_rect = info.get_rect(center=(WIDTH // 2, 170))
            self.screen.blit(info, info_rect)

        # Поля ввода
        for input_box in self.confirmation_inputs:
            input_box.draw(self.font_small)

        # Кнопки
        for button in self.confirmation_buttons:
            button.draw()

    def draw_main_menu(self):
        """Отрисовка главного меню"""
        self.game_screens.draw_main_menu([])

        # Приветствие пользователя
        if self.current_user:
            welcome = self.font_small.render(f"Привет, {self.current_user['login']}!", True, GOLD)
            welcome_rect = welcome.get_rect(topright=(WIDTH - 20, 20))
            self.screen.blit(welcome, welcome_rect)

        # Кнопки
        for button in self.menu_buttons["main"]:
            button.draw()

    def draw_offline_levels(self):
        """Отрисовка выбора уровня оффлайн"""
        self.game_screens.draw_offline_level_selection([])

        # Заголовок
        title = self.font_medium.render("Выберите сложность", True, BLACK)
        title_rect = title.get_rect(center=(WIDTH // 2, 100))
        self.screen.blit(title, title_rect)

        # Кнопки
        for button in self.menu_buttons["offline_levels"]:
            button.draw()

    def draw_online_levels(self):
        """Отрисовка выбора уровня онлайн"""
        self.game_screens.draw_online_level_selection([])

        # Заголовок
        title = self.font_medium.render("Выберите режим онлайн", True, WHITE)
        title_rect = title.get_rect(center=(WIDTH // 2, 100))
        self.screen.blit(title, title_rect)

        # Кнопки
        for button in self.menu_buttons["online_levels"]:
            button.draw()

    def draw_searching(self):
        """Отрисовка поиска противника"""
        self.game_screens.draw_searching_opponent()

        # Прогресс поиска
        elapsed = time.time() - self.search_start_time
        if elapsed > 5:  # Через 5 секунд "находим" противника
            # Имитация найденного противника
            self.start_online_game()
            return

        # Анимация
        dots = "." * (int(elapsed * 2) % 4)
        searching_text = self.font_medium.render(f"Поиск противника{dots}", True, GREEN)
        text_rect = searching_text.get_rect(center=(WIDTH // 2, HEIGHT - 100))
        self.screen.blit(searching_text, text_rect)

        # Кнопка отмены
        cancel_text = self.font_small.render("Нажмите ESC для отмены", True, GRAY)
        cancel_rect = cancel_text.get_rect(center=(WIDTH // 2, HEIGHT - 50))
        self.screen.blit(cancel_text, cancel_rect)

    def draw_game(self):
        """Отрисовка игры"""
        # Фон
        self.game_screens.draw_offline_game_background()

        # Виселица
        self.hangman.draw_gallows_base()

        # Рисуем части тела в зависимости от ошибок
        if self.hangman.errors >= 1:
            self.hangman.draw_head()
        if self.hangman.errors >= 2:
            self.hangman.draw_body()
        if self.hangman.errors >= 3:
            self.hangman.draw_left_arm()
        if self.hangman.errors >= 4:
            self.hangman.draw_right_arm()
        if self.hangman.errors >= 5:
            self.hangman.draw_left_leg()
        if self.hangman.errors >= 6:
            self.hangman.draw_right_leg()

        # Слово
        self.letters_display.draw()

        # Алфавит
        for button in self.alphabet_buttons:
            button.draw()

        # Информация
        info_y = 20

        # Сложность
        difficulty_text = self.font_small.render(
            f"Сложность: {DIFFICULTY_SETTINGS[self.current_difficulty]['name']}",
            True, BLACK
        )
        self.screen.blit(difficulty_text, (10, info_y))

        # Ошибки
        errors_text = self.font_small.render(
            f"Ошибки: {self.hangman.errors}/{self.game_manager.max_errors}",
            True, RED if self.hangman.errors > self.game_manager.max_errors // 2 else BLACK
        )
        self.screen.blit(errors_text, (10, info_y + 30))

        # Таймер для сложного режима
        if self.game_manager and self.game_manager.time_limit:
            time_left = self.game_manager.get_time_left()
            if time_left is not None:
                color = RED if time_left < 30 else BLACK
                time_text = self.font_small.render(
                    f"Время: {time_left // 60}:{time_left % 60:02d}",
                    True, color
                )
                self.screen.blit(time_text, (10, info_y + 60))

    def draw_online_game(self):
        """Отрисовка онлайн игры"""
        # Фон
        self.game_screens.draw_online_game_background()

        # Виселица (наша)
        self.hangman.draw_gallows_base()

        # Рисуем части тела
        if self.hangman.errors >= 1:
            self.hangman.draw_head()
        if self.hangman.errors >= 2:
            self.hangman.draw_body()
        if self.hangman.errors >= 3:
            self.hangman.draw_left_arm()
        if self.hangman.errors >= 4:
            self.hangman.draw_right_arm()
        if self.hangman.errors >= 5:
            self.hangman.draw_left_leg()
        if self.hangman.errors >= 6:
            self.hangman.draw_right_leg()

        # Наше слово
        self.letters_display.draw()

        # Слово противника (отображается частично)
        if self.game_manager and self.game_manager.opponent_word:
            opp_display = self.game_manager.get_opponent_display()
            opp_text = self.font_medium.render(opp_display, True, BLUE)
            opp_rect = opp_text.get_rect(center=(WIDTH // 2, 400))
            self.screen.blit(opp_text, opp_rect)

            label = self.font_small.render("Слово противника:", True, GRAY)
            label_rect = label.get_rect(center=(WIDTH // 2, 370))
            self.screen.blit(label, label_rect)

        # Алфавит
        for button in self.alphabet_buttons:
            button.draw()

        # Информация
        info_y = 20

        # Сложность
        difficulty_text = self.font_small.render(
            f"Сложность: {DIFFICULTY_SETTINGS[self.current_difficulty]['name']}",
            True, WHITE
        )
        self.screen.blit(difficulty_text, (10, info_y))

        # Ошибки
        errors_text = self.font_small.render(
            f"Ошибки: {self.hangman.errors}/{self.game_manager.max_errors}",
            True, RED if self.hangman.errors > self.game_manager.max_errors // 2 else WHITE
        )
        self.screen.blit(errors_text, (10, info_y + 30))

        # Чей ход
        if self.game_manager:
            turn_text = self.font_small.render(
                "Ваш ход!" if self.game_manager.my_turn else "Ход противника...",
                True, GREEN if self.game_manager.my_turn else YELLOW
            )
            self.screen.blit(turn_text, (WIDTH - 200, info_y))

        # Таймер для сложного режима
        if self.game_manager and self.game_manager.time_limit:
            time_left = self.game_manager.get_time_left()
            if time_left is not None:
                color = RED if time_left < 30 else WHITE
                time_text = self.font_small.render(
                    f"Время: {time_left // 60}:{time_left % 60:02d}",
                    True, color
                )
                self.screen.blit(time_text, (10, info_y + 60))

    def draw_help(self):
        """Отрисовка справки"""
        # Фон
        self.screen.fill((245, 245, 220))

        # Заголовок
        title = self.font_large.render("Правила игры", True, BLACK)
        title_rect = title.get_rect(center=(WIDTH // 2, 50))
        self.screen.blit(title, title_rect)

        # Текст правил
        rules = [
            "Hangman (Виселица) - игра в угадывание слов.",
            "",
            "Правила:",
            "• Загадано случайное слово",
            "• Вы можете называть буквы алфавита",
            "• Если буква есть в слове - она открывается",
            "• Если буквы нет - рисуется часть виселицы",
            "• Игра продолжается пока не откроете всё слово",
            "  или не сделаете 7 ошибок",
            "",
            "Режимы сложности:",
            "• Легкий - 7 ошибок, без ограничения времени",
            "• Средний - 5 ошибок, без ограничения времени",
            "• Сложный - 5 ошибок, 3 минуты на слово",
            "",
            "Онлайн режим:",
            "• Игра с реальным противником",
            "• Слова могут отличаться на 1 букву",
            "• Ход переходит после ошибки",
            "",
            "Нажмите ESC для возврата в меню"
        ]

        y = 120
        for line in rules:
            if line.startswith("•"):
                text = self.font_small.render(line, True, BLACK)
            elif line.startswith("Режимы") or line.startswith("Онлайн"):
                text = self.font_medium.render(line, True, BLUE)
                y += 10
            elif not line:
                y += 10
                continue
            else:
                text = self.font_small.render(line, True, BLACK)

            text_rect = text.get_rect(topleft=(100, y))
            self.screen.blit(text, text_rect)
            y += 30

    def draw_records(self):
        """Отрисовка таблицы рекордов"""
        # Фон
        self.screen.fill((20, 20, 40))

        # Заголовок
        title = self.font_large.render("Таблица рекордов", True, GOLD)
        title_rect = title.get_rect(center=(WIDTH // 2, 50))
        self.screen.blit(title, title_rect)

        # Заголовки колонок
        headers = ["Место", "Игрок", "Счет", "Режим", "Длина слова", "Дата"]
        x_positions = [50, 150, 300, 400, 520, 620]

        for i, header in enumerate(headers):
            text = self.font_small.render(header, True, YELLOW)
            self.screen.blit(text, (x_positions[i], 120))

        # Рекорды
        if self.records:
            y = 160
            for i, record in enumerate(self.records):
                login, score, game_mode, word_length, date = record

                # Цвет для первых трех мест
                if i == 0:
                    color = GOLD
                elif i == 1:
                    color = (192, 192, 192)  # Серебро
                elif i == 2:
                    color = (205, 127, 50)  # Бронза
                else:
                    color = WHITE

                # Место
                place_text = self.font_small.render(f"{i + 1}", True, color)
                self.screen.blit(place_text, (x_positions[0], y))

                # Игрок
                name_text = self.font_small.render(login[:15], True, color)
                self.screen.blit(name_text, (x_positions[1], y))

                # Счет
                score_text = self.font_small.render(str(score), True, color)
                self.screen.blit(score_text, (x_positions[2], y))

                # Режим
                mode_text = self.font_small.render(game_mode, True, color)
                self.screen.blit(mode_text, (x_positions[3], y))

                # Длина слова
                length_text = self.font_small.render(str(word_length), True, color)
                self.screen.blit(length_text, (x_positions[4], y))

                # Дата (кратко)
                date_str = date.split()[0] if date else ""
                date_text = self.font_small.render(date_str, True, color)
                self.screen.blit(date_text, (x_positions[5], y))

                y += 30
        else:
            no_records = self.font_medium.render("Пока нет рекордов", True, GRAY)
            no_rect = no_records.get_rect(center=(WIDTH // 2, 300))
            self.screen.blit(no_records, no_rect)

        # Подсказка
        hint = self.font_small.render("Нажмите ESC для возврата", True, GRAY)
        hint_rect = hint.get_rect(center=(WIDTH // 2, HEIGHT - 50))
        self.screen.blit(hint, hint_rect)

    def draw_game_over(self):
        """Отрисовка экрана окончания игры"""
        # Фон с затемнением
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        # Результат
        if self.game_manager and self.game_manager.won:
            result_text = self.font_large.render("ПОБЕДА!", True, GREEN)
            score_text = self.font_medium.render(f"Счет: {self.game_manager.score}", True, GOLD)
        else:
            result_text = self.font_large.render("ПОРАЖЕНИЕ!", True, RED)
            word = self.game_manager.word if self.game_manager else "???"
            score_text = self.font_medium.render(f"Загаданное слово: {word}", True, WHITE)

        result_rect = result_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
        self.screen.blit(result_text, result_rect)

        score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30))
        self.screen.blit(score_text, score_rect)

        # Инструкции
        again_text = self.font_small.render("Нажмите ПРОБЕЛ чтобы сыграть снова", True, GRAY)
        again_rect = again_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
        self.screen.blit(again_text, again_rect)

        menu_text = self.font_small.render("Нажмите ESC для выхода в меню", True, GRAY)
        menu_rect = menu_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
        self.screen.blit(menu_text, menu_rect)


if __name__ == "__main__":
    game = HangmanGame()
    game.run()
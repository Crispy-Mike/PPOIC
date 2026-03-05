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
DARK_BLUE = (0, 0, 139)
GOLD = (255, 215, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)

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
        self.bot_thinking = False  # флаг, что бот "думает"
        self.bot_message = None  # текущее сообщение от бота
        self.bot_message_time = 0  # время показа сообщения
        # Инициализация компонентов
        self.db = Database()
        self.email_sender = create_demo_email_sender()
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

        # Элементы интерфейса
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

        # Прокрутка для справки
        self.help_scroll = 0
        self.help_max_scroll = 0
        self.dragging_scroll = False

        # Создаем кнопки
        self.create_alphabet_buttons()
        self.create_menu_buttons()
        self.create_entrance_screen()

    def set_alphabet_position(self, y_offset):
        """Устанавливает вертикальное положение всех кнопок алфавита"""
        start_x = 50
        start_y = y_offset
        button_size = 35
        spacing = 5
        letters = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
        for i, button in enumerate(self.alphabet_buttons):
            x = start_x + (i % 11) * (button_size + spacing)
            y = start_y + (i // 11) * (button_size + spacing)
            button.x = x
            button.y = y
            button.rect.x = x
            button.rect.y = y

    def start_bot_turn(self):
        """Запускает таймер для хода бота (думает от 2 до 7 секунд)"""
        if self.bot_thinking:
            return
        self.bot_thinking = True
        self.game_manager.waiting_for_opponent = True
        thinking_time = random.uniform(2, 7) * 1000  # в миллисекундах
        pygame.time.set_timer(pygame.USEREVENT + 2, int(thinking_time), loops=1)

    def do_bot_turn(self):
        """Выполняет ход бота после задержки"""
        self.bot_thinking = False
        self.game_manager.waiting_for_opponent = False

        # Бот выбирает букву
        letter, result = self.game_manager.bot_guess()
        if letter is None:
            # Если нет доступных букв (маловероятно), ход переходит игроку
            self.game_manager.my_turn = True
            return

        # Показываем результат
        if result.get("success", False):
            message = f"угадал букву '{letter}'!"
        else:
            message = f"ошибся с буквой '{letter}'!"
        self.bot_message = message
        self.bot_message_time = time.time()

        # Проверяем окончание игры
        if result.get("game_over", False):
            if result.get("opponent_won", False):
                self.game_manager.won = False
                self.play_sound(self.lose_sound)
            self.end_game()
            return

        # Обновляем статус хода
        if result.get("continue_turn", False):
            # Бот продолжает ход
            self.game_manager.my_turn = False
            self.game_manager.waiting_for_opponent = True
            self.start_bot_turn()  # следующий ход бота
        else:
            # Ход переходит к игроку
            self.game_manager.my_turn = True
            self.game_manager.waiting_for_opponent = False
    def load_sounds(self):
        """Загрузка звуковых эффектов"""
        try:
            # Создаем простые звуки с помощью pygame.mixer.Sound
            # Если файлы не найдены, создаем заглушки
            self.correct_sound = None
            self.wrong_sound = None
            self.win_sound = None
            self.lose_sound = None
            self.click_sound = None

            # Пытаемся загрузить звуки из файлов
            try:
                self.correct_sound = pygame.mixer.Sound("sounds/correct.wav")
                self.wrong_sound = pygame.mixer.Sound("sounds/wrong.wav")
                self.win_sound = pygame.mixer.Sound("sounds/win.wav")
                self.lose_sound = pygame.mixer.Sound("sounds/lose.wav")
                self.click_sound = pygame.mixer.Sound("sounds/click.wav")
                pygame.mixer.music.load("sounds/background.mp3")
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play(-1)  # Бесконечное воспроизведение
            except:
                print("Звуковые файлы не найдены, использую заглушки")
                # Создаем заглушки для звуков
                self.create_dummy_sounds()
        except Exception as e:
            print(f"Ошибка загрузки звуков: {e}")

    def create_dummy_sounds(self):
        """Создание заглушек для звуков"""

        class DummySound:
            def play(self):
                pass

        self.correct_sound = DummySound()
        self.wrong_sound = DummySound()
        self.win_sound = DummySound()
        self.lose_sound = DummySound()
        self.click_sound = DummySound()

    def play_sound(self, sound):
        """Воспроизведение звука"""
        if sound:
            try:
                sound.play()
            except:
                pass

    def create_alphabet_buttons(self):
        """Создание кнопок алфавита"""
        self.alphabet_buttons = []
        letters = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
        start_x = 50  # Сместил левее
        start_y = 450
        button_size = 35  # Немного уменьшил
        spacing = 5  # Уменьшил отступ

        for i, letter in enumerate(letters):
            x = start_x + (i % 11) * (button_size + spacing)  # 11 букв в ряд
            y = start_y + (i // 11) * (button_size + spacing)
            button = Button(x, y, button_size, button_size, letter, self.screen)
            button.font = pygame.font.Font(None, 25)
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
                Button(300, 340, 50, 200, "Рекорды", self.screen),
                Button(300, 410, 50, 200, "Справка", self.screen),
                Button(300, 480, 50, 200, "Выход", self.screen)
            ],
            "offline_levels": [
                Button(150, 250, 50, 150, "Легкий", self.screen),
                Button(325, 250, 50, 150, "Средний", self.screen),
                Button(500, 250, 50, 150, "Сложный", self.screen),
                Button(300, 400, 50, 200, "Назад", self.screen)
            ],
            "online_levels": [
                Button(150, 250, 50, 150, "Легкий", self.screen),
                Button(325, 250, 50, 150, "Средний", self.screen),
                Button(500, 250, 50, 150, "Сложный", self.screen),
                Button(300, 400, 50, 200, "Назад", self.screen)
            ]
        }

        # Настройка цветов кнопок
        for category in self.menu_buttons:
            for button in self.menu_buttons[category]:
                if "Легкий" in button.text:
                    button.color = (144, 238, 144)  # Светло-зеленый
                elif "Средний" in button.text:
                    button.color = DARK_BLUE  # Синий
                    button.text_color = WHITE
                elif "Сложный" in button.text:
                    button.color = (255, 182, 193)  # Светло-красный

    def create_entrance_screen(self):
        """Создание экрана входа"""
        button_ready = Button(300, 350, 50, 200, "Войти", self.screen)
        button_registration = Button(300, 420, 50, 200, "Регистрация", self.screen)
        button_exit = Button(300, 490, 50, 200, "Выход", self.screen)

        input_box_name = InputBox(250, 200, 300, 40, self.screen, "text", "Введите логин")
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
                    elif event.key == pygame.K_UP and self.current_state == STATE_HELP:
                        self.help_scroll = max(0, self.help_scroll - 30)
                    elif event.key == pygame.K_DOWN and self.current_state == STATE_HELP:
                        self.help_scroll = min(self.help_max_scroll, self.help_scroll + 30)
                # Удалён старый блок для USEREVENT + 1
                self.handle_events(event)

            # Отрисовка
            self.draw()

            pygame.display.flip()
            self.clock.tick(FPS)

        self.db.close()
        pygame.quit()
        sys.exit()
    def show_splash(self):
        """Показ заставки"""
        start_time = time.time()
        while time.time() - start_time < 3:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.current_state = STATE_ENTRANCE
                        return

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
        if self.current_state == STATE_GAME or self.current_state == STATE_GAME_ONLINE:
            if self.current_state == STATE_GAME_ONLINE:
                self.set_alphabet_position(450)  # вернуть для оффлайн
            self.current_state = STATE_MAIN_MENU
        elif self.current_state in [STATE_OFFLINE_LEVELS, STATE_ONLINE_LEVELS, STATE_HELP, STATE_RECORDS,
                                    STATE_SEARCHING]:
            self.current_state = STATE_MAIN_MENU
        elif self.current_state == STATE_ENTRANCE:
            pass
        else:
            self.current_state = STATE_ENTRANCE

    def handle_events(self, event):
        """Обработка событий"""
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
            # Обработка события хода бота (USEREVENT + 2)
            if event.type == pygame.USEREVENT + 2:
                self.do_bot_turn()
            else:
                self.handle_online_game_events(event)

        elif self.current_state == STATE_HELP:
            self.handle_help_events(event)

        elif self.current_state == STATE_RECORDS:
            self.handle_records_events(event)

        elif self.current_state == STATE_GAME_OVER:
            self.handle_game_over_events(event)
    def handle_entrance_events(self, event):
        """Обработка событий на экране входа"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.entrance_buttons:
                if button.rect.collidepoint(event.pos):
                    self.play_sound(self.click_sound)
                    if button.text == "Войти":
                        self.handle_login()
                    elif button.text == "Регистрация":
                        self.current_state = STATE_REGISTRATION
                        self.create_registration_screen()
                    elif button.text == "Выход":
                        pygame.quit()
                        sys.exit()

        for input_box in self.entrance_inputs:
            input_box.handle_event(event)

    def handle_registration_events(self, event):
        """Обработка событий на экране регистрации"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.registration_buttons:
                if button.rect.collidepoint(event.pos):
                    self.play_sound(self.click_sound)
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
                    self.play_sound(self.click_sound)
                    if button.text == "Подтвердить":
                        self.handle_confirmation()

        for input_box in self.confirmation_inputs:
            input_box.handle_event(event)

    def handle_main_menu_events(self, event):
        """Обработка событий главного меню"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.menu_buttons["main"]:
                if button.rect.collidepoint(event.pos):
                    self.play_sound(self.click_sound)
                    if button.text == "Оффлайн игра":
                        self.current_state = STATE_OFFLINE_LEVELS
                    elif button.text == "Онлайн игра":
                        self.current_state = STATE_ONLINE_LEVELS
                    elif button.text == "Рекорды":
                        self.load_records()
                        self.current_state = STATE_RECORDS
                    elif button.text == "Справка":
                        self.current_state = STATE_HELP
                        self.help_scroll = 0
                    elif button.text == "Выход":
                        pygame.quit()
                        sys.exit()

    def handle_offline_levels_events(self, event):
        """Обработка событий выбора уровня оффлайн"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.menu_buttons["offline_levels"]:
                if button.rect.collidepoint(event.pos):
                    self.play_sound(self.click_sound)
                    if button.text == "Назад":
                        self.current_state = STATE_MAIN_MENU
                    else:
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
                    self.play_sound(self.click_sound)
                    if button.text == "Назад":
                        self.current_state = STATE_MAIN_MENU
                    else:
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
            for i, button in enumerate(self.alphabet_buttons):
                if button.rect.collidepoint(event.pos) and not button.active:
                    self.play_sound(self.click_sound)
                    letter = button.text
                    self.make_guess(letter)
                    break

    def handle_online_game_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Проверка нажатия на буквы (только если наш ход)
            if (self.game_manager and self.game_manager.my_turn and
                    not self.game_manager.waiting_for_opponent and
                    not self.game_manager.game_over):

                for button in self.alphabet_buttons:
                    if button.rect.collidepoint(event.pos) and not button.active:
                        self.play_sound(self.click_sound)
                        letter = button.text
                        self.make_online_guess(letter)
                        break

        # Если после хода игрока очередь бота и бот ещё не запущен
        if (self.current_state == STATE_GAME_ONLINE and
                self.game_manager and
                not self.game_manager.my_turn and
                not self.game_manager.waiting_for_opponent and
                not self.game_manager.game_over and
                not self.bot_thinking):
            self.start_bot_turn()

    def handle_help_events(self, event):
        """Обработка событий на экране справки с прокруткой"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Колесо вверх
                self.help_scroll = max(0, self.help_scroll - 30)
            elif event.button == 5:  # Колесо вниз
                self.help_scroll = min(self.help_max_scroll, self.help_scroll + 30)

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
                if self.current_mode == "offline":
                    self.start_offline_game(self.current_difficulty)
                else:
                    self.start_online_search(self.current_difficulty)
            elif event.key == pygame.K_ESCAPE:
                self.current_state = STATE_MAIN_MENU

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

        result = self.db.register_user(login, email, password)

        if result["success"]:
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

        self.game_manager = GameManager(mode="offline", difficulty=difficulty)
        self.hangman = Hangman(50, 100, self.screen)  # Сместил левее
        self.hangman.errors = 0
        self.hangman.max_errors = self.game_manager.max_errors

        # Слово размещаем левее
        word_x = 250  # Сместил левее
        word_y = 350
        self.letters_display = Letters(self.screen, self.game_manager.word, word_x, word_y, 48, 45)

        for button in self.alphabet_buttons:
            button.color = LIGHT_BLUE
            button.active = False

        self.game_manager.start_game()
        self.current_state = STATE_GAME

    def start_online_search(self, difficulty):
        """Поиск противника для онлайн игры"""
        self.current_mode = "online"
        self.current_difficulty = difficulty

        self.search_start_time = time.time()
        self.current_state = STATE_SEARCHING

    def start_online_game(self):
        """Запуск онлайн игры"""
        self.bot_thinking = False
        self.bot_message = None
        self.game_manager = GameManager(mode="online", difficulty=self.current_difficulty)
        self.game_manager.set_opponent_word(len(self.game_manager.word))

        self.hangman = Hangman(50, 100, self.screen)
        self.hangman.errors = 0
        self.hangman.max_errors = self.game_manager.max_errors

        # Слово размещаем слева
        word_x = 100
        word_y = 350
        self.letters_display = Letters(self.screen, self.game_manager.word, word_x, word_y, 48, 45)

        for button in self.alphabet_buttons:
            button.color = LIGHT_BLUE
            button.active = False

        # Устанавливаем алфавит ниже, чтобы не перекрывать виселицы
        self.set_alphabet_position(400)

        # Сброс состояния бота
        self.bot_thinking = False
        self.bot_message = None

        self.game_manager.start_game()
        self.current_state = STATE_GAME_ONLINE
    def make_guess(self, letter):
        """Обработка попытки угадать букву"""
        if not self.game_manager or self.game_manager.game_over:
            return

        for button in self.alphabet_buttons:
            if button.text == letter:
                button.active = True
                break

        result = self.game_manager.guess_letter(letter)

        if result["success"]:
            self.play_sound(self.correct_sound)
            self.letters_display.guessed_letters.append(letter)
            for button in self.alphabet_buttons:
                if button.text == letter:
                    button.color = GREEN
        else:
            self.play_sound(self.wrong_sound)
            self.hangman.add_error()
            for button in self.alphabet_buttons:
                if button.text == letter:
                    button.color = RED

        if result.get("game_over", False):
            if self.game_manager.won:
                self.play_sound(self.win_sound)
            else:
                self.play_sound(self.lose_sound)
            self.end_game()

    def make_online_guess(self, letter):
        """Обработка попытки в онлайн режиме"""
        if not self.game_manager or not self.game_manager.my_turn or self.game_manager.waiting_for_opponent:
            print(
                f"НЕЛЬЗЯ ХОДИТЬ: my_turn={self.game_manager.my_turn if self.game_manager else 'None'}, waiting={self.game_manager.waiting_for_opponent if self.game_manager else 'None'}")
            return

        print(f"ИГРОК ХОДИТ: буква {letter}")

        for button in self.alphabet_buttons:
            if button.text == letter:
                button.active = True
                break

        result = self.game_manager.guess_letter(letter)
        print(f"Результат хода игрока: {result}")

        if result["success"]:
            self.play_sound(self.correct_sound)
            for button in self.alphabet_buttons:
                if button.text == letter:
                    button.color = GREEN

            if result.get("game_over", False):
                if self.game_manager.won:
                    self.play_sound(self.win_sound)
                self.end_game()
                return
        else:
            self.play_sound(self.wrong_sound)
            self.hangman.add_error()
            for button in self.alphabet_buttons:
                if button.text == letter:
                    button.color = RED

            if result.get("game_over", False):
                self.play_sound(self.lose_sound)
                self.end_game()
                return

            # Если ошибка - ход переходит к противнику
            print("ОШИБКА ИГРОКА - Ход переходит к противнику")
            self.game_manager.my_turn = False
            self.game_manager.waiting_for_opponent = False  # Сбросим, чтобы триггернулся таймер


    def end_game(self):
        """Завершение игры"""
        if self.game_manager.won:
            if self.current_user:
                self.db.save_record(
                    self.current_user["user_id"],
                    self.current_user["login"],
                    self.game_manager.score,
                    f"{self.current_mode}_{self.current_difficulty}",
                    len(self.game_manager.word)
                )

        self.current_state = STATE_GAME_OVER

    def load_records(self):
        """Загрузка таблицы рекордов"""
        self.records = self.db.get_top_records(10)

    def show_message(self, text, color=WHITE):
        """Показ временного сообщения"""
        print(f"MESSAGE: {text}")

    def draw(self):
        """Отрисовка"""
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
        # Простой фон без надписей
        self.screen.fill((20, 20, 40))

        # Заголовок в верхней части
        title = self.font_large.render("HANGMAN", True, GOLD)
        title_rect = title.get_rect(center=(WIDTH // 2, 80))
        self.screen.blit(title, title_rect)

        subtitle = self.font_small.render("Classic Word Guessing Game", True, WHITE)
        sub_rect = subtitle.get_rect(center=(WIDTH // 2, 130))
        self.screen.blit(subtitle, sub_rect)

        # Поля ввода
        for input_box in self.entrance_inputs:
            input_box.draw(self.font_small)

        # Кнопки
        for button in self.entrance_buttons:
            button.draw()

    def draw_registration(self):
        """Отрисовка экрана регистрации"""
        self.screen.fill((20, 20, 40))

        title = self.font_large.render("HANGMAN", True, GOLD)
        title_rect = title.get_rect(center=(WIDTH // 2, 50))
        self.screen.blit(title, title_rect)

        subtitle = self.font_small.render("Регистрация", True, WHITE)
        sub_rect = subtitle.get_rect(center=(WIDTH // 2, 100))
        self.screen.blit(subtitle, sub_rect)

        for input_box in self.registration_inputs:
            input_box.draw(self.font_small)

        for button in self.registration_buttons:
            button.draw()

    def draw_confirmation(self):
        """Отрисовка экрана подтверждения"""
        self.screen.fill((20, 20, 40))

        title = self.font_large.render("HANGMAN", True, GOLD)
        title_rect = title.get_rect(center=(WIDTH // 2, 50))
        self.screen.blit(title, title_rect)

        subtitle = self.font_small.render("Подтверждение email", True, WHITE)
        sub_rect = subtitle.get_rect(center=(WIDTH // 2, 100))
        self.screen.blit(subtitle, sub_rect)

        if self.temp_user_data:
            info = self.font_small.render(f"Код отправлен на {self.temp_user_data['email']}", True, GRAY)
            info_rect = info.get_rect(center=(WIDTH // 2, 160))
            self.screen.blit(info, info_rect)

        for input_box in self.confirmation_inputs:
            input_box.draw(self.font_small)

        for button in self.confirmation_buttons:
            button.draw()

    def draw_main_menu(self):
        """Отрисовка главного меню"""
        # Простой градиентный фон
        for i in range(HEIGHT):
            color = (20 + i // 10, 20 + i // 10, 40 + i // 5)
            pygame.draw.line(self.screen, color, (0, i), (WIDTH, i))

        # Заголовок
        title = self.font_large.render("HANGMAN", True, GOLD)
        title_rect = title.get_rect(center=(WIDTH // 2, 100))
        self.screen.blit(title, title_rect)

        # Приветствие пользователя
        if self.current_user:
            welcome = self.font_small.render(f"Привет, {self.current_user['login']}!", True, GOLD)
            welcome_rect = welcome.get_rect(center=(WIDTH // 2, 160))
            self.screen.blit(welcome, welcome_rect)

        # Кнопки
        for button in self.menu_buttons["main"]:
            button.draw()

    def draw_offline_levels(self):
        """Отрисовка выбора уровня оффлайн"""
        # Простой фон
        self.screen.fill((245, 245, 220))

        # Заголовок
        title = self.font_medium.render("Выберите сложность", True, BLACK)
        title_rect = title.get_rect(center=(WIDTH // 2, 120))
        self.screen.blit(title, title_rect)

        # Кнопки
        for button in self.menu_buttons["offline_levels"]:
            button.draw()

    def draw_online_levels(self):
        """Отрисовка выбора уровня онлайн"""
        self.screen.fill((0, 0, 20))

        # Заголовок
        title = self.font_medium.render("Выберите сложность", True, WHITE)
        title_rect = title.get_rect(center=(WIDTH // 2, 120))
        self.screen.blit(title, title_rect)

        for button in self.menu_buttons["online_levels"]:
            button.draw()

    def draw_searching(self):
        """Отрисовка поиска противника"""
        self.screen.fill((0, 0, 20))

        # Центрируем все элементы
        center_x = WIDTH // 2
        center_y = HEIGHT // 2 - 50

        # Радар
        for radius in [50, 100, 150]:
            pygame.draw.circle(self.screen, (0, 100, 0), (center_x, center_y), radius, 1)

        # Линии радара
        pygame.draw.line(self.screen, (0, 100, 0), (center_x - 150, center_y), (center_x + 150, center_y), 1)
        pygame.draw.line(self.screen, (0, 100, 0), (center_x, center_y - 150), (center_x, center_y + 150), 1)

        # Вращающаяся линия
        time_passed = time.time() - self.search_start_time
        angle = time_passed * 2
        end_x = center_x + 140 * pygame.math.Vector2(1, 0).rotate(angle * 57.3)[0]
        end_y = center_y + 140 * pygame.math.Vector2(1, 0).rotate(angle * 57.3)[1]
        pygame.draw.line(self.screen, (0, 255, 0), (center_x, center_y), (end_x, end_y), 2)

        # Прогресс поиска
        if time_passed > 5:
            self.start_online_game()
            return

        # Текст поиска
        dots = "." * (int(time_passed * 2) % 4)
        searching_text = self.font_large.render(f"ПОИСК ПРОТИВНИКА{dots}", True, GREEN)
        text_rect = searching_text.get_rect(center=(center_x, center_y + 100))
        self.screen.blit(searching_text, text_rect)

        # Статистика
        stats = [
            f"Players Online: {random.randint(100, 1000)}",
            f"Your Rank: #{random.randint(1, 100)}",
            f"Est. Time: {random.randint(5, 15)}s"
        ]

        y_offset = center_y + 160
        for stat in stats:
            stat_text = self.font_small.render(stat, True, (100, 255, 100))
            stat_rect = stat_text.get_rect(center=(center_x, y_offset))
            self.screen.blit(stat_text, stat_rect)
            y_offset += 30

        # Подсказка внизу экрана
        hint_text = self.font_small.render("ESC - отмена", True, GRAY)
        hint_rect = hint_text.get_rect(center=(center_x, HEIGHT - 30))
        self.screen.blit(hint_text, hint_rect)

    def draw_game(self):
        """Отрисовка игры"""
        # Светлый фон для оффлайн игры
        self.screen.fill((245, 245, 220))

        # Виселица (черная на светлом фоне)
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

        # Слово
        self.letters_display.draw()

        # Алфавит
        for button in self.alphabet_buttons:
            button.draw()

        # Информация
        info_y = 20

        difficulty_text = self.font_small.render(
            f"Сложность: {DIFFICULTY_SETTINGS[self.current_difficulty]['name']}",
            True, BLACK
        )
        self.screen.blit(difficulty_text, (10, info_y))

        errors_text = self.font_small.render(
            f"Ошибки: {self.hangman.errors}/{self.game_manager.max_errors}",
            True, RED if self.hangman.errors > self.game_manager.max_errors // 2 else BLACK
        )
        self.screen.blit(errors_text, (10, info_y + 30))

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
        self.draw_online_game_with_message(None)

    def draw_online_game_with_message(self, extra_message=None):
        """Отрисовка онлайн игры с дополнительным сообщением"""
        # Темный фон
        self.screen.fill((10, 10, 30))

        # Наша виселица (слева)
        self.draw_hangman(30, 80, self.hangman.errors, is_opponent=False)

        # Виселица противника (справа)
        if self.game_manager:
            self.draw_hangman(480, 80, self.game_manager.opponent_errors, is_opponent=True)

        # НАШЕ СЛОВО - слева
        if self.letters_display:
            word = self.game_manager.word
            guessed = self.game_manager.guessed_letters
            start_x = 80
            start_y = 320
            for i, letter in enumerate(word):
                if letter in guessed:
                    text = self.font_medium.render(letter, True, WHITE)
                    text_rect = text.get_rect(center=(start_x + i * 35, start_y))
                    self.screen.blit(text, text_rect)
                else:
                    # Рисуем подчеркивание
                    text = self.font_medium.render("_", True, GRAY)
                    text_rect = text.get_rect(center=(start_x + i * 35, start_y))
                    self.screen.blit(text, text_rect)
                    line_y = start_y + 30
                    line_x = start_x + i * 35 - 12
                    pygame.draw.line(self.screen, GRAY,
                                     (line_x, line_y),
                                     (line_x + 25, line_y), 2)

        # СЛОВО БОТА - справа
        if self.game_manager and self.game_manager.opponent_word:
            opp_word = self.game_manager.opponent_word
            opp_guessed = self.game_manager.opponent_guessed
            start_x = 500
            start_y = 320
            for i, letter in enumerate(opp_word):
                if letter in opp_guessed:
                    text = self.font_medium.render(letter, True, GREEN)
                    text_rect = text.get_rect(center=(start_x + i * 35, start_y))
                    self.screen.blit(text, text_rect)
                else:
                    text = self.font_medium.render("_", True, GRAY)
                    text_rect = text.get_rect(center=(start_x + i * 35, start_y))
                    self.screen.blit(text, text_rect)
                    line_y = start_y + 30
                    line_x = start_x + i * 35 - 12
                    pygame.draw.line(self.screen, GRAY,
                                     (line_x, line_y),
                                     (line_x + 25, line_y), 2)

        # Алфавит (уже с правильными координатами, установленными в start_online_game)
        for button in self.alphabet_buttons:
            button.draw()

        # Информация
        info_y = 10

        # Наша информация
        difficulty_text = self.font_small.render(
            f"Сложность: {DIFFICULTY_SETTINGS[self.current_difficulty]['name']}",
            True, WHITE
        )
        self.screen.blit(difficulty_text, (10, info_y))

        errors_text = self.font_small.render(
            f"Наши ошибки: {self.hangman.errors}/{self.game_manager.max_errors}",
            True, RED if self.hangman.errors > self.game_manager.max_errors // 2 else WHITE
        )
        self.screen.blit(errors_text, (10, info_y + 25))

        # Информация о боте
        if self.game_manager:
            opp_errors_text = self.font_small.render(
                f"Ошибки: {self.game_manager.opponent_errors}/{self.game_manager.max_errors}",
                True, YELLOW
            )
            opp_errors_rect = opp_errors_text.get_rect(topright=(WIDTH - 10, info_y))
            self.screen.blit(opp_errors_text, opp_errors_rect)

            if self.current_difficulty == "medium":
                stats_text = self.font_tiny.render(
                    "Бот: ~1-2 ошибки/3 хода", True, GRAY
                )
                stats_rect = stats_text.get_rect(topright=(WIDTH - 10, info_y + 50))
                self.screen.blit(stats_text, stats_rect)
            elif self.current_difficulty == "hard":
                stats_text = self.font_tiny.render(
                    "Бот: ~1 ошибка/3 хода", True, GRAY
                )
                stats_rect = stats_text.get_rect(topright=(WIDTH - 10, info_y + 50))
                self.screen.blit(stats_text, stats_rect)

        # Чей ход и сообщения
        center_x = WIDTH // 2
        message_y = 280

        # Сначала проверяем, есть ли сообщение от бота (показываем 1.5 сек)
        if self.bot_message and time.time() - self.bot_message_time < 1.5:
            msg_text = self.font_medium.render(self.bot_message, True, YELLOW)
            msg_rect = msg_text.get_rect(center=(center_x, message_y))
            self.screen.blit(msg_text, msg_rect)
        elif self.bot_message:
            self.bot_message = None  # сообщение устарело
        elif extra_message:
            msg_text = self.font_medium.render(extra_message, True, YELLOW)
            msg_rect = msg_text.get_rect(center=(center_x, message_y))
            self.screen.blit(msg_text, msg_rect)
        elif self.game_manager:
            if self.game_manager.waiting_for_opponent:
                turn_text = self.font_medium.render("Противник думает...", True, YELLOW)
            elif self.game_manager.my_turn:
                turn_text = self.font_medium.render("ВАШ ХОД!", True, GREEN)
            else:
                turn_text = self.font_medium.render("Ход противника...", True, YELLOW)
            turn_rect = turn_text.get_rect(center=(center_x, message_y))
            self.screen.blit(turn_text, turn_rect)

        # Таймер
        if self.game_manager and self.game_manager.time_limit:
            time_left = self.game_manager.get_time_left()
            if time_left is not None:
                color = RED if time_left < 30 else WHITE
                time_text = self.font_small.render(
                    f"Время: {time_left // 60}:{time_left % 60:02d}",
                    True, color
                )
                time_rect = time_text.get_rect(center=(center_x, message_y -30))
                self.screen.blit(time_text, time_rect)
    def draw_hangman(self, x, y, errors, is_opponent=False):
        """Отрисовка виселицы с заданными координатами и количеством ошибок
        is_opponent=True - рисует зеркально (справа налево)"""

        if is_opponent:
            # Зеркальная виселица для противника
            # Основание
            pygame.draw.line(self.screen, WHITE,
                             (x + 150, y + 250), (x, y + 250), 3)  # перевернуто
            # Столб
            pygame.draw.line(self.screen, WHITE,
                             (x + 100, y + 250), (x + 100, y + 50), 3)
            # Перекладина
            pygame.draw.line(self.screen, WHITE,
                             (x + 100, y + 50), (x, y + 50), 3)  # перевернуто
            # Веревка
            pygame.draw.line(self.screen, WHITE,
                             (x, y + 50), (x, y + 80), 3)  # перевернуто

            # Рисуем части тела зеркально
            if errors >= 1:  # Голова
                pygame.draw.circle(self.screen, WHITE,
                                   (x, y + 100), 15, 2)  # x без смещения вправо

            if errors >= 2:  # Тело
                pygame.draw.line(self.screen, WHITE,
                                 (x, y + 115), (x, y + 170), 2)

            if errors >= 3:  # Левая рука (зеркально)
                pygame.draw.line(self.screen, WHITE,
                                 (x, y + 130), (x + 30, y + 150), 2)  # +30 вместо -30

            if errors >= 4:  # Правая рука (зеркально)
                pygame.draw.line(self.screen, WHITE,
                                 (x, y + 130), (x - 30, y + 150), 2)  # -30 вместо +30

            if errors >= 5:  # Левая нога (зеркально)
                pygame.draw.line(self.screen, WHITE,
                                 (x, y + 170), (x + 30, y + 210), 2)  # +30 вместо -30

            if errors >= 6:  # Правая нога (зеркально)
                pygame.draw.line(self.screen, WHITE,
                                 (x, y + 170), (x - 30, y + 210), 2)  # -30 вместо +30
        else:
            # Обычная виселица для игрока
            # Основание
            pygame.draw.line(self.screen, WHITE, (x + 50, y + 250),
                             (x + 200, y + 250), 3)
            # Столб
            pygame.draw.line(self.screen, WHITE, (x + 100, y + 250),
                             (x + 100, y + 50), 3)
            # Перекладина
            pygame.draw.line(self.screen, WHITE, (x + 100, y + 50),
                             (x + 200, y + 50), 3)
            # Веревка
            pygame.draw.line(self.screen, WHITE, (x + 200, y + 50),
                             (x + 200, y + 80), 3)

            # Рисуем части тела
            if errors >= 1:  # Голова
                pygame.draw.circle(self.screen, WHITE,
                                   (x + 200, y + 100), 15, 2)

            if errors >= 2:  # Тело
                pygame.draw.line(self.screen, WHITE,
                                 (x + 200, y + 115), (x + 200, y + 170), 2)

            if errors >= 3:  # Левая рука
                pygame.draw.line(self.screen, WHITE,
                                 (x + 200, y + 130), (x + 170, y + 150), 2)

            if errors >= 4:  # Правая рука
                pygame.draw.line(self.screen, WHITE,
                                 (x + 200, y + 130), (x + 230, y + 150), 2)

            if errors >= 5:  # Левая нога
                pygame.draw.line(self.screen, WHITE,
                                 (x + 200, y + 170), (x + 170, y + 210), 2)

            if errors >= 6:  # Правая нога
                pygame.draw.line(self.screen, WHITE,
                                 (x + 200, y + 170), (x + 230, y + 210), 2)

    def draw_help(self):
        """Отрисовка справки с прокруткой"""
        self.screen.fill((245, 245, 220))

        # Заголовок
        title = self.font_large.render("Правила игры", True, BLACK)
        title_rect = title.get_rect(center=(WIDTH // 2, 50))
        self.screen.blit(title, title_rect)

        # Текст правил
        rules = [
            "Hangman (Виселица) - игра в угадывание слов.",
            "",
            "ПРАВИЛА:",
            "• Загадано случайное слово",
            "• Вы можете называть буквы алфавита",
            "• Если буква есть в слове - она открывается",
            "• Если буквы нет - рисуется часть виселицы",
            "• Игра продолжается пока не откроете всё слово",
            "  или не сделаете максимальное количество ошибок",
            "",
            "РЕЖИМЫ СЛОЖНОСТИ:",
            "• Легкий - 7 ошибок, без ограничения времени",
            "• Средний - 5 ошибок, без ограничения времени",
            "• Сложный - 5 ошибок, 3 минуты на слово",
            "",
            "ОНЛАЙН РЕЖИМ:",
            "• Игра с реальным противником",
            "• Слова могут отличаться на 1 букву",
            "• Ход переходит после ошибки",
            "• Кто первый угадает слово - побеждает",
            "",
            "УПРАВЛЕНИЕ:",
            "• Мышь - выбор букв и кнопок",
            "• ESC - выход в меню",
            "• Стрелки вверх/вниз - прокрутка",
            "• Колесико мыши - прокрутка",
            "",
            "СОВЕТЫ:",
            "• Начинайте с гласных букв",
            "• Часто используемые буквы: А, Е, О, И, Н, Т",
            "• Следите за количеством ошибок",
            "• В сложном режиме следите за временем",
            "",
            "УДАЧНОЙ ИГРЫ!",
            "",
            "Нажмите ESC для возврата в меню"
        ]

        # Вычисляем максимальную прокрутку
        total_height = len(rules) * 35 + 100
        self.help_max_scroll = max(0, total_height - (HEIGHT - 100))

        # Создаем поверхность для прокрутки
        help_surface = pygame.Surface((WIDTH - 100, total_height))
        help_surface.fill((245, 245, 220))

        y = 0
        for line in rules:
            if line.startswith("ПРАВИЛА") or line.startswith("РЕЖИМЫ") or line.startswith("ОНЛАЙН") or line.startswith(
                    "УПРАВЛЕНИЕ") or line.startswith("СОВЕТЫ"):
                color = BLUE
                font = self.font_medium
            elif line.startswith("•"):
                color = BLACK
                font = self.font_small
            elif not line:
                y += 20
                continue
            else:
                color = BLACK
                font = self.font_small

            text = font.render(line, True, color)
            text_rect = text.get_rect(topleft=(50, y))
            help_surface.blit(text, text_rect)
            y += 35

        # Отображаем часть поверхности с учетом прокрутки
        self.screen.blit(help_surface, (0, 100 - self.help_scroll))

        # Полоса прокрутки
        if self.help_max_scroll > 0:
            scroll_height = (HEIGHT - 150) * (HEIGHT - 150) / total_height
            scroll_pos = 100 + (self.help_scroll / self.help_max_scroll) * (HEIGHT - 200 - scroll_height)
            pygame.draw.rect(self.screen, GRAY, (WIDTH - 20, 100, 10, HEIGHT - 200))
            pygame.draw.rect(self.screen, DARK_BLUE, (WIDTH - 20, scroll_pos, 10, scroll_height))

        # Подсказка
        hint = self.font_small.render("ESC - назад | Стрелки/колесико - прокрутка", True, GRAY)
        hint_rect = hint.get_rect(center=(WIDTH // 2, HEIGHT - 30))
        self.screen.blit(hint, hint_rect)

    def draw_records(self):
        """Отрисовка таблицы рекордов"""
        # Простой фон без лишних надписей
        self.screen.fill((20, 20, 40))

        # Заголовок
        title = self.font_large.render("Таблица рекордов", True, GOLD)
        title_rect = title.get_rect(center=(WIDTH // 2, 50))
        self.screen.blit(title, title_rect)

        # Заголовки колонок
        headers = ["Место", "Игрок", "Счет", "Режим", "Длина", "Дата"]
        x_positions = [50, 150, 300, 400, 550, 650]

        # Рисуем рамку для таблицы
        pygame.draw.rect(self.screen, (50, 50, 80), (-10, 90, 830, 400), 2)

        for i, header in enumerate(headers):
            text = self.font_small.render(header, True, YELLOW)
            self.screen.blit(text, (x_positions[i], 100))

        # Рекорды
        if self.records:
            y = 140
            for i, record in enumerate(self.records[:8]):  # Показываем только 8 записей
                login, score, game_mode, word_length, date = record

                if i == 0:
                    color = GOLD
                elif i == 1:
                    color = (192, 192, 192)
                elif i == 2:
                    color = (205, 127, 50)
                else:
                    color = WHITE

                # Место
                place_text = self.font_small.render(f"{i + 1}", True, color)
                self.screen.blit(place_text, (x_positions[0], y))

                # Игрок
                name_text = self.font_small.render(login[:12], True, color)
                self.screen.blit(name_text, (x_positions[1], y))

                # Счет
                score_text = self.font_small.render(str(score), True, color)
                self.screen.blit(score_text, (x_positions[2], y))

                # Режим
                mode_display = game_mode.replace("offline_", "офф ").replace("online_", "онл ")[:8]
                mode_text = self.font_small.render(mode_display, True, color)
                self.screen.blit(mode_text, (x_positions[3], y))

                # Длина слова
                length_text = self.font_small.render(str(word_length), True, color)
                self.screen.blit(length_text, (x_positions[4], y))

                # Дата (только число)
                date_str = date.split()[0] if date else ""
                date_text = self.font_small.render(date_str, True, color)
                self.screen.blit(date_text, (x_positions[5], y))

                y += 35
        else:
            no_records = self.font_medium.render("Пока нет рекордов", True, GRAY)
            no_rect = no_records.get_rect(center=(WIDTH // 2, 300))
            self.screen.blit(no_records, no_rect)

        # Подсказка внизу
        hint = self.font_small.render("Нажмите ESC для возврата", True, GRAY)
        hint_rect = hint.get_rect(center=(WIDTH // 2, HEIGHT - 50))
        self.screen.blit(hint, hint_rect)

    def draw_game_over(self):
        """Отрисовка экрана окончания игры"""
        # Затемнение фона
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

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

        again_text = self.font_small.render("Нажмите ПРОБЕЛ чтобы сыграть снова", True, GRAY)
        again_rect = again_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
        self.screen.blit(again_text, again_rect)

        menu_text = self.font_small.render("Нажмите ESC для выхода в меню", True, GRAY)
        menu_rect = menu_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
        self.screen.blit(menu_text, menu_rect)


if __name__ == "__main__":
    game = HangmanGame()
    game.run()

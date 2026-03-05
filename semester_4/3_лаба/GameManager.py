import random
import time
from WORDS_BY_LENGTH import get_word_by_length, get_random_word


class GameManager:
    def __init__(self, mode="offline", difficulty="easy", word_length=None):
        """
        mode: "offline" или "online"
        difficulty: "easy", "medium", "hard"
        word_length: длина слова
        """
        self.mode = mode
        self.difficulty = difficulty
        self.word = ""
        self.guessed_letters = []
        self.wrong_letters = []
        self.errors = 0
        self.max_errors = self.get_max_errors()
        self.time_limit = self.get_time_limit()
        self.start_time = None
        self.score = 0
        self.game_over = False
        self.won = False

        # Для онлайн режима (бот)
        self.opponent_word = None
        self.opponent_guessed = []
        self.opponent_wrong = []
        self.opponent_errors = 0
        self.my_turn = True  # Чей ход
        self.waiting_for_opponent = False  # Ожидание хода бота

        # Счетчики для бота
        self.bot_turn_count = 0
        self.bot_error_count = 0

        # Выбираем слово
        if word_length:
            self.word = get_word_by_length(word_length)
        else:
            self.word = get_random_word()

        self.word = self.word.upper()
        self.original_word = self.word

    def get_max_errors(self):
        """Количество допустимых ошибок в зависимости от сложности"""
        if self.difficulty == "easy":
            return 7
        elif self.difficulty == "medium":
            return 5
        elif self.difficulty == "hard":
            return 5

    def get_time_limit(self):
        """Временное ограничение в секундах"""
        if self.difficulty == "hard":
            return 180  # 3 минуты
        return None

    def start_game(self):
        """Начать игру"""
        self.start_time = time.time()

    def guess_letter(self, letter):
        """Попытка угадать букву (наш ход)"""
        letter = letter.upper()

        if self.game_over:
            return {"success": False, "message": "Игра окончена"}

        if letter in self.guessed_letters or letter in self.wrong_letters:
            return {"success": False, "message": "Буква уже была"}

        if letter in self.word:
            self.guessed_letters.append(letter)
            # Проверяем, угадано ли всё слово
            if all(l in self.guessed_letters for l in self.word):
                self.game_over = True
                self.won = True
                self.calculate_score()
                return {"success": True, "message": "Победа!", "game_over": True}

            # Если угадали - ход продолжается
            return {"success": True, "message": "Есть такая буква!", "continue_turn": True}
        else:
            self.wrong_letters.append(letter)
            self.errors += 1

            # Проверка на поражение
            if self.errors >= self.max_errors:
                self.game_over = True
                self.won = False
                return {"success": False, "message": "Поражение!", "game_over": True}

            # Если ошиблись - ход переходит к боту
            self.my_turn = False
            self.waiting_for_opponent = True

            return {"success": False, "message": "Нет такой буквы", "continue_turn": False}

    def bot_guess(self):
        """Бот делает ход (возвращает букву и результат)"""
        # Все доступные буквы
        all_letters = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"

        # Частые буквы
        frequent = "АЕИНОРСТ"

        # Какие буквы бот ещё не использовал
        used = self.opponent_guessed + self.opponent_wrong
        available = [l for l in all_letters if l not in used]

        if not available:
            # Если все буквы использованы, игра должна была закончиться
            self.my_turn = True
            self.waiting_for_opponent = False
            return None, None

        # Выбор буквы в зависимости от сложности
        letter = None

        if self.difficulty == "easy":
            # Легкий: полностью случайный выбор
            letter = random.choice(available)

        elif self.difficulty == "medium":
            # Средний: 1-2 ошибки в 3 хода
            self.bot_turn_count += 1

            # Каждые 3 хода проверяем, нужно ли сделать ошибку
            if self.bot_turn_count % 3 == 1:
                # Первый ход в цикле - с вероятностью 66% ошибка
                if random.random() < 0.66:
                    # Выбираем букву, которой точно нет в слове
                    wrong_available = [l for l in available if l not in self.opponent_word]
                    if wrong_available:
                        letter = random.choice(wrong_available)

            if not letter:
                # Если не выбрали ошибочную букву, выбираем умно
                # Сначала проверяем частые буквы, которые есть в слове
                smart_choices = [l for l in frequent if l in self.opponent_word and l in available]
                if smart_choices and random.random() < 0.7:
                    letter = random.choice(smart_choices)
                else:
                    # Иначе случайная буква
                    letter = random.choice(available)

        elif self.difficulty == "hard":
            # Сложный: 1 ошибка в 3 хода
            self.bot_turn_count += 1

            # Каждые 3 хода одна ошибка
            if self.bot_turn_count % 3 == 2:  # Второй ход в цикле
                # Выбираем букву, которой точно нет в слове
                wrong_available = [l for l in available if l not in self.opponent_word]
                if wrong_available:
                    letter = random.choice(wrong_available)

            if not letter:
                # Иначе выбираем буквы, которые есть в слове
                correct_available = [l for l in available if l in self.opponent_word]
                if correct_available:
                    # Из них предпочитаем частые
                    freq_correct = [l for l in correct_available if l in frequent]
                    if freq_correct and random.random() < 0.8:
                        letter = random.choice(freq_correct)
                    else:
                        letter = random.choice(correct_available)
                else:
                    # Если нет правильных букв, берем случайную
                    letter = random.choice(available)

        if not letter:
            letter = random.choice(available)

        # Бот делает ход
        if letter in self.opponent_word:
            self.opponent_guessed.append(letter)

            # Проверяем, угадал ли бот всё слово
            if all(l in self.opponent_guessed for l in self.opponent_word):
                return letter, {"success": True, "game_over": True, "opponent_won": True}

            # Если угадал - продолжает ход
            return letter, {"success": True, "continue_turn": True}
        else:
            self.opponent_wrong.append(letter)
            self.opponent_errors += 1
            self.bot_error_count += 1

            # Проверка на поражение бота
            if self.opponent_errors >= self.max_errors:
                return letter, {"success": False, "game_over": True, "opponent_won": False}

            # Если ошибся - ход переходит к игроку
            self.my_turn = True
            self.waiting_for_opponent = False
            return letter, {"success": False, "continue_turn": False}

    def check_time_limit(self):
        """Проверка ограничения по времени"""
        if self.time_limit and self.start_time:
            elapsed = time.time() - self.start_time
            if elapsed > self.time_limit:
                self.game_over = True
                self.won = False
                return True
        return False

    def get_time_left(self):
        """Сколько времени осталось"""
        if self.time_limit and self.start_time:
            elapsed = time.time() - self.start_time
            left = max(0, self.time_limit - elapsed)
            return int(left)
        return None

    def calculate_score(self):
        """Подсчет очков за победу"""
        if self.won:
            base_score = len(self.word) * 100
            difficulty_multiplier = {
                "easy": 1,
                "medium": 2,
                "hard": 3
            }
            multiplier = difficulty_multiplier.get(self.difficulty, 1)
            error_penalty = self.errors * 10
            self.score = max(100, base_score * multiplier - error_penalty)

            if self.difficulty == "hard" and self.time_limit and self.start_time:
                time_left = self.get_time_left()
                if time_left:
                    self.score += time_left * 2

    def get_word_display(self):
        """Получить отображение слова с угаданными буквами"""
        display = []
        for letter in self.word:
            if letter in self.guessed_letters:
                display.append(letter)
            else:
                display.append("_")
        return " ".join(display)

    # Методы для онлайн режима
    def set_opponent_word(self, word_length):
        """Установить слово бота (длина может отличаться на ±1)"""
        variation = random.choice([-1, 0, 1])
        actual_length = max(2, word_length + variation)
        from WORDS_BY_LENGTH import get_word_by_length
        self.opponent_word = get_word_by_length(actual_length)
        if self.opponent_word:
            self.opponent_word = self.opponent_word.upper()

    def get_opponent_display(self):
        """Получить отображение слова бота"""
        if not self.opponent_word:
            return ""
        display = []
        for letter in self.opponent_word:
            if letter in self.opponent_guessed:
                display.append(letter)
            else:
                display.append("_")
        return " ".join(display)
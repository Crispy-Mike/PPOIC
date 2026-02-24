import random
import time
from WORDS_BY_LENGTH import get_word_by_length, get_random_word


class GameManager:
    def __init__(self, mode="offline", difficulty="easy", word_length=None):
        """
        mode: "offline" или "online"
        difficulty: "easy", "medium", "hard"
        word_length: длина слова (для онлайн режима может отличаться у игроков)
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

        # Выбираем слово
        if word_length:
            self.word = get_word_by_length(word_length)
        else:
            self.word = get_random_word()

        self.word = self.word.upper()
        self.original_word = self.word

        # Для онлайн режима
        self.opponent_word = None
        self.opponent_guessed = []
        self.opponent_wrong = []
        self.my_turn = True  # Чей ход

    def get_max_errors(self):
        """Количество допустимых ошибок в зависимости от сложности"""
        if self.mode == "offline":
            if self.difficulty == "easy":
                return 7  # Полный человечек (голова, тело, 2 руки, 2 ноги, веревка)
            elif self.difficulty == "medium":
                return 5  # Без двух конечностей
            elif self.difficulty == "hard":
                return 3  # Только голова и тело
        else:  # online режим
            if self.difficulty == "easy":
                return 7
            elif self.difficulty == "medium":
                return 5
            elif self.difficulty == "hard":
                return 5  # В харде онлайн тоже 5 ошибок, но есть ограничение по времени

    def get_time_limit(self):
        """Временное ограничение в секундах"""
        if self.mode == "online" and self.difficulty == "hard":
            return 180  # 3 минуты
        elif self.mode == "offline" and self.difficulty == "hard":
            return 180  # 3 минуты для оффлайн харда
        return None  # Без ограничения времени

    def start_game(self):
        """Начать игру"""
        self.start_time = time.time()

    def guess_letter(self, letter):
        """Попытка угадать букву"""
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
            return {"success": True, "message": "Есть такая буква!", "continue_turn": True}
        else:
            self.wrong_letters.append(letter)
            self.errors += 1

            if self.errors >= self.max_errors:
                self.game_over = True
                self.won = False
                return {"success": False, "message": "Поражение!", "game_over": True}

            return {"success": False, "message": "Нет такой буквы", "continue_turn": False}

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
            # Бонус за сложность
            difficulty_multiplier = {
                "easy": 1,
                "medium": 2,
                "hard": 3
            }
            multiplier = difficulty_multiplier.get(self.difficulty, 1)

            # Штраф за ошибки
            error_penalty = self.errors * 10

            self.score = max(100, base_score * multiplier - error_penalty)

            # Бонус за время для хард режима
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
        """Установить слово противника (длина может отличаться на ±1)"""
        variation = random.choice([-1, 0, 1])
        actual_length = max(2, word_length + variation)
        self.opponent_word = get_word_by_length(actual_length)
        if self.opponent_word:
            self.opponent_word = self.opponent_word.upper()

    def opponent_guess(self, letter):
        """Противник угадывает букву"""
        letter = letter.upper()

        if letter in self.opponent_word:
            self.opponent_guessed.append(letter)
            if all(l in self.opponent_guessed for l in self.opponent_word):
                return {"success": True, "game_over": True}
            return {"success": True, "continue_turn": True}
        else:
            self.opponent_wrong.append(letter)
            return {"success": False, "continue_turn": False}

    def get_opponent_display(self):
        """Получить отображение слова противника"""
        if not self.opponent_word:
            return ""
        display = []
        for letter in self.opponent_word:
            if letter in self.opponent_guessed:
                display.append(letter)
            else:
                display.append("_")
        return " ".join(display)
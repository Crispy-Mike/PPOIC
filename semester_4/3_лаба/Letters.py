import pygame

class Letters:
    def __init__(self, screen, word, x, y, font_size=48, letter_spacing=40):
        self.start_x = x
        self.y = y
        self.word = word.upper()
        self.font = pygame.font.Font(None, font_size)
        self.letter_spacing = letter_spacing
        self.guessed_letters = []
        self.letter_positions = []
        self.screen = screen
        self.calculate_position()

    def calculate_position(self):
        self.letter_positions = []
        for i in range(len(self.word)):
            x = self.start_x + i * self.letter_spacing
            self.letter_positions.append((x, self.y))

    def check_letter(self, letter):
        letter = letter.upper()
        if letter in self.guessed_letters:
            return False
        elif letter not in self.word:
            return False
        return True

    def add_guessed_letter(self, letter):
        letter = letter.upper()
        if self.check_letter(letter):
            self.guessed_letters.append(letter)

    def is_letter_guessed(self, index):
        return self.word[index] in self.guessed_letters

    def draw(self, color_guessed=(0, 0, 0), color_hidden=(100, 100, 100)):
        for i, (x, y) in enumerate(self.letter_positions):
            letter = self.word[i]

            if self.is_letter_guessed(i):
                text_surface = self.font.render(letter, True, color_guessed)
                self.screen.blit(text_surface, (x, y))
            else:
                letter_surface = self.font.render(letter, True, color_hidden)
                letter_width = letter_surface.get_width()

                line_y = y + letter_surface.get_height() + 5
                pygame.draw.line(
                    self.screen,
                    color_hidden,
                    (x, line_y),
                    (x + letter_width, line_y),
                    3
                )

    def all_letters_guessed(self):
        for letter in self.word:
            if letter not in self.guessed_letters:
                return False
        return True
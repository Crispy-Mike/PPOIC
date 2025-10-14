import random


class Tag_Game:
    def __init__(self, size=4):
        self.board = []
        self.zero_index = []
        self.size = size
        self.board_win = []

    def check_board(self, board):
        size = len(board)
        one_mass = []
        for i in range(size):
            for j in range(size):
                if board[i][j] != 0:
                    one_mass.append(board[i][j])

        inversion = 0
        for x in range(len(one_mass)):
            for y in range(x + 1, len(one_mass)):
                if one_mass[x] > one_mass[y]:
                    inversion += 1

        zero = 0
        for i in range(size):
            for j in range(size):
                if board[i][j] == 0:
                    zero = size - i
                    break

        if size % 2 == 1:
            return inversion % 2 == 0
        else:
            return (inversion + zero) % 2 == 1

    def create_board(self):
        numbers = list(range(1, self.size * self.size)) + [0]

        # Создаем выигрышную доску
        self.board_win = []
        num = 1
        for i in range(self.size):
            row = []
            for j in range(self.size):
                if i == self.size - 1 and j == self.size - 1:
                    row.append(0)
                else:
                    row.append(num)
                    num += 1
            self.board_win.append(row)

        # Создаем игровую доску
        while True:
            random.shuffle(numbers)
            self.board = []
            index = 0
            for i in range(self.size):
                row = []
                for j in range(self.size):
                    row.append(numbers[index])
                    index += 1
                self.board.append(row)

            if self.check_board(self.board):
                break

        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 0:
                    self.zero_index = [i, j]
                    return

    def check_win(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] != self.board_win[i][j]:
                    return False
        return True

    def move(self, direction):
        if direction == "w" and self.zero_index[0] > 0:
            value_above = self.board[self.zero_index[0] - 1][self.zero_index[1]]
            self.board[self.zero_index[0]][self.zero_index[1]] = value_above
            self.board[self.zero_index[0] - 1][self.zero_index[1]] = 0
            self.zero_index[0] -= 1
            return True

        elif direction == "s" and self.zero_index[0] < self.size - 1:
            value_below = self.board[self.zero_index[0] + 1][self.zero_index[1]]
            self.board[self.zero_index[0]][self.zero_index[1]] = value_below
            self.board[self.zero_index[0] + 1][self.zero_index[1]] = 0
            self.zero_index[0] += 1
            return True

        elif direction == "a" and self.zero_index[1] > 0:
            value_left = self.board[self.zero_index[0]][self.zero_index[1] - 1]
            self.board[self.zero_index[0]][self.zero_index[1]] = value_left
            self.board[self.zero_index[0]][self.zero_index[1] - 1] = 0
            self.zero_index[1] -= 1
            return True

        elif direction == "d" and self.zero_index[1] < self.size - 1:
            value_right = self.board[self.zero_index[0]][self.zero_index[1] + 1]
            self.board[self.zero_index[0]][self.zero_index[1]] = value_right
            self.board[self.zero_index[0]][self.zero_index[1] + 1] = 0
            self.zero_index[1] += 1
            return True

        return False

    def get_board(self):
        return self.board

    def get_win_board(self):
        return self.board_win
import unittest
from unittest.mock import patch
import random
from Tag_Game import Tag_Game

class TestTagGame(unittest.TestCase):

    def setUp(self):
        """Настройка перед каждым тестом"""
        self.game = Tag_Game(size=4)

    def test_init(self):
        """Тест инициализации игры"""
        self.assertEqual(self.game.size, 4)
        self.assertEqual(self.game.board, [])
        self.assertEqual(self.game.zero_index, [])
        self.assertEqual(self.game.board_win, [])

    def test_check_board(self):
        """Тест проверки решаемости доски"""
        # Решаемая доска 3x3
        board_3x3_solvable = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 0]
        ]
        self.assertTrue(self.game.check_board(board_3x3_solvable))

        # Нерешаемая доска 3x3
        board_3x3_unsolvable = [
            [1, 2, 3],
            [4, 5, 6],
            [8, 7, 0]
        ]
        self.assertFalse(self.game.check_board(board_3x3_unsolvable))

    def test_create_board(self):
        """Тест создания валидной доски"""
        self.game.create_board()

        # Проверяем размер доски
        self.assertEqual(len(self.game.board), 4)
        self.assertEqual(len(self.game.board[0]), 4)

        # Проверяем, что доска решаемая
        self.assertTrue(self.game.check_board(self.game.board))

        # Проверяем, что нулевой элемент найден
        self.assertEqual(len(self.game.zero_index), 2)
        self.assertEqual(self.game.board[self.game.zero_index[0]][self.game.zero_index[1]], 0)

    def test_create_board_contains_all_numbers(self):
        """Тест, что доска содержит все числа от 0 до 15"""
        self.game.create_board()

        all_numbers = set()
        for row in self.game.board:
            for num in row:
                all_numbers.add(num)

        expected_numbers = set(range(0, 16))
        self.assertEqual(all_numbers, expected_numbers)

    def test_create_board_win_board(self):
        """Тест создания выигрышной доски"""
        self.game.create_board()

        expected_win_board = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 0]
        ]

        self.assertEqual(self.game.board_win, expected_win_board)

    def test_check_win_false_after_creation(self):
        """Тест проверки победы на начальной доске"""
        self.game.create_board()
        # После создания доска не должна быть выигрышной
        self.assertFalse(self.game.check_win())

    def test_check_win_true(self):
        """Тест проверки победы на выигрышной доске"""
        # Устанавливаем выигрышную доску
        self.game.board = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 0]
        ]
        self.game.board_win = self.game.board.copy()
        self.game.zero_index = [3, 3]

        self.assertTrue(self.game.check_win())

    def test_check_win_false(self):
        """Тест проверки победы на невыигрышной доске"""
        self.game.board = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 0, 15]  # 0 и 15 поменяны местами
        ]
        self.game.board_win = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 0]
        ]

        self.assertFalse(self.game.check_win())

    def test_move_w_invalid(self):
        """Тест невалидного хода вверх (ноль на верхней границе)"""
        self.game.board = [
            [1, 2, 0, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 3]
        ]
        self.game.zero_index = [0, 2]

        result = self.game.move("w")

        self.assertFalse(result)
        self.assertEqual(self.game.zero_index, [0, 2])

    def test_move_s_valid(self):
        """Тест валидного хода вниз"""
        self.game.board = [
            [1, 2, 3, 4],
            [5, 6, 0, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 7]
        ]
        self.game.zero_index = [1, 2]

        result = self.game.move("s")

        self.assertTrue(result)
        self.assertEqual(self.game.board[1][2], 11)
        self.assertEqual(self.game.board[2][2], 0)
        self.assertEqual(self.game.zero_index, [2, 2])

    def test_move_s_invalid(self):
        """Тест невалидного хода вниз (ноль на нижней границе)"""
        self.game.board = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 0, 15]
        ]
        self.game.zero_index = [3, 2]

        result = self.game.move("s")

        self.assertFalse(result)
        self.assertEqual(self.game.zero_index, [3, 2])

    def test_move_a_valid(self):
        """Тест валидного хода влево"""
        self.game.board = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 0, 11],
            [13, 14, 15, 12]
        ]
        self.game.zero_index = [2, 2]

        result = self.game.move("a")

        self.assertTrue(result)
        self.assertEqual(self.game.board[2][2], 10)
        self.assertEqual(self.game.board[2][1], 0)
        self.assertEqual(self.game.zero_index, [2, 1])

    def test_move_a_invalid(self):
        """Тест невалидного хода влево (ноль на левой границе)"""
        self.game.board = [
            [1, 2, 3, 4],
            [0, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 5]
        ]
        self.game.zero_index = [1, 0]

        result = self.game.move("a")

        self.assertFalse(result)
        self.assertEqual(self.game.zero_index, [1, 0])

    def test_move_d_valid(self):
        """Тест валидного хода вправо"""
        self.game.board = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 0, 10, 11],
            [13, 14, 15, 12]
        ]
        self.game.zero_index = [2, 1]

        result = self.game.move("d")

        self.assertTrue(result)
        self.assertEqual(self.game.board[2][1], 10)
        self.assertEqual(self.game.board[2][2], 0)
        self.assertEqual(self.game.zero_index, [2, 2])

    def test_move_d_invalid(self):
        """Тест невалидного хода вправо (ноль на правой границе)"""
        self.game.board = [
            [1, 2, 3, 0],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 4]
        ]
        self.game.zero_index = [0, 3]

        result = self.game.move("d")

        self.assertFalse(result)
        self.assertEqual(self.game.zero_index, [0, 3])

    def test_move_invalid_direction(self):
        """Тест хода с невалидным направлением"""
        self.game.board = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 0, 11],
            [13, 14, 15, 12]
        ]
        self.game.zero_index = [2, 2]

        result = self.game.move("x")

        self.assertFalse(result)
        self.assertEqual(self.game.zero_index, [2, 2])

    def test_get_board(self):
        """Тест получения доски"""
        test_board = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 0]
        ]
        self.game.board = test_board

        self.assertEqual(self.game.get_board(), test_board)

    def test_get_win_board(self):
        """Тест получения выигрышной доски"""
        test_win_board = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 0]
        ]
        self.game.board_win = test_win_board

        self.assertEqual(self.game.get_win_board(), test_win_board)

    def test_create_board_different_size(self):
        """Тест создания доски с разным размером"""
        game_3x3 = Tag_Game(size=3)
        game_3x3.create_board()

        self.assertEqual(len(game_3x3.board), 3)
        self.assertEqual(len(game_3x3.board[0]), 3)

        all_numbers = set()
        for row in game_3x3.board:
            for num in row:
                all_numbers.add(num)

        expected_numbers = set(range(0, 9))
        self.assertEqual(all_numbers, expected_numbers)

    def test_check_board_solvability_guarantee(self):
        """Тест гарантии решаемости созданной доски"""
        for _ in range(10):
            game = Tag_Game(size=4)
            game.create_board()
            self.assertTrue(game.check_board(game.board))

    def test_create_board_zero_position(self):
        """Тест отслеживания позиции нуля при создании доски"""
        self.game.create_board()

        zero_found = False
        for i in range(self.game.size):
            for j in range(self.game.size):
                if self.game.board[i][j] == 0:
                    zero_found = True
                    self.assertEqual([i, j], self.game.zero_index)
                    break
            if zero_found:
                break

        self.assertTrue(zero_found)

    @patch('random.shuffle')
    def test_create_board_retry(self, mock_shuffle):
        """Тест механизма повторных попыток создания доски"""

        def side_effect(numbers):
            if not hasattr(side_effect, 'call_count'):
                side_effect.call_count = 0
            side_effect.call_count += 1

            if side_effect.call_count == 1:
                # Первый вызов - нерешаемая доска
                numbers[:] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 14, 0]
            else:
                # Второй вызов - решаемая доска
                numbers[:] = list(range(1, 16)) + [0]

        mock_shuffle.side_effect = side_effect

        self.game.create_board()

        # Проверяем, что shuffle вызывался дважды
        self.assertEqual(mock_shuffle.call_count, 2)
        # Проверяем, что доска решаемая
        self.assertTrue(self.game.check_board(self.game.board))

    def test_move_sequence(self):
        """Тест последовательности ходов"""
        self.game.board = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 0, 15]
        ]
        self.game.board_win = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 0]
        ]
        self.game.zero_index = [3, 2]

        # Ход вправо
        self.assertTrue(self.game.move("d"))
        self.assertEqual(self.game.board[3][2], 15)
        self.assertEqual(self.game.board[3][3], 0)
        self.assertEqual(self.game.zero_index, [3, 3])

        # Проверка победы
        self.assertTrue(self.game.check_win())


if __name__ == '__main__':
    unittest.main(verbosity=2)
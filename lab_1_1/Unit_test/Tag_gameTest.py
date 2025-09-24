import unittest
import sys
import os

# Добавляем корневую папку проекта в путь
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from Tag_Game import Tag_Game


class TestTag_GameLogic(unittest.TestCase):

    def test_size(self):
        """Тест инициализации игры"""
        game = Tag_Game()
        self.assertEqual(game.size, 4)

    def test_board(self):
        """Тест инициализации игры"""
        game = Tag_Game()
        self.assertEqual(game.board, [])


    def test_zero_index(self):
        """Тест инициализации игры"""
        game = Tag_Game()
        self.assertEqual(game.zero_index, [])



    def test_check_win(self):
        """Тест проверки победы"""
        game = Tag_Game()

        # Победа
        game.board = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 0]
        ]
        game.board_win = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 0]
        ]
        self.assertTrue(game.check_win())


    def test_move(self):
        """Тест движения"""
        game = Tag_Game()
        game.board = [
            [1, 2, 3, 4],
            [5, 6, 0, 8],
            [9, 10, 7, 12],
            [13, 14, 15, 11]
        ]
        game.zero_index = [1, 2]

        # Валидное движение
        self.assertTrue(game.move('w'))
        self.assertEqual(game.zero_index, [0, 2])


    def test_get_board(self):
        """Тест получения доски"""
        game = Tag_Game()
        test_board = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 0]
        ]
        game.board = test_board
        self.assertEqual(game.get_board(), test_board)

    def test_get_win_board(self):
        """Тест получения выигрышной доски"""
        game = Tag_Game()
        test_win_board = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 0]
        ]
        game.board_win = test_win_board
        self.assertEqual(game.get_win_board(), test_win_board)


if __name__ == "__main__":
    unittest.main()
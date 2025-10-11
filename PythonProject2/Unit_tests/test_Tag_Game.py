import unittest
import os
import sys

sys.path.append(os.path.dirname(__file__))

from Tag_Game import Tag_Game

class TestTag_GameLogic(unittest.TestCase):

    def setUp(self):
        self.game = Tag_Game()

    def test_size(self):
        self.assertEqual(self.game.size, 4)

    def test_board_initialization(self):
        self.assertIsInstance(self.game.board, list)
        self.assertIsInstance(self.game.board_win, list)

    def test_zero_index_initialization(self):
        self.assertIsInstance(self.game.zero_index, list)

    def test_check_win_positive(self):
        winning_board = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 0]
        ]
        self.game.board = winning_board
        self.game.board_win = winning_board
        self.assertTrue(self.game.check_win())

    def test_check_win_negative(self):
        non_winning_board = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 0, 15]
        ]
        self.game.board = non_winning_board
        self.game.board_win = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 0]
        ]
        self.assertFalse(self.game.check_win())

    def test_move_valid(self):
        self.game.board = [
            [1, 2, 3, 4],
            [5, 6, 0, 8],
            [9, 10, 7, 12],
            [13, 14, 15, 11]
        ]
        self.game.zero_index = [1, 2]
        self.assertTrue(self.game.move('w'))
        self.assertEqual(self.game.zero_index, [0, 2])

    def test_move_invalid(self):
        self.game.board = [
            [0, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 1]
        ]
        self.game.zero_index = [0, 0]
        self.assertFalse(self.game.move('a'))

    def test_get_board(self):
        test_board = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 0]
        ]
        self.game.board = test_board
        self.assertEqual(self.game.get_board(), test_board)

    def test_get_win_board(self):
        test_win_board = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 0]
        ]
        self.game.board_win = test_win_board
        self.assertEqual(self.game.get_win_board(), test_win_board)

    def test_game_initialization_complete(self):
        self.assertIsNotNone(self.game.size)
        self.assertIsNotNone(self.game.board)
        self.assertIsNotNone(self.game.board_win)
        self.assertIsNotNone(self.game.zero_index)

    def test_move_all_directions(self):
        self.game.board = [
            [1, 2, 3, 4],
            [5, 0, 6, 7],
            [8, 9, 10, 11],
            [12, 13, 14, 15]
        ]
        self.game.zero_index = [1, 1]

        self.assertTrue(self.game.move('w'))
        self.assertEqual(self.game.zero_index, [0, 1])

        self.assertTrue(self.game.move('s'))
        self.assertEqual(self.game.zero_index, [1, 1])

        self.assertTrue(self.game.move('a'))
        self.assertEqual(self.game.zero_index, [1, 0])

        self.assertTrue(self.game.move('d'))
        self.assertEqual(self.game.zero_index, [1, 1])

    def test_invalid_direction(self):
        self.assertFalse(self.game.move('x'))

if __name__ == '__main__':
    unittest.main()
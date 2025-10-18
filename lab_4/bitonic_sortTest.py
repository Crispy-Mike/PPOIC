import unittest
from bitonic_sort import bitonic_sort

class TestSortingNetwork(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(bitonic_sort([3, 7, 2, 5]), [2, 3, 5, 7])
    def test_reverse(self):
        self.assertEqual(bitonic_sort([9, 8, 7, 6]), [6, 7, 8, 9])

import unittest
from quicksort import quicksort

class TestQuicksort(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(quicksort([3, 1, 4, 1, 5]), [1, 1, 3, 4, 5])
    def test_empty(self):
        self.assertEqual(quicksort([]), [])
    def test_sorted(self):
        self.assertEqual(quicksort([1, 2, 3]), [1, 2, 3])

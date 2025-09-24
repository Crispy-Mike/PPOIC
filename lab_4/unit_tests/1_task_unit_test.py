import unittest
from task_1 import cocktail_sort, strand_sort, Student


class TestSortingAlgorithms(unittest.TestCase):

    def test_cocktail_sort_empty(self):
        arr = []
        cocktail_sort(arr)
        self.assertEqual(arr, [])

    def test_cocktail_sort_single(self):
        arr = [42]
        cocktail_sort(arr)
        self.assertEqual(arr, [42])

    def test_cocktail_sort_sorted(self):
        arr = [1, 2, 3, 4, 5]
        cocktail_sort(arr)
        self.assertEqual(arr, [1, 2, 3, 4, 5])

    def test_cocktail_sort_reverse(self):
        arr = [5, 4, 3, 2, 1]
        cocktail_sort(arr)
        self.assertEqual(arr, [1, 2, 3, 4, 5])

    def test_cocktail_sort_random(self):
        arr = [64, 34, 25, 12, 22, 11, 90, 5]
        cocktail_sort(arr)
        self.assertEqual(arr, [5, 11, 12, 22, 25, 34, 64, 90])

    def test_strand_sort_empty(self):
        result = strand_sort([])
        self.assertEqual(result, [])

    def test_strand_sort_single(self):
        result = strand_sort([42])
        self.assertEqual(result, [42])

    def test_strand_sort_sorted(self):
        result = strand_sort([1, 2, 3, 4, 5])
        self.assertEqual(result, [1, 2, 3, 4, 5])

    def test_strand_sort_reverse(self):
        result = strand_sort([5, 4, 3, 2, 1])
        self.assertEqual(result, [1, 2, 3, 4, 5])

    def test_strand_sort_random(self):
        result = strand_sort([64, 34, 25, 12, 22, 11, 90, 5])
        self.assertEqual(result, [5, 11, 12, 22, 25, 34, 64, 90])

    def test_cocktail_sort_students(self):
        students = [Student("Иван", 72), Student("Анна", 85), Student("Петр", 68)]
        cocktail_sort(students)
        self.assertEqual(students[0].score, 68)
        self.assertEqual(students[1].score, 72)
        self.assertEqual(students[2].score, 85)



if __name__ == '__main__':
    unittest.main()
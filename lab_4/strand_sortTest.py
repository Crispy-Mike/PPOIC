import unittest
from strand_sort import strand_sort
from Student import Student

class TestStrandSort(unittest.TestCase):

    def test_strand_sort_empty(self):
        """Тест сортировки пустого массива"""
        arr = []
        result = strand_sort(arr)
        self.assertEqual(result, [])

    def test_strand_sort_single(self):
        """Тест сортировки массива с одним элементом"""
        arr = [42]
        result = strand_sort(arr)
        self.assertEqual(result, [42])

    def test_strand_sort_numbers(self):
        """Тест сортировки чисел"""
        arr = [64, 34, 25, 12, 22, 11, 90]
        result = strand_sort(arr)
        self.assertEqual(result, [11, 12, 22, 25, 34, 64, 90])

    def test_strand_sort_already_sorted(self):
        """Тест сортировки уже отсортированного массива"""
        arr = [1, 2, 3, 4, 5]
        result = strand_sort(arr)
        self.assertEqual(result, [1, 2, 3, 4, 5])

    def test_strand_sort_reverse(self):
        """Тест сортировки массива в обратном порядке"""
        arr = [5, 4, 3, 2, 1]
        result = strand_sort(arr)
        self.assertEqual(result, [1, 2, 3, 4, 5])

    def test_strand_sort_duplicates(self):
        """Тест сортировки массива с дубликатами"""
        arr = [3, 1, 4, 1, 5, 9, 2, 6, 5]
        result = strand_sort(arr)
        self.assertEqual(result, [1, 1, 2, 3, 4, 5, 5, 6, 9])

    def test_strand_sort_students(self):
        """Тест сортировки студентов"""
        students = [
            Student("Анна", 85),
            Student("Иван", 72),
            Student("Мария", 95),
            Student("Петр", 68)
        ]
        result = strand_sort(students)
        self.assertEqual([s.score for s in result], [68, 72, 85, 95])
        self.assertEqual(result[0].name, "Петр")
        self.assertEqual(result[-1].name, "Мария")

    def test_strand_sort_strings(self):
        """Тест сортировки строк"""
        arr = ["banana", "apple", "cherry", "date"]
        result = strand_sort(arr)
        self.assertEqual(result, ["apple", "banana", "cherry", "date"])

    def test_strand_sort_identical(self):
        """Тест сортировки массива с одинаковыми элементами"""
        arr = [7, 7, 7, 7]
        result = strand_sort(arr)
        self.assertEqual(result, [7, 7, 7, 7])

    def test_strand_sort_preserves_original(self):
        """Тест что оригинальный массив не изменяется"""
        original = [3, 1, 4, 2]
        result = strand_sort(original)
        self.assertEqual(original, [3, 1, 4, 2])  # оригинал не изменился
        self.assertEqual(result, [1, 2, 3, 4])    # результат отсортирован

if __name__ == '__main__':
    unittest.main(verbosity=2)
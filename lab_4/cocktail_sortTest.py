import unittest
from cocktail_sort import cocktail_sort
from Student import Student

class TestCocktailSort(unittest.TestCase):

    def test_cocktail_sort_empty(self):
        """Тест сортировки пустого массива"""
        arr = []
        cocktail_sort(arr)
        self.assertEqual(arr, [])

    def test_cocktail_sort_single(self):
        """Тест сортировки массива с одним элементом"""
        arr = [42]
        cocktail_sort(arr)
        self.assertEqual(arr, [42])

    def test_cocktail_sort_numbers(self):
        """Тест сортировки чисел"""
        arr = [64, 34, 25, 12, 22, 11, 90]
        cocktail_sort(arr)
        self.assertEqual(arr, [11, 12, 22, 25, 34, 64, 90])

    def test_cocktail_sort_already_sorted(self):
        """Тест сортировки уже отсортированного массива"""
        arr = [1, 2, 3, 4, 5]
        cocktail_sort(arr)
        self.assertEqual(arr, [1, 2, 3, 4, 5])

    def test_cocktail_sort_reverse(self):
        """Тест сортировки массива в обратном порядке"""
        arr = [5, 4, 3, 2, 1]
        cocktail_sort(arr)
        self.assertEqual(arr, [1, 2, 3, 4, 5])

    def test_cocktail_sort_duplicates(self):
        """Тест сортировки массива с дубликатами"""
        arr = [3, 1, 4, 1, 5, 9, 2, 6, 5]
        cocktail_sort(arr)
        self.assertEqual(arr, [1, 1, 2, 3, 4, 5, 5, 6, 9])

    def test_cocktail_sort_students(self):
        """Тест сортировки студентов"""
        students = [
            Student("Анна", 85),
            Student("Иван", 72),
            Student("Мария", 95),
            Student("Петр", 68)
        ]
        cocktail_sort(students)
        self.assertEqual([s.score for s in students], [68, 72, 85, 95])
        self.assertEqual(students[0].name, "Петр")
        self.assertEqual(students[-1].name, "Мария")

    def test_cocktail_sort_strings(self):
        """Тест сортировки строк"""
        arr = ["banana", "apple", "cherry", "date"]
        cocktail_sort(arr)
        self.assertEqual(arr, ["apple", "banana", "cherry", "date"])

    def test_cocktail_sort_identical(self):
        """Тест сортировки массива с одинаковыми элементами"""
        arr = [7, 7, 7, 7]
        cocktail_sort(arr)
        self.assertEqual(arr, [7, 7, 7, 7])

if __name__ == '__main__':
    unittest.main(verbosity=2)
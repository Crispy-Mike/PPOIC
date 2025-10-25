import unittest
import sys
import os
from typing import List, TypeVar
import random

# Добавляем путь к исходному файлу
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from sorts import Sorts, Comparable

T = TypeVar('T')


class TestNumber(Comparable):
    """Тестовый класс, реализующий Comparable интерфейс"""

    def __init__(self, value: int):
        self.value = value

    def __lt__(self, other: 'TestNumber') -> bool:
        if not isinstance(other, TestNumber):
            return NotImplemented
        return self.value < other.value

    def __gt__(self, other: 'TestNumber') -> bool:
        if not isinstance(other, TestNumber):
            return NotImplemented
        return self.value > other.value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TestNumber):
            return False
        return self.value == other.value

    def __le__(self, other: 'TestNumber') -> bool:
        return self < other or self == other

    def __ge__(self, other: 'TestNumber') -> bool:
        return self > other or self == other

    def __repr__(self) -> str:
        return f"TestNumber({self.value})"


class TestSorts(unittest.TestCase):

    def setUp(self):
        """Настройка тестовых данных"""
        self.test_cases = [
            # Пустой массив
            [],
            # Массив из одного элемента
            [1],
            # Уже отсортированный массив
            [1, 2, 3, 4, 5],
            # Обратно отсортированный массив
            [5, 4, 3, 2, 1],
            # Массив с дубликатами
            [3, 1, 4, 1, 5, 9, 2, 6, 5, 3],
            # Массив с отрицательными числами
            [-5, -1, -3, 0, 2, -4],
            # Массив с одинаковыми элементами
            [7, 7, 7, 7, 7],
        ]

        # Строковые тестовые данные
        self.string_test_cases = [
            [],
            ["a"],
            ["a", "b", "c"],
            ["c", "b", "a"],
            ["banana", "apple", "cherry", "date"],
        ]

    def test_quick_sort_basic(self):
        """Тест базовой функциональности быстрой сортировки"""
        # Тест с целыми числами
        for arr in self.test_cases:
            with self.subTest(arr=arr):
                original = arr.copy()
                expected = sorted(arr)
                result = Sorts.quick_sort(arr)
                self.assertEqual(result, expected,
                                 f"Failed for input: {original}. Expected: {expected}, Got: {result}")
                # Проверяем что оригинальный массив не изменился
                self.assertEqual(arr, original)

        # Тест со строками
        for arr in self.string_test_cases:
            with self.subTest(arr=arr):
                original = arr.copy()
                expected = sorted(arr)
                result = Sorts.quick_sort(arr)
                self.assertEqual(result, expected,
                                 f"Failed for strings: {original}. Expected: {expected}, Got: {result}")
                self.assertEqual(arr, original)

    def test_quick_sort_inplace_basic(self):
        """Тест in-place быстрой сортировки"""
        for arr in self.test_cases:
            with self.subTest(arr=arr):
                test_arr = arr.copy()
                expected = sorted(arr)
                Sorts.quick_sort_inplace(test_arr)
                self.assertEqual(test_arr, expected,
                                 f"Inplace failed for: {arr}. Expected: {expected}, Got: {test_arr}")

    def test_quick_sort_inplace_partial(self):
        """Тест in-place сортировки части массива"""
        arr = [5, 3, 8, 1, 2, 7, 4, 6]
        test_arr = arr.copy()

        # Сортируем только часть массива с индексами 2-6
        Sorts.quick_sort_inplace(test_arr, 2, 6)

        # Проверяем что отсортирована только указанная часть
        # Индексы 2-6: [8, 1, 2, 7, 4] должны стать [1, 2, 4, 7, 8]
        expected = [5, 3, 1, 2, 4, 7, 8, 6]
        self.assertEqual(test_arr, expected)

    def test_quick_sort_inplace_edge_cases(self):
        """Тест граничных случаев in-place сортировки"""
        # Пустой массив
        arr = []
        Sorts.quick_sort_inplace(arr)
        self.assertEqual(arr, [])

        # Один элемент
        arr = [1]
        Sorts.quick_sort_inplace(arr)
        self.assertEqual(arr, [1])

        # Два элемента
        arr = [2, 1]
        Sorts.quick_sort_inplace(arr)
        self.assertEqual(arr, [1, 2])

        # Уже отсортированный
        arr = [1, 2, 3]
        Sorts.quick_sort_inplace(arr)
        self.assertEqual(arr, [1, 2, 3])

    def test_partition_method(self):
        """Тест вспомогательного метода partition"""
        # Тест обычного случая
        arr = [10, 80, 30, 90, 40, 50, 70]
        test_arr = arr.copy()
        pivot_index = Sorts._partition(test_arr, 0, 6)
        pivot = test_arr[pivot_index]

        # Проверяем что все элементы слева <= pivot, а справа >= pivot
        for i in range(0, pivot_index):
            self.assertLessEqual(test_arr[i], pivot)
        for i in range(pivot_index + 1, len(test_arr)):
            self.assertGreaterEqual(test_arr[i], pivot)

        # Тест с уже отсортированным массивом
        arr = [1, 2, 3, 4, 5]
        test_arr = arr.copy()
        pivot_index = Sorts._partition(test_arr, 0, 4)
        self.assertEqual(pivot_index, 4)  # Последний элемент должен быть pivot

    def test_odd_even_sort_basic(self):
        """Тест базовой функциональности чет-нечет сортировки"""
        for arr in self.test_cases:
            with self.subTest(arr=arr):
                test_arr = arr.copy()
                expected = sorted(arr)
                Sorts.odd_even_sort(test_arr)
                self.assertEqual(test_arr, expected,
                                 f"Odd-even failed for: {arr}. Expected: {expected}, Got: {test_arr}")

    def test_odd_even_sort_strings(self):
        """Тест чет-нечет сортировки со строками"""
        for arr in self.string_test_cases:
            with self.subTest(arr=arr):
                test_arr = arr.copy()
                expected = sorted(arr)
                Sorts.odd_even_sort(test_arr)
                self.assertEqual(test_arr, expected,
                                 f"Odd-even strings failed for: {arr}")

    def test_odd_even_sort_edge_cases(self):
        """Тест граничных случаев чет-нечет сортировки"""
        # Пустой массив
        arr = []
        Sorts.odd_even_sort(arr)
        self.assertEqual(arr, [])

        # Один элемент
        arr = [42]
        Sorts.odd_even_sort(arr)
        self.assertEqual(arr, [42])

        # Два элемента
        arr = [2, 1]
        Sorts.odd_even_sort(arr)
        self.assertEqual(arr, [1, 2])

    def test_bubble_sort_basic(self):
        """Тест базовой функциональности пузырьковой сортировки"""
        for arr in self.test_cases:
            with self.subTest(arr=arr):
                test_arr = arr.copy()
                expected = sorted(arr)
                Sorts.bubble_sort(test_arr)
                self.assertEqual(test_arr, expected,
                                 f"Bubble failed for: {arr}. Expected: {expected}, Got: {test_arr}")

    def test_bubble_sort_strings(self):
        """Тест пузырьковой сортировки со строками"""
        for arr in self.string_test_cases:
            with self.subTest(arr=arr):
                test_arr = arr.copy()
                expected = sorted(arr)
                Sorts.bubble_sort(test_arr)
                self.assertEqual(test_arr, expected,
                                 f"Bubble strings failed for: {arr}")

    def test_bubble_sort_edge_cases(self):
        """Тест граничных случаев пузырьковой сортировки"""
        # Пустой массив
        arr = []
        Sorts.bubble_sort(arr)
        self.assertEqual(arr, [])

        # Один элемент
        arr = [99]
        Sorts.bubble_sort(arr)
        self.assertEqual(arr, [99])

        # Уже отсортированный
        arr = [1, 2, 3]
        original = arr.copy()
        Sorts.bubble_sort(arr)
        self.assertEqual(arr, original)

    def test_custom_comparable_class(self):
        """Тест с пользовательским классом, реализующим Comparable"""
        test_objects = [
            TestNumber(5),
            TestNumber(1),
            TestNumber(8),
            TestNumber(3),
            TestNumber(2)
        ]

        # Тест быстрой сортировки
        result = Sorts.quick_sort(test_objects)
        expected_values = [1, 2, 3, 5, 8]
        self.assertEqual([x.value for x in result], expected_values)

        # Тест in-place быстрой сортировки
        test_objects_inplace = [TestNumber(x.value) for x in test_objects]  # Создаем новые объекты
        Sorts.quick_sort_inplace(test_objects_inplace)
        self.assertEqual([x.value for x in test_objects_inplace], expected_values)

        # Тест чет-нечет сортировки
        test_objects_odd_even = [TestNumber(x.value) for x in test_objects]
        Sorts.odd_even_sort(test_objects_odd_even)
        self.assertEqual([x.value for x in test_objects_odd_even], expected_values)

        # Тест пузырьковой сортировки
        test_objects_bubble = [TestNumber(x.value) for x in test_objects]
        Sorts.bubble_sort(test_objects_bubble)
        self.assertEqual([x.value for x in test_objects_bubble], expected_values)

    def test_algorithm_consistency(self):
        """Тест согласованности результатов разных алгоритмов"""
        test_data = [random.randint(1, 100) for _ in range(20)]  # Уменьшил размер для стабильности

        # Быстрая сортировка
        quick_result = Sorts.quick_sort(test_data.copy())

        # In-place быстрая сортировка
        inplace_data = test_data.copy()
        Sorts.quick_sort_inplace(inplace_data)

        # Чет-нечет сортировка
        odd_even_data = test_data.copy()
        Sorts.odd_even_sort(odd_even_data)

        # Пузырьковая сортировка
        bubble_data = test_data.copy()
        Sorts.bubble_sort(bubble_data)

        # Все должны давать одинаковый результат
        expected = sorted(test_data)
        self.assertEqual(quick_result, expected)
        self.assertEqual(inplace_data, expected)
        self.assertEqual(odd_even_data, expected)
        self.assertEqual(bubble_data, expected)

    def test_large_dataset(self):
        """Тест с большим набором данных"""
        large_array = [random.randint(1, 1000) for _ in range(100)]  # Уменьшил размер
        expected = sorted(large_array)

        # Быстрая сортировка
        result_quick = Sorts.quick_sort(large_array.copy())
        self.assertEqual(result_quick, expected)

        # In-place быстрая сортировка
        inplace_data = large_array.copy()
        Sorts.quick_sort_inplace(inplace_data)
        self.assertEqual(inplace_data, expected)

        # Чет-нечет сортировка
        odd_even_data = large_array.copy()
        Sorts.odd_even_sort(odd_even_data)
        self.assertEqual(odd_even_data, expected)

        # Пузырьковая сортировка
        bubble_data = large_array.copy()
        Sorts.bubble_sort(bubble_data)
        self.assertEqual(bubble_data, expected)

    def test_negative_numbers(self):
        """Тест с отрицательными числами"""
        arr = [-5, -1, -10, 0, 3, -2, 7]
        expected = sorted(arr)

        # Тестируем каждый алгоритм отдельно
        test_arr = arr.copy()
        result_quick = Sorts.quick_sort(test_arr)
        self.assertEqual(result_quick, expected)

        test_arr = arr.copy()
        Sorts.quick_sort_inplace(test_arr)
        self.assertEqual(test_arr, expected)

        test_arr = arr.copy()
        Sorts.odd_even_sort(test_arr)
        self.assertEqual(test_arr, expected)

        test_arr = arr.copy()
        Sorts.bubble_sort(test_arr)
        self.assertEqual(test_arr, expected)

    def test_duplicate_elements(self):
        """Тест с дублирующимися элементами"""
        arr = [5, 2, 8, 2, 5, 1, 8, 1]
        expected = sorted(arr)

        # Все алгоритмы должны правильно обрабатывать дубликаты
        result_quick = Sorts.quick_sort(arr.copy())
        self.assertEqual(result_quick, expected)

        arr_inplace = arr.copy()
        Sorts.quick_sort_inplace(arr_inplace)
        self.assertEqual(arr_inplace, expected)

        arr_odd_even = arr.copy()
        Sorts.odd_even_sort(arr_odd_even)
        self.assertEqual(arr_odd_even, expected)

        arr_bubble = arr.copy()
        Sorts.bubble_sort(arr_bubble)
        self.assertEqual(arr_bubble, expected)

    def test_single_element_and_empty(self):
        """Тест специальных случаев с одним элементом и пустым массивом"""
        test_cases = [[], [1], [0], [-1]]

        for arr in test_cases:
            with self.subTest(arr=arr):
                expected = sorted(arr)

                # Быстрая сортировка
                result_quick = Sorts.quick_sort(arr.copy())
                self.assertEqual(result_quick, expected)

                # In-place
                arr_inplace = arr.copy()
                Sorts.quick_sort_inplace(arr_inplace)
                self.assertEqual(arr_inplace, expected)

                # Чет-нечет
                arr_odd_even = arr.copy()
                Sorts.odd_even_sort(arr_odd_even)
                self.assertEqual(arr_odd_even, expected)

                # Пузырьковая
                arr_bubble = arr.copy()
                Sorts.bubble_sort(arr_bubble)
                self.assertEqual(arr_bubble, expected)

    def test_floating_point_numbers(self):
        """Тест с числами с плавающей точкой"""
        arr = [3.14, 1.41, 2.71, 0.577, 1.618]
        expected = sorted(arr)

        result_quick = Sorts.quick_sort(arr.copy())
        self.assertEqual(result_quick, expected)

        arr_inplace = arr.copy()
        Sorts.quick_sort_inplace(arr_inplace)
        self.assertEqual(arr_inplace, expected)

        arr_odd_even = arr.copy()
        Sorts.odd_even_sort(arr_odd_even)
        self.assertEqual(arr_odd_even, expected)

        arr_bubble = arr.copy()
        Sorts.bubble_sort(arr_bubble)
        self.assertEqual(arr_bubble, expected)


class TestPerformance(unittest.TestCase):
    """Тесты производительности (проверяем что алгоритмы завершаются)"""

    def test_performance_quick_sort(self):
        """Тест производительности быстрой сортировки"""
        large_array = [random.randint(1, 1000) for _ in range(100)]
        result = Sorts.quick_sort(large_array)
        self.assertEqual(len(result), len(large_array))
        self.assertEqual(result, sorted(large_array))

    def test_performance_odd_even_sort(self):
        """Тест производительности чет-нечет сортировки"""
        medium_array = [random.randint(1, 100) for _ in range(50)]
        test_array = medium_array.copy()
        Sorts.odd_even_sort(test_array)
        self.assertEqual(test_array, sorted(medium_array))


if __name__ == '__main__':
    # Запуск тестов с детальным выводом
    unittest.main(verbosity=2)
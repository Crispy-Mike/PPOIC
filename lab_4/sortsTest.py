import unittest
import sys
import os
from typing import List, TypeVar
import random


sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from sorts import Sorts

T = TypeVar('T')


class TestNumber:
    """Вспомогательный класс для тестирования сортировки объектов"""

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
        self.test_cases = [
            [],
            [1],
            [1, 2, 3, 4, 5],
            [5, 4, 3, 2, 1],
            [3, 1, 4, 1, 5, 9, 2, 6, 5, 3],
            [-5, -1, -3, 0, 2, -4],
            [7, 7, 7, 7, 7],
        ]

        self.string_test_cases = [
            [],
            ["a"],
            ["a", "b", "c"],
            ["c", "b", "a"],
            ["banana", "apple", "cherry", "date"],
        ]

    def test_quick_sort_basic(self):
        """Тест быстрой сортировки"""
        for arr in self.test_cases:
            with self.subTest(arr=arr):
                original = arr.copy()
                expected = sorted(arr)
                result = Sorts.quick_sort(arr)
                self.assertEqual(result, expected)
                self.assertEqual(arr, original)  # не модифицирует оригинал

        for arr in self.string_test_cases:
            with self.subTest(arr=arr):
                original = arr.copy()
                expected = sorted(arr)
                result = Sorts.quick_sort(arr)
                self.assertEqual(result, expected)
                self.assertEqual(arr, original)

    def test_sorting_network_sort_basic(self):
        """Тест сортировочной сети"""
        for arr in self.test_cases:
            with self.subTest(arr=arr):
                test_arr = arr.copy()
                expected = sorted(arr)
                Sorts.sorting_network_sort(test_arr)
                self.assertEqual(test_arr, expected)

        for arr in self.string_test_cases:
            with self.subTest(arr=arr):
                test_arr = arr.copy()
                expected = sorted(arr)
                Sorts.sorting_network_sort(test_arr)
                self.assertEqual(test_arr, expected)

    def test_custom_comparable_class(self):
        test_objects = [
            TestNumber(5),
            TestNumber(1),
            TestNumber(8),
            TestNumber(3),
            TestNumber(2)
        ]
        expected_values = [1, 2, 3, 5, 8]

        # Quicksort
        result = Sorts.quick_sort(test_objects)
        self.assertEqual([x.value for x in result], expected_values)

        # Sorting network
        test_objects_sn = [TestNumber(x.value) for x in test_objects]
        Sorts.sorting_network_sort(test_objects_sn)
        self.assertEqual([x.value for x in test_objects_sn], expected_values)

    def test_algorithm_consistency(self):
        test_data = [random.randint(1, 100) for _ in range(20)]
        expected = sorted(test_data)

        quick_result = Sorts.quick_sort(test_data.copy())
        sn_data = test_data.copy()
        Sorts.sorting_network_sort(sn_data)

        self.assertEqual(quick_result, expected)
        self.assertEqual(sn_data, expected)

    def test_large_dataset(self):
        large_array = [random.randint(1, 1000) for _ in range(100)]
        expected = sorted(large_array)

        quick_result = Sorts.quick_sort(large_array.copy())
        self.assertEqual(quick_result, expected)

        sn_data = large_array.copy()
        Sorts.sorting_network_sort(sn_data)
        self.assertEqual(sn_data, expected)

    def test_edge_cases(self):
        edge_cases = [[], [42], [2, 1], [1, 1, 1]]
        for arr in edge_cases:
            with self.subTest(arr=arr):
                expected = sorted(arr)

                # Quicksort
                self.assertEqual(Sorts.quick_sort(arr.copy()), expected)

                # Sorting network
                test_arr = arr.copy()
                Sorts.sorting_network_sort(test_arr)
                self.assertEqual(test_arr, expected)


class TestPerformance(unittest.TestCase):

    def test_performance_quick_sort(self):
        large_array = [random.randint(1, 1000) for _ in range(100)]
        result = Sorts.quick_sort(large_array)
        self.assertEqual(result, sorted(large_array))

    def test_performance_sorting_network(self):
        medium_array = [random.randint(1, 100) for _ in range(50)]
        test_array = medium_array.copy()
        Sorts.sorting_network_sort(test_array)
        self.assertEqual(test_array, sorted(medium_array))


if __name__ == '__main__':
    unittest.main(verbosity=2)
from typing import List, TypeVar, Generic
from abc import ABC, abstractmethod

T = TypeVar('T')


class Comparable(ABC):
    @abstractmethod
    def __lt__(self, other):
        pass

    @abstractmethod
    def __gt__(self, other):
        pass


class Sorts:
    """Класс с различными алгоритмами сортировки"""

    @staticmethod
    def quick_sort(arr: List[T]) -> List[T]:
        """Быстрая сортировка для списков"""
        if len(arr) <= 1:
            return arr

        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]

        return Sorts.quick_sort(left) + middle + Sorts.quick_sort(right)

    @staticmethod
    def quick_sort_inplace(arr: List[T], low: int = 0, high: int = None) -> None:
        """Быстрая сортировка на месте"""
        if high is None:
            high = len(arr) - 1

        if low < high:
            pi = Sorts._partition(arr, low, high)
            Sorts.quick_sort_inplace(arr, low, pi - 1)
            Sorts.quick_sort_inplace(arr, pi + 1, high)

    @staticmethod
    def _partition(arr: List[T], low: int, high: int) -> int:
        """Вспомогательная функция для быстрой сортировки"""
        pivot = arr[high]
        i = low - 1

        for j in range(low, high):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]

        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1

    @staticmethod
    def odd_even_sort(arr: List[T]) -> None:
        """Сортировка чет-нечет (сортировочная сеть)"""
        n = len(arr)
        is_sorted = False

        while not is_sorted:
            is_sorted = True

            # Нечетные индексы
            for i in range(1, n - 1, 2):
                if arr[i] > arr[i + 1]:
                    arr[i], arr[i + 1] = arr[i + 1], arr[i]
                    is_sorted = False

            # Четные индексы
            for i in range(0, n - 1, 2):
                if arr[i] > arr[i + 1]:
                    arr[i], arr[i + 1] = arr[i + 1], arr[i]
                    is_sorted = False

    @staticmethod
    def bubble_sort(arr: List[T]) -> None:
        """Пузырьковая сортировка (еще один вид сортировочной сети)"""
        n = len(arr)
        for i in range(n):
            for j in range(0, n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
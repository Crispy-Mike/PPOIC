from typing import List, TypeVar

T = TypeVar('T')


class Sorts:
    """Класс с двумя алгоритмами сортировки: Quicksort и Sorting Network"""

    @staticmethod
    def quick_sort(arr: List[T]) -> List[T]:
        """Быстрая сортировка (не на месте)"""
        if len(arr) <= 1:
            return arr
        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]
        return Sorts.quick_sort(left) + middle + Sorts.quick_sort(right)

    @staticmethod
    def sorting_network_sort(arr: List[T]) -> None:
        """
        Сортировка с помощью сортирующей сети (Odd-Even Transposition Sort).
        Работает на месте. Гарантированно сортирует массив любой длины.
        """
        n = len(arr)
        if n <= 1:
            return

        # Повторяем проходы, пока массив не отсортирован
        for _ in range(n):
            # Нечётные фазы: сравниваем (1,2), (3,4), ...
            for i in range(1, n - 1, 2):
                if arr[i] > arr[i + 1]:
                    arr[i], arr[i + 1] = arr[i + 1], arr[i]
            # Чётные фазы: сравниваем (0,1), (2,3), ...
            for i in range(0, n - 1, 2):
                if arr[i] > arr[i + 1]:
                    arr[i], arr[i + 1] = arr[i + 1], arr[i]
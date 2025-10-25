from sorts import Sorts
from Student import Student


def demonstrate_builtin_types():
    """Демонстрация сортировки встроенных типов"""
    print("=" * 50)
    print("СОРТИРОВКА ВСТРОЕННЫХ ТИПОВ")
    print("=" * 50)

    # Сортировка целых чисел
    numbers = [64, 34, 25, 12, 22, 11, 90, 5]
    print(f"Исходный массив чисел: {numbers}")

    numbers_quick = numbers.copy()
    sorted_numbers = Sorts.quick_sort(numbers_quick)
    print(f"Быстрая сортировка:    {sorted_numbers}")

    numbers_odd_even = numbers.copy()
    Sorts.odd_even_sort(numbers_odd_even)
    print(f"Чет-нечет сортировка:  {numbers_odd_even}")

    # Сортировка строк
    words = ["banana", "apple", "cherry", "date", "elderberry"]
    print(f"\nИсходный массив слов: {words}")

    words_quick = words.copy()
    sorted_words = Sorts.quick_sort(words_quick)
    print(f"Быстрая сортировка:    {sorted_words}")

    words_bubble = words.copy()
    Sorts.bubble_sort(words_bubble)
    print(f"Пузырьковая сортировка: {words_bubble}")


def demonstrate_custom_class():
    """Демонстрация сортировки пользовательского класса"""
    print("\n" + "=" * 50)
    print("СОРТИРОВКА ПОЛЬЗОВАТЕЛЬСКОГО КЛАССА")
    print("=" * 50)

    # Создаем массив студентов
    students = [
        Student("Alice", 20, 4.5),
        Student("Bob", 19, 3.8),
        Student("Charlie", 22, 4.2),
        Student("Diana", 21, 4.8),
        Student("Eve", 18, 3.9)
    ]

    print("Исходный список студентов:")
    for student in students:
        print(f"  {student}")

    # Сортировка быстрой сортировкой (по возрасту - используется __lt__)
    students_quick = students.copy()
    sorted_students = Sorts.quick_sort(students_quick)

    print("\nПосле быстрой сортировки (по возрасту):")
    for student in sorted_students:
        print(f"  {student}")

    # Сортировка чет-нечет (по возрасту - используется __lt__)
    students_odd_even = students.copy()
    Sorts.odd_even_sort(students_odd_even)

    print("\nПосле чет-нечет сортировки (по возрасту):")
    for student in students_odd_even:
        print(f"  {student}")

    # Демонстрация с разными компараторами
    print("\n" + "-" * 50)
    print("Сортировка с кастомными компараторами:")
    print("-" * 50)

    # Сортировка по оценке с использованием лямбда-функции
    students_by_grade = students.copy()
    # Используем sorted() с кастомным ключом для демонстрации гибкости
    students_by_grade_sorted = sorted(students_by_grade, key=lambda x: x.grade)

    print("Сортировка по оценке (по убыванию):")
    for student in reversed(students_by_grade_sorted):
        print(f"  {student}")

    # Сортировка по имени
    students_by_name = students.copy()
    students_by_name_sorted = sorted(students_by_name, key=lambda x: x.name)

    print("\nСортировка по имени:")
    for student in students_by_name_sorted:
        print(f"  {student}")


def performance_comparison():
    """Сравнение производительности на разных типах данных"""
    print("\n" + "=" * 50)
    print("СРАВНЕНИЕ РАЗЛИЧНЫХ АЛГОРИТМОВ")
    print("=" * 50)

    import time
    import random

    # Генерируем тестовые данные
    test_data = [random.randint(1, 1000) for _ in range(100)]

    # Тестируем быструю сортировку
    data1 = test_data.copy()
    start_time = time.time()
    sorted_data = Sorts.quick_sort(data1)
    quick_time = time.time() - start_time

    # Тестируем чет-нечет сортировку
    data2 = test_data.copy()
    start_time = time.time()
    Sorts.odd_even_sort(data2)
    odd_even_time = time.time() - start_time

    # Тестируем пузырьковую сортировку
    data3 = test_data.copy()
    start_time = time.time()
    Sorts.bubble_sort(data3)
    bubble_time = time.time() - start_time

    print(f"Быстрая сортировка:  {quick_time:.6f} секунд")
    print(f"Чет-нечет сортировка: {odd_even_time:.6f} секунд")
    print(f"Пузырьковая сортировка: {bubble_time:.6f} секунд")
    print(f"\nРезультаты корректны: {sorted_data == data2 == data3}")


if __name__ == "__main__":
    demonstrate_builtin_types()
    demonstrate_custom_class()
    performance_comparison()
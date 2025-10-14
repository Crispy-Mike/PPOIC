from Student import Student
from cocktail_sort import *
from strand_sort import *

def get_user_input():
    """Получение данных от пользователя"""
    print("\nВыберите тип данных для сортировки:")
    print("1. Целые числа")
    print("2. Строки")
    print("3. Студенты (имя и оценка)")

    choice = input("Ваш выбор (1-3): ").strip()

    if choice == "1":
        print("Введите целые числа через пробел:")
        data = input().split()
        try:
            return [int(x) for x in data]
        except ValueError:
            print("Ошибка! Введите только целые числа.")
            return get_user_input()

    elif choice == "2":
        print("Введите строки через пробел:")
        return input().split()

    elif choice == "3":
        students = []
        print("Введите данные студентов в формате: Имя Оценка")
        print("Для завершения введите 'stop'")
        while True:
            line = input().strip()
            if line.lower() == 'stop':
                break
            if line:
                parts = line.split()
                if len(parts) >= 2:
                    try:
                        name = parts[0]
                        score = int(parts[1])
                        students.append(Student(name, score))
                    except ValueError:
                        print("Ошибка! Оценка должна быть числом.")
                else:
                    print("Ошибка! Введите имя и оценку через пробел.")
        return students

    else:
        print("Неверный выбор!")
        return get_user_input()


def demonstrate_sorting():
    print("=" * 50)
    print("ДЕМОНСТРАЦИЯ РАБОТЫ АЛГОРИТМОВ СОРТИРОВКИ")
    print("=" * 50)

    print("\nВыберите режим:")
    print("1. Автоматическая демонстрация")
    print("2. Ручной ввод данных")

    mode = input("Ваш выбор (1-2): ").strip()

    if mode == "1":
        # Автоматическая демонстрация
        print("\n1. Сортировка целых чисел (Cocktail Sort):")
        numbers = [64, 34, 25, 12, 22, 11, 90, 5]
        print(f"До сортировки:    {numbers}")
        numbers_copy = numbers.copy()
        cocktail_sort(numbers_copy)
        print(f"После сортировки: {numbers_copy}")

        print("\n2. Сортировка строк (Strand Sort):")
        words = ["banana", "apple", "cherry", "date", "blueberry"]
        print(f"До сортировки:    {words}")
        sorted_words = strand_sort(words)
        print(f"После сортировки: {sorted_words}")

        print("\n3. Сортировка студентов по оценкам:")
        students = [
            Student("Анна", 85),
            Student("Иван", 72),
            Student("Мария", 95),
            Student("Петр", 68),
            Student("Ольга", 91)
        ]

        print("До сортировки:")
        for student in students:
            print(f"  {student}")

        students_copy = students.copy()
        cocktail_sort(students_copy)

        print("\nПосле Cocktail Sort:")
        for student in students_copy:
            print(f"  {student}")

        students_sorted = strand_sort(students)

        print("\nПосле Strand Sort:")
        for student in students_sorted:
            print(f"  {student}")

    elif mode == "2":
        # Ручной ввод
        data = get_user_input()

        print(f"\nДо сортировки: {data}")

        # Cocktail sort
        data_cocktail = data.copy() if hasattr(data, 'copy') else data[:]
        cocktail_sort(data_cocktail)
        print(f"После Cocktail Sort: {data_cocktail}")

        # Strand sort
        data_strand = strand_sort(data)
        print(f"После Strand Sort: {data_strand}")

    else:
        print("Неверный выбор! Запускаю автоматическую демонстрацию.")
        demonstrate_sorting()


def test_edge_cases():
    print("\n" + "=" * 50)
    print("ТЕСТИРОВАНИЕ КРАЙНИХ СЛУЧАЕВ")
    print("=" * 50)

    empty_arr = []
    cocktail_sort(empty_arr)
    print(f"Пустой массив: {empty_arr}")

    single_arr = [42]
    cocktail_sort(single_arr)
    print(f"Один элемент: {single_arr}")

    sorted_arr = [1, 2, 3, 4, 5]
    cocktail_sort(sorted_arr)
    print(f"Уже отсортированный: {sorted_arr}")

    reverse_arr = [5, 4, 3, 2, 1]
    cocktail_sort(reverse_arr)
    print(f"Обратный порядок: {reverse_arr}")


if __name__ == "__main__":
    demonstrate_sorting()
    test_edge_cases()
    print("\n" + "=" * 50)
    print("ВСЕ ТЕСТЫ ЗАВЕРШЕНЫ!")
    print("=" * 50)
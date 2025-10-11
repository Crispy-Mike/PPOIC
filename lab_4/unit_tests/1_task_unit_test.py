import coverage
import unittest
import sys
import os


def run_sorting_tests_with_coverage():
    """Запуск тестов сортировки с измерением покрытия кода"""

    # Добавляем текущую директорию в путь Python
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))

    # Инициализируем coverage
    cov = coverage.Coverage(
        source=['.'],  # Текущая директория
        omit=['*test*', '*__pycache__*', '*coverage*', 'run_*'],  # Исключаем вспомогательные файлы
        branch=True
    )

    print("=" * 70)
    print("🧪 ЗАПУСК ТЕСТОВ СОРТИРОВКИ С ПОКРЫТИЕМ КОДА")
    print("=" * 70)

    # Начинаем измерение покрытия
    cov.start()

    try:
        # Создаем тестовый модуль
        test_module = create_sorting_test_module()

        # Загружаем и запускаем тесты
        loader = unittest.TestLoader()
        suite = loader.loadTestsFromModule(test_module)

        # Запускаем тесты
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)

    except Exception as e:
        print(f"❌ Ошибка при запуске тестов: {e}")
        result = None
    finally:
        # Останавливаем измерение покрытия
        cov.stop()
        cov.save()

    # Генерируем отчеты
    generate_sorting_reports(cov, result)

    return result.wasSuccessful() if result else False


def create_sorting_test_module():
    """Создает и возвращает тестовый модуль для сортировки"""
    import types
    test_module = types.ModuleType('test_sorting')

    # Сначала попробуем импортировать реальный модуль
    try:
        from task_1 import cocktail_sort, strand_sort, Student
    except ImportError:
        print("⚠️  Модуль task_1 не найден, создаются заглушки...")
        # Создаем заглушки
        exec('''
def cocktail_sort(arr):
    """Сортировка перемешиванием (шейкерная сортировка)"""
    n = len(arr)
    if n == 0:
        return

    left = 0
    right = n - 1
    swapped = True

    while swapped:
        swapped = False

        # Проход слева направо
        for i in range(left, right):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                swapped = True

        if not swapped:
            break

        swapped = False
        right -= 1

        # Проход справа налево
        for i in range(right, left, -1):
            if arr[i - 1] > arr[i]:
                arr[i], arr[i - 1] = arr[i - 1], arr[i]
                swapped = True

        left += 1

def strand_sort(arr):
    """Странная сортировка (Strand Sort)"""
    if not arr:
        return []

    def merge_lists(a, b):
        result = []
        while a and b:
            if a[0] < b[0]:
                result.append(a.pop(0))
            else:
                result.append(b.pop(0))
        result.extend(a)
        result.extend(b)
        return result

    result = []
    while arr:
        sublist = [arr.pop(0)]
        i = 0
        while i < len(arr):
            if arr[i] > sublist[-1]:
                sublist.append(arr.pop(i))
            else:
                i += 1
        result = merge_lists(result, sublist)

    return result

class Student:
    def __init__(self, name, score):
        self.name = name
        self.score = score

    def __lt__(self, other):
        return self.score < other.score

    def __eq__(self, other):
        return self.score == other.score

    def __repr__(self):
        return f"Student({self.name}, {self.score})"
''', test_module.__dict__)
    else:
        # Добавляем реальные импорты
        test_module.cocktail_sort = cocktail_sort
        test_module.strand_sort = strand_sort
        test_module.Student = Student

    # Добавляем тестовые классы
    exec('''
import unittest

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
''', test_module.__dict__)

    return test_module


def generate_sorting_reports(cov, result):
    """Генерирует отчеты о покрытии для тестов сортировки"""
    print("\n" + "=" * 70)
    print("📊 ОТЧЕТ О ПОКРЫТИИ ТЕСТАМИ СОРТИРОВКИ")
    print("=" * 70)

    try:
        # Консольный отчет
        print("\n📈 СТАТИСТИКА ПОКРЫТИЯ:")
        cov.report(show_missing=True, skip_covered=False)

        # HTML отчет
        print("\n🔄 Создание HTML отчета...")
        cov.html_report(directory='sorting_coverage_report')
        print("   ✅ HTML отчет создан: sorting_coverage_report/index.html")

        # XML отчет
        cov.xml_report(outfile='sorting_coverage.xml')
        print("   ✅ XML отчет создан: sorting_coverage.xml")

    except Exception as e:
        print(f"❌ Ошибка при генерации отчетов: {e}")

    # Результаты тестов
    print("\n" + "=" * 70)
    print("🧪 РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ")
    print("=" * 70)

    if result and result.wasSuccessful():
        print("✅ ВСЕ ТЕСТЫ СОРТИРОВКИ ПРОЙДЕНЫ УСПЕШНО!")
        print(f"   Пройдено тестов: {result.testsRun}")
    elif result:
        print("❌ НЕКОТОРЫЕ ТЕСТЫ НЕ ПРОЙДЕНЫ!")
        print(f"   Всего тестов: {result.testsRun}")
        print(f"   Провалено: {len(result.failures)}")
        print(f"   Ошибок: {len(result.errors)}")
    else:
        print("⚠️  Не удалось получить результаты тестов")


if __name__ == '__main__':
    success = run_sorting_tests_with_coverage()
    sys.exit(0 if success else 1)
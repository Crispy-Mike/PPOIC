import coverage
import unittest
import os
import sys

sys.path.append(os.path.dirname(__file__))

from test_Tag_Game import TestTag_GameLogic

def run_tests_with_coverage():
    cov = coverage.Coverage()
    cov.start()

    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestTag_GameLogic)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    cov.stop()
    cov.save()

    print("\n" + "=" * 60)
    print("ОТЧЕТ О ПОКРЫТИИ ТЕСТАМИ")
    print("=" * 60)
    cov.report()

    cov.html_report(directory='htmlcov')
    print(f"\nДетальный HTML отчет создан в папке 'htmlcov'")

    print("\nФайлы с покрытием:")
    for module in cov.get_data().measured_files():
        print(f"  - {os.path.basename(module)}")

    return result.wasSuccessful()

if __name__ == "__main__":
    print("Запуск тестов с измерением покрытия...")
    print("=" * 50)

    success = run_tests_with_coverage()

    print("\n" + "=" * 50)
    if success:
        print("✅ ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
    else:
        print("❚ НЕКОТОРЫЕ ТЕСТЫ НЕ ПРОЙДЕНЫ!")
    print("=" * 50)
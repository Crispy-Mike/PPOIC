import unittest
import sys
import os

# Добавляем путь для импорта тестов
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Импортируем тестовый модуль
import Unit_tests.test_airline_system  # замените your_test_file на имя вашего файла с тестами

if __name__ == '__main__':
    # Создаем test loader
    loader = unittest.TestLoader()

    # Загружаем тесты из модуля
    suite = loader.loadTestsFromModule(Unit_tests.test_airline_system)

    # Запускаем тесты
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
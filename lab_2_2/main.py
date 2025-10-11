import unittest
import sys
import os
# Добавляем путь для импорта тестов
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


import Unit_tests.BankSystemTest

if __name__ == '__main__':
    # Создаем test loader
    loader = unittest.TestLoader()

    # Загружаем тесты из модуля
    suite = loader.loadTestsFromModule(Unit_tests.BankSystemTest)

    # Запускаем тесты
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
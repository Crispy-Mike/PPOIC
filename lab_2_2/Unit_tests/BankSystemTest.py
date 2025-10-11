import coverage
import unittest
import sys
import os

# Добавляем путь к проекту для импорта модулей
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')


def run_tests_with_coverage():
    """Запуск тестов с измерением покрытия кода"""

    # Инициализируем coverage
    cov = coverage.Coverage(
        source=['Classes'],  # Указываем папку с исходным кодом
        omit=['*test*', '*__pycache__*'],  # Исключаем тесты и кэш
        branch=True  # Включаем измерение покрытия ветвей
    )

    # Начинаем измерение покрытия
    cov.start()

    print("=" * 70)
    print("ЗАПУСК ТЕСТОВ С ИЗМЕРЕНИЕМ ПОКРЫТИЯ КОДА")
    print("=" * 70)

    try:
        # Загружаем и запускаем тесты
        loader = unittest.TestLoader()
        suite = loader.loadTestsFromName('test_bank_system')

        # Запускаем тесты
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)

    finally:
        # Останавливаем измерение покрытия
        cov.stop()
        cov.save()

    print("\n" + "=" * 70)
    print("ОТЧЕТ О ПОКРЫТИИ ТЕСТАМИ")
    print("=" * 70)

    # Выводим отчет в консоль
    cov.report(show_missing=True, skip_covered=False)

    # Генерируем HTML отчет
    print("\nГенерация HTML отчета...")
    cov.html_report(
        directory='coverage_report',
        title='Отчет покрытия тестами - Банковская система'
    )

    # Генерируем XML отчет (для CI/CD)
    cov.xml_report(outfile='coverage.xml')

    # Анализируем покрытие по файлам
    print("\n" + "=" * 70)
    print("ДЕТАЛЬНАЯ ИНФОРМАЦИЯ О ПОКРЫТИИ")
    print("=" * 70)

    analyzed_files = cov.get_data().measured_files()
    for file_path in analyzed_files:
        file_name = os.path.basename(file_path)
        if 'Classes' in file_path:
            analysis = cov.analysis(file_path)
            covered_lines = len(analysis[1])
            missing_lines = len(analysis[2])
            total_lines = covered_lines + missing_lines
            coverage_percent = (covered_lines / total_lines * 100) if total_lines > 0 else 0

            print(f"\n📊 {file_name}:")
            print(f"   Покрыто: {covered_lines}/{total_lines} строк ({coverage_percent:.1f}%)")
            if missing_lines > 0:
                print(f"   Непокрытые строки: {missing_lines}")

    # Выводим общую статистику
    print("\n" + "=" * 70)
    print("ОБЩАЯ СТАТИСТИКА")
    print("=" * 70)

    total_stats = cov.report(show_missing=False)
    coverage_percentage = cov.html_report(directory='coverage_report')

    # Проверяем результат тестов
    if result.wasSuccessful():
        print("✅ ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
    else:
        print("❌ НЕКОТОРЫЕ ТЕСТЫ НЕ ПРОЙДЕНЫ!")
        print(f"   Тестов пройдено: {result.testsRun - len(result.failures) - len(result.errors)}/{result.testsRun}")
        if result.failures:
            print(f"   Проваленных тестов: {len(result.failures)}")
        if result.errors:
            print(f"   Ошибочных тестов: {len(result.errors)}")

    print(f"\n📁 HTML отчет сохранен в папке: coverage_report/")
    print(f"📊 XML отчет сохранен в файле: coverage.xml")
    print("=" * 70)

    return result.wasSuccessful()


if __name__ == '__main__':
    # Сохраняем текущий тестовый код в файл
    test_code = '''
import unittest
import sys
import os

# Добавляем путь к проекту для импорта модулей
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')

from Classes.Bank import Bank
from Classes.BankAccount import BankAccount, InsufficientFundsError, InvalidTransactionError
from Classes.BankStatement import BankStatement
from Classes.Branch import Branch
from Classes.BranchManager import BranchManager
from Classes.AuthService import AuthService, AuthenticationError
from Classes.BiometricScanner import BiometricScanner
from Classes.AuditReport import AuditReport


class TestBank(unittest.TestCase):
    """Тесты для класса Bank"""

    def test_init(self):
        """Тест инициализации банка"""
        bank = Bank("Сбербанк")
        self.assertEqual(bank.name_bank, "Сбербанк")
        self.assertEqual(bank.branches, [])
        self.assertEqual(bank.currency_rates, {})

    def test_add_currency_rate(self):
        """Тест добавления курса валют"""
        bank = Bank("Сбербанк")

        # Создаем mock-объекты для валют
        class MockCurrency:
            def __init__(self, code):
                self.code = code

        from_currency = MockCurrency('USD')
        to_currency = MockCurrency('RUB')

        bank.add_currency_rate(from_currency, to_currency, 75.5)
        self.assertEqual(bank.currency_rates[('USD', 'RUB')], 75.5)

    def test_get_currency_rate(self):
        """Тест получения курса валют"""
        bank = Bank("Сбербанк")

        class MockCurrency:
            def __init__(self, code):
                self.code = code

        from_currency = MockCurrency('USD')
        to_currency = MockCurrency('RUB')

        bank.add_currency_rate(from_currency, to_currency, 75.5)
        rate = bank.get_currency_rate(from_currency, to_currency)
        self.assertEqual(rate, 75.5)

        # Тест для несуществующего курса
        eur_currency = MockCurrency('EUR')
        non_existent_rate = bank.get_currency_rate(from_currency, eur_currency)
        self.assertIsNone(non_existent_rate)


class TestBankAccount(unittest.TestCase):
    """Тесты для класса BankAccount"""

    def setUp(self):
        """Настройка перед каждым тестом"""

        class MockCurrency:
            def __init__(self, code):
                self.code = code

        self.currency = MockCurrency('RUB')

    def test_init(self):
        """Тест инициализации банковского счета"""
        account = BankAccount("1234567890", "дебетовый", self.currency, 1000.0)

        self.assertEqual(account.account_number, "1234567890")
        self.assertEqual(account.account_type, "дебетовый")
        self.assertEqual(account.currency.code, "RUB")
        self.assertEqual(account.balance, 1000.0)
        self.assertIsNone(account.owner)

    def test_deposit_positive_amount(self):
        """Тест внесения средств на счет"""
        account = BankAccount("1234567890", "дебетовый", self.currency, 1000.0)

        new_balance = account.deposit(500.0)
        self.assertEqual(new_balance, 1500.0)
        self.assertEqual(account.balance, 1500.0)

    def test_deposit_negative_amount(self):
        """Тест внесения отрицательной суммы"""
        account = BankAccount("1234567890", "дебетовый", self.currency, 1000.0)

        with self.assertRaises(InvalidTransactionError):
            account.deposit(-100.0)

    def test_withdraw_sufficient_funds(self):
        """Тест снятия средств при достаточном балансе"""
        account = BankAccount("1234567890", "дебетовый", self.currency, 1000.0)

        new_balance = account.withdraw(300.0)
        self.assertEqual(new_balance, 700.0)
        self.assertEqual(account.balance, 700.0)

    def test_withdraw_insufficient_funds(self):
        """Тест снятия средств при недостаточном балансе"""
        account = BankAccount("1234567890", "дебетовый", self.currency, 1000.0)

        with self.assertRaises(InsufficientFundsError):
            account.withdraw(1500.0)

    def test_withdraw_negative_amount(self):
        """Тест снятия отрицательной суммы"""
        account = BankAccount("1234567890", "дебетовый", self.currency, 1000.0)

        with self.assertRaises(InvalidTransactionError):
            account.withdraw(-100.0)


class TestBankStatement(unittest.TestCase):
    """Тесты для класса BankStatement"""

    def test_init(self):
        """Тест инициализации банковской выписки"""

        class MockAccount:
            def __init__(self, account_number):
                self.account_number = account_number

        account = MockAccount('1234567890')
        transactions = []

        statement = BankStatement("STMT001", account, "2024-01-01", "2024-01-31", transactions)

        self.assertEqual(statement.statement_id, "STMT001")
        self.assertEqual(statement.account.account_number, "1234567890")
        self.assertEqual(statement.period_start, "2024-01-01")
        self.assertEqual(statement.period_end, "2024-01-31")
        self.assertEqual(statement.transactions, [])

    def test_generate_statement(self):
        """Тест генерации выписки"""

        class MockAccount:
            def __init__(self, account_number):
                self.account_number = account_number

        class MockTransaction:
            def __init__(self, amount):
                self.amount = amount

        account = MockAccount('1234567890')
        transactions = [
            MockTransaction(100.0),
            MockTransaction(-50.0)
        ]

        statement = BankStatement("STMT001", account, "2024-01-01", "2024-01-31", transactions)
        statement.opening_balance = 500.0

        result = statement.generate_statement()
        self.assertEqual(result, "Выписка для счета 1234567890")
        self.assertEqual(statement.closing_balance, 550.0)  # 500 + 100 - 50


class TestBranch(unittest.TestCase):
    """Тесты для класса Branch"""

    def test_init(self):
        """Тест инициализации филиала"""
        branch = Branch("Центральный филиал", "ул. Ленина, 1", "BR001")

        self.assertEqual(branch.name_branch, "Центральный филиал")
        self.assertEqual(branch.address, "ул. Ленина, 1")
        self.assertEqual(branch.branch_code, "BR001")
        self.assertEqual(branch.customers, [])
        self.assertEqual(branch.employees, [])

    def test_add_atm(self):
        """Тест добавления банкомата в филиал"""

        class MockATM:
            def __init__(self):
                self.branch = None

        branch = Branch("Центральный филиал", "ул. Ленина, 1", "BR001")
        atm = MockATM()

        branch.add_atm(atm)
        self.assertIn(atm, branch.atms)
        self.assertEqual(atm.branch, branch)



class TestAuthService(unittest.TestCase):
    """Тесты для класса AuthService"""

    def test_init(self):
        """Тест инициализации службы аутентификации"""
        auth_service = AuthService("AUTH001", "active", "high", 3, 300)

        self.assertEqual(auth_service.system_id, "AUTH001")
        self.assertEqual(auth_service.system_type, "authentication")
        self.assertEqual(auth_service.status, "active")
        self.assertEqual(auth_service.security_level, "high")
        self.assertEqual(auth_service.max_attempts, 3)
        self.assertEqual(auth_service.timeout_duration, 300)
        self.assertTrue(auth_service.two_factor_enabled)

    def test_authenticate_user_success(self):
        """Тест успешной аутентификации пользователя"""
        auth_service = AuthService("AUTH001", "active", "high", 3, 300)

        result = auth_service.authenticate_user("user123", "password123")
        self.assertTrue(result)

    def test_authenticate_user_too_many_attempts(self):
        """Тест аутентификации при превышении попыток"""
        auth_service = AuthService("AUTH001", "active", "high", 3, 300)
        auth_service.failed_attempts = 3  # Симулируем превышение попыток

        with self.assertRaises(AuthenticationError):
            auth_service.authenticate_user("user123", "wrong_password")


class TestBiometricScanner(unittest.TestCase):
    """Тесты для класса BiometricScanner"""

    def test_init(self):
        """Тест инициализации биометрического сканера"""
        scanner = BiometricScanner("SCAN001", "fingerprint", 99.5, True)

        self.assertEqual(scanner.scanner_id, "SCAN001")
        self.assertEqual(scanner.scanner_type, "fingerprint")
        self.assertEqual(scanner.accuracy, 99.5)
        self.assertTrue(scanner.is_enabled)

    def test_scanner_disabled(self):
        """Тест отключенного сканера"""
        scanner = BiometricScanner("SCAN002", "retina", 98.0, False)

        self.assertEqual(scanner.scanner_id, "SCAN002")
        self.assertEqual(scanner.scanner_type, "retina")
        self.assertFalse(scanner.is_enabled)


class TestAuditReport(unittest.TestCase):
    """Тесты для класса AuditReport"""

    def test_init(self):
        """Тест инициализации аудиторского отчета"""
        data = {"transactions": 1000, "errors": 5}

        class MockAuditor:
            def __init__(self, name):
                self.name = name

        auditor = MockAuditor('Иван Аудиторов')

        report = AuditReport("AUDIT001", "2024-01-01", data, auditor)

        self.assertEqual(report.report_id, "AUDIT001")
        self.assertEqual(report.report_type, "audit")
        self.assertEqual(report.generation_date, "2024-01-01")
        self.assertEqual(report.data, data)
        self.assertEqual(report.auditor.name, "Иван Аудиторов")
        self.assertEqual(report.findings, [])
        self.assertEqual(report.recommendations, [])

    def test_add_finding(self):
        """Тест добавления находки аудита"""
        data = {"transactions": 1000, "errors": 5}

        class MockAuditor:
            def __init__(self, name):
                self.name = name

        auditor = MockAuditor('Иван Аудиторов')

        report = AuditReport("AUDIT001", "2024-01-01", data, auditor)
        report.add_finding("Обнаружена недостача средств")
        report.add_finding("Нарушение процедур безопасности")

        self.assertEqual(len(report.findings), 2)
        self.assertIn("Обнаружена недостача средств", report.findings)
        self.assertIn("Нарушение процедур безопасности", report.findings)


if __name__ == '__main__':
    # Создаем тестовый suite и запускаем
    unittest.main(verbosity=2)
'''

    # Сохраняем тесты во временный файл
    with open('test_bank_system.py', 'w', encoding='utf-8') as f:
        f.write(test_code)

    # Запускаем тесты с покрытием
    success = run_tests_with_coverage()

    # Удаляем временный файл
    try:
        os.remove('test_bank_system.py')
    except:
        pass

    # Завершаем с соответствующим кодом выхода
    sys.exit(0 if success else 1)
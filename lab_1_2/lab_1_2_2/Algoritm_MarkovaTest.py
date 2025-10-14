import unittest
from unittest.mock import patch
import io
from Algoritm_Markova import Algoritm_Markova

class TestAlgoritmMarkova(unittest.TestCase):

    def setUp(self):
        """Настройка тестового окружения перед каждым тестом"""
        self.algo = Algoritm_Markova()

    def test_initial_state(self):
        """Тест начального состояния объекта"""
        self.assertEqual(self.algo.rules, [])
        self.assertEqual(self.algo._Algoritm_Markova__first, "")
        self.assertEqual(self.algo._Algoritm_Markova__second, "")
        self.assertFalse(self.algo._Algoritm_Markova__terminal)

    @patch('builtins.input', side_effect=["abc", "def", "да"])
    def test_input_info_terminal_true(self, mock_input):
        """Тест ввода информации с терминальным правилом"""
        self.algo.input_info()

        self.assertEqual(len(self.algo.rules), 1)
        self.assertEqual(self.algo.rules[0], ("abc", "def", True))
        self.assertEqual(self.algo._Algoritm_Markova__first, "abc")
        self.assertEqual(self.algo._Algoritm_Markova__second, "def")
        self.assertTrue(self.algo._Algoritm_Markova__terminal)

    @patch('builtins.input', side_effect=["test", "replace", "нет"])
    def test_input_info_terminal_false(self, mock_input):
        """Тест ввода информации с нетерминальным правилом"""
        self.algp.input_info()

        self.assertEqual(len(self.algo.rules), 1)
        self.assertEqual(self.algo.rules[0], ("test", "replace", False))

    @patch('builtins.input', side_effect=["a", "b", "да", "x", "y", "нет"])
    def test_multiple_input_info(self, mock_input):
        """Тест добавления нескольких правил"""
        self.algo.input_info()
        self.algo.input_info()

        self.assertEqual(len(self.algo.rules), 2)
        self.assertEqual(self.algo.rules[0], ("a", "b", True))
        self.assertEqual(self.algo.rules[1], ("x", "y", False))

    def test_get_info_empty_rules(self):
        """Тест вывода информации при пустом списке правил"""
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            self.algo.get_info()
            output = mock_stdout.getvalue()
            self.assertEqual(output, "")  # Ничего не должно выводиться

    @patch('builtins.input', side_effect=["hello", "world", "да"])
    def test_get_info_with_rules(self, mock_input):
        """Тест вывода информации с правилами"""
        self.algo.input_info()

        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            self.algo.get_info()
            output = mock_stdout.getvalue()
            self.assertIn("hello->world", output)
            self.assertIn("(True)", output)

    def test_main_algoritm_no_rules(self):
        """Тест основного алгоритма без правил"""
        result = self.algo.main_algoritm("test string")
        self.assertEqual(result, "test string")

    def test_main_algoritm_single_rule(self):
        """Тест основного алгоритма с одним правилом"""
        self.algo.rules = [("a", "b", False)]
        result = self.algo.main_algoritm("abc")
        self.assertEqual(result, "bbc")

    def test_main_algoritm_multiple_rules(self):
        """Тест основного алгоритма с несколькими правилами"""
        self.algo.rules = [
            ("a", "x", False),
            ("b", "y", False),
            ("c", "z", False)
        ]
        result = self.algo.main_algoritm("abc")
        self.assertEqual(result, "xyz")

    def test_main_algoritm_no_pattern_found(self):
        """Тест случая, когда паттерн не найден"""
        self.algo.rules = [("x", "y", False)]
        result = self.algo.main_algoritm("abc")
        self.assertEqual(result, "abc")

    def test_main_algoritm_priority_order(self):
        """Тест приоритета правил (первое подходящее применяется)"""
        self.algo.rules = [
            ("ab", "1", False),
            ("a", "2", False),
            ("b", "3", False)
        ]
        result = self.algo.main_algoritm("abc")
        # Должно примениться правило "ab" -> "1", а не "a" -> "2"
        self.assertEqual(result, "1c")

    @patch('builtins.input', side_effect=["1"])
    def test_delete_rule_single(self, mock_input):
        """Тест удаления единственного правила"""
        self.algo.rules = [("a", "b", False)]

        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            self.algo.delete_rule()
            output = mock_stdout.getvalue()
            self.assertIn("Правило удалено: a -> b", output)

        self.assertEqual(len(self.algo.rules), 0)

    @patch('builtins.input', side_effect=["2"])
    def test_delete_rule_multiple(self, mock_input):
        """Тест удаления правила из нескольких"""
        self.algo.rules = [
            ("a", "1", False),
            ("b", "2", False),
            ("c", "3", False)
        ]

        self.algo.delete_rule()
        self.assertEqual(len(self.algo.rules), 2)
        self.assertEqual(self.algo.rules[0], ("a", "1", False))
        self.assertEqual(self.algo.rules[1], ("c", "3", False))

    @patch('builtins.input', side_effect=["5"])  # Неверный номер
    def test_delete_rule_invalid_index(self, mock_input):
        """Тест удаления с неверным номером правила"""
        self.algo.rules = [("a", "b", False)]

        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            self.algo.delete_rule()
            output = mock_stdout.getvalue()
            self.assertIn("Неверный номер правила!", output)

        self.assertEqual(len(self.algo.rules), 1)

    @patch('builtins.input', side_effect=["abc"])  # Не число
    def test_delete_rule_invalid_input(self, mock_input):
        """Тест удаления с некорректным вводом"""
        self.algo.rules = [("a", "b", False)]

        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            self.algo.delete_rule()
            output = mock_stdout.getvalue()
            self.assertIn("Ошибка при удалении правила", output)

        self.assertEqual(len(self.algo.rules), 1)

    def test_delete_rule_empty_rules(self):
        """Тест удаления при пустом списке правил"""
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            self.algo.delete_rule()
            output = mock_stdout.getvalue()
            self.assertIn("Правил нет!", output)

    def test_clear_all_rules(self):
        """Тест очистки всех правил"""
        self.algo.rules = [
            ("a", "1", False),
            ("b", "2", True),
            ("c", "3", False)
        ]

        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            self.algo.clear_all_rules()
            output = mock_stdout.getvalue()
            self.assertIn("Все правила удалены!", output)

        self.assertEqual(len(self.algo.rules), 0)

    def test_clear_all_rules_empty(self):
        """Тест очистки пустого списка правил"""
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            self.algo.clear_all_rules()
            output = mock_stdout.getvalue()
            self.assertIn("Все правила удалены!", output)

        self.assertEqual(len(self.algo.rules), 0)

    @patch('builtins.input', side_effect=["", "", "да"])
    def test_input_info_empty_strings(self, mock_input):
        """Тест ввода с пустыми строками"""
        self.algo.input_info()

        self.assertEqual(len(self.algo.rules), 1)
        self.assertEqual(self.algo.rules[0], ("", "", True))

    def test_main_algoritm_empty_string(self):
        """Тест основного алгоритма с пустой строкой"""
        self.algo.rules = [("a", "b", False)]
        result = self.algo.main_algoritm("")
        self.assertEqual(result, "")

    def test_main_algoritm_rule_with_empty_replacement(self):
        """Тест правила с пустой заменой"""
        self.algo.rules = [("test", "", False)]
        result = self.algo.main_algoritm("this is a test string")
        self.assertEqual(result, "this is a  string")


if __name__ == '__main__':
    unittest.main()
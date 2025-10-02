import unittest
from unittest.mock import patch
from io import StringIO
from algoritm_Markova import Algoritm_Markova


class TestAlgoritmMarkova(unittest.TestCase):

    def setUp(self):
        self.algo = Algoritm_Markova()

    def test_input_info_normal_case(self):
        with patch('builtins.input', side_effect=['яблоко', 'груша', 'да']):
            with patch('sys.stdout', new_callable=StringIO) as fake_out:
                self.algo.input_info()
                output = fake_out.getvalue().strip()

        self.assertEqual(len(self.algo.rules), 1)
        self.assertEqual(self.algo.rules[0], ('яблоко', 'груша', True))
        self.assertIn('Правило добавлено:яблоко->груша  (True)', output)

    def test_input_info_terminal_false(self):
        with patch('builtins.input', side_effect=['кошка', 'собака', 'нет']):
            self.algo.input_info()

        self.assertEqual(self.algo.rules[0], ('кошка', 'собака', False))

    def test_get_info_empty_rules(self):
        with patch('sys.stdout', new_callable=StringIO) as fake_out:
            self.algo.get_info()
            output = fake_out.getvalue().strip()

        self.assertEqual(output, '')

    def test_get_info_with_rules(self):
        self.algo.rules = [('яблоко', 'груша', True), ('кошка', 'собака', False)]

        with patch('sys.stdout', new_callable=StringIO) as fake_out:
            self.algo.get_info()
            output = fake_out.getvalue().strip()

        expected_output = '1. яблоко->груша  (True)\n2. кошка->собака  (False)'
        self.assertEqual(output, expected_output)

    def test_main_algoritm_no_rules(self):
        result = self.algo.main_algoritm('тестовая строка')
        self.assertEqual(result, 'тестовая строка')

    def test_main_algoritm_one_terminal_rule(self):
        self.algo.rules = [('яблоко', 'ГРУША', True)]
        result = self.algo.main_algoritm('яблоко и апельсин')
        self.assertEqual(result, 'ГРУША и апельсин')

    def test_main_algoritm_multiple_terminal_rules(self):
        self.algo.rules = [
            ('яблоко', 'ФРУКТ1', True),
            ('апельсин', 'ФРУКТ2', True)
        ]
        result = self.algo.main_algoritm('яблоко и апельсин')
        self.assertEqual(result, 'ФРУКТ1 и ФРУКТ2')

    def test_main_algoritm_non_terminal_rule(self):
        self.algo.rules = [('яблоко', 'груша', False)]
        result = self.algo.main_algoritm('яблоко и яблоко')
        self.assertEqual(result, 'яблоко и яблоко')

    def test_main_algoritm_mixed_rules(self):
        self.algo.rules = [
            ('яблоко', 'ГРУША', True),
            ('кошка', 'СОБАКА', False)
        ]
        result = self.algo.main_algoritm('яблоко и кошка')
        self.assertEqual(result, 'ГРУША и кошка')

    def test_delete_rule_empty_rules(self):
        with patch('sys.stdout', new_callable=StringIO) as fake_out:
            self.algo.delete_rule()
            output = fake_out.getvalue().strip()

        self.assertEqual(output, 'Правил нет!')

    def test_delete_rule_valid_index(self):
        self.algo.rules = [('яблоко', 'груша', True), ('кошка', 'собака', False)]

        with patch('builtins.input', return_value='1'):
            with patch('sys.stdout', new_callable=StringIO) as fake_out:
                self.algo.delete_rule()
                output = fake_out.getvalue().strip()

        self.assertEqual(len(self.algo.rules), 1)
        self.assertEqual(self.algo.rules[0], ('кошка', 'собака', False))
        self.assertIn('Правило удалено: яблоко -> груша', output)

    def test_delete_rule_invalid_index_too_high(self):
        self.algo.rules = [('яблоко', 'груша', True)]

        with patch('builtins.input', return_value='5'):
            with patch('sys.stdout', new_callable=StringIO) as fake_out:
                self.algo.delete_rule()
                output = fake_out.getvalue().strip()

        self.assertEqual(len(self.algo.rules), 1)
        self.assertIn('Неверный номер правила!', output)

    def test_delete_rule_invalid_index_zero(self):
        self.algo.rules = [('яблоко', 'груша', True)]

        with patch('builtins.input', return_value='0'):
            with patch('sys.stdout', new_callable=StringIO) as fake_out:
                self.algo.delete_rule()
                output = fake_out.getvalue().strip()

        self.assertEqual(len(self.algo.rules), 1)
        self.assertIn('Неверный номер правила!', output)

    def test_delete_rule_invalid_input_not_number(self):
        self.algo.rules = [('яблокo', 'груша', True)]

        with patch('builtins.input', return_value='не число'):
            with patch('sys.stdout', new_callable=StringIO) as fake_out:
                self.algo.delete_rule()
                output = fake_out.getvalue().strip()

        self.assertEqual(len(self.algo.rules), 1)
        self.assertIn('Ошибка ввода!', output)

    def test_clear_all_rules_empty(self):
        with patch('sys.stdout', new_callable=StringIO) as fake_out:
            self.algo.clear_all_rules()
            output = fake_out.getvalue().strip()

        self.assertEqual(self.algo.rules, [])
        self.assertEqual(output, 'Все правила удалены!')

    def test_clear_all_rules_with_data(self):
        self.algo.rules = [('яблоко', 'груша', True), ('кошка', 'собака', False)]

        with patch('sys.stdout', new_callable=StringIO) as fake_out:
            self.algo.clear_all_rules()
            output = fake_out.getvalue().strip()

        self.assertEqual(self.algo.rules, [])
        self.assertEqual(output, 'Все правила удалены!')


if __name__ == '__main__':
    unittest.main()
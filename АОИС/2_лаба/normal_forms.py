"""
Модуль построения СДНФ и СКНФ.
"""

from typing import List, Dict, Tuple, Set
from truth_table import TruthTable


class NormalForm:
    """Класс для работы с нормальными формами (СДНФ, СКНФ)."""
    
    def __init__(self, truth_table: TruthTable):
        """
        Инициализация нормальной формы.
        
        Args:
            truth_table: Таблица истинности функции
        """
        self.truth_table = truth_table
        self.variables = truth_table.variables
        self.num_vars = len(self.variables)
    
    def _literal_to_string(self, var: str, value: bool) -> str:
        """
        Преобразование литерала в строку.
        
        Args:
            var: Имя переменной
            value: Значение (True - прямая, False - инвертированная)
            
        Returns:
            Строковое представление литерала
        """
        if value:
            return var
        else:
            return f"!{var}"
    
    def _minterm_to_string(self, row: Dict) -> str:
        """
        Создание минтерма для строки таблицы истинности.
        
        Args:
            row: Строка таблицы истинности
            
        Returns:
            Строка минтерма
        """
        literals = []
        for var in self.variables:
            value = row['inputs'][var]
            literals.append(self._literal_to_string(var, value))
        return "".join(f"({lit})" for lit in literals)
    
    def _maxterm_to_string(self, row: Dict) -> str:
        """
        Создание максстерма для строки таблицы истинности.
        
        Args:
            row: Строка таблицы истинности
            
        Returns:
            Строка максстерма
        """
        literals = []
        for var in self.variables:
            value = row['inputs'][var]
            literals.append(self._literal_to_string(var, not value))
        return "".join(f"({lit})" for lit in literals)
    
    def build_sdnf(self) -> str:
        """
        Построение СДНФ (Совершенная Дизъюнктивная Нормальная Форма).
        
        Returns:
            Строка СДНФ
        """
        true_rows = self.truth_table.get_true_rows()
        
        if not true_rows:
            return "0"
        
        minterms = [self._minterm_to_string(row) for row in true_rows]
        return " v ".join(minterms)
    
    def build_sknf(self) -> str:
        """
        Построение СКНФ (Совершенная Конъюнктивная Нормальная Форма).
        
        Returns:
            Строка СКНФ
        """
        false_rows = self.truth_table.get_false_rows()
        
        if not false_rows:
            return "1"
        
        maxterms = [self._maxterm_to_string(row) for row in false_rows]
        return " & ".join(maxterms)
    
    def get_sdnf_numeric(self) -> List[int]:
        """
        Получение числовой формы СДНФ (индексы наборов где F=1).
        
        Returns:
            Список индексов
        """
        return self.truth_table.get_true_indices()
    
    def get_sknf_numeric(self) -> List[int]:
        """
        Получение числовой формы СКНФ (индексы наборов где F=0).
        
        Returns:
            Список индексов
        """
        return self.truth_table.get_false_indices()
    
    def get_sdnf_index_form(self) -> str:
        """
        Получение индексной формы СДНФ.
        
        Returns:
            Строка индексной формы
        """
        indices = self.get_sdnf_numeric()
        if not indices:
            return "empty"
        return f"sum({', '.join(map(str, indices))})"
    
    def get_sknf_index_form(self) -> str:
        """
        Получение индексной формы СКНФ.
        
        Returns:
            Строка индексной формы
        """
        indices = self.get_sknf_numeric()
        if not indices:
            return "empty"
        return f"prod({', '.join(map(str, indices))})"
    
    def get_function_index_form(self) -> str:
        """
        Получение полной индексной формы функции.
        
        Returns:
            Строка индексной формы
        """
        sdnf_indices = self.get_sdnf_numeric()
        sknf_indices = self.get_sknf_numeric()
        return f"F = sum({', '.join(map(str, sdnf_indices))}) = prod({', '.join(map(str, sknf_indices))})"

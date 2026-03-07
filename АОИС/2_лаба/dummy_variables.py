"""
Модуль поиска фиктивных переменных.
Фиктивная переменная - переменная, значение которой не влияет на результат функции.
"""

from typing import List, Set, Dict
from truth_table import TruthTable


class DummyVariables:
    """Класс для поиска фиктивных переменных."""
    
    def __init__(self, truth_table: TruthTable):
        """
        Инициализация поиска фиктивных переменных.
        
        Args:
            truth_table: Таблица истинности функции
        """
        self.truth_table = truth_table
        self.variables = truth_table.variables
        self.num_vars = len(self.variables)
        self.values = truth_table.get_function_values()
    
    def is_dummy(self, var: str) -> bool:
        """
        Проверка, является ли переменная фиктивной.
        
        Переменная фиктивна, если функция не меняет значение
        при изменении этой переменной.
        
        Args:
            var: Имя переменной
            
        Returns:
            True если переменная фиктивная
        """
        var_index = self.variables.index(var)
        
        # Проверяем все пары наборов, отличающихся только этой переменной
        for i, row in enumerate(self.truth_table.rows):
            # Создаём индекс набора с инвертированной переменной var
            modified_inputs = row['inputs'].copy()
            modified_inputs[var] = not modified_inputs[var]
            
            # Находим индекс этого набора в таблице
            modified_index = self._find_row_index(modified_inputs)
            
            # Если значения функции различаются - переменная существенна
            if self.values[i] != self.values[modified_index]:
                return False
        
        return True
    
    def _find_row_index(self, inputs: Dict[str, bool]) -> int:
        """
        Поиск индекса строки по значениям переменных.
        
        Args:
            inputs: Словарь значений переменных
            
        Returns:
            Индекс строки
        """
        for i, row in enumerate(self.truth_table.rows):
            if row['inputs'] == inputs:
                return i
        raise ValueError("Строка не найдена")
    
    def get_dummy_variables(self) -> List[str]:
        """
        Получение списка всех фиктивных переменных.
        
        Returns:
            Список фиктивных переменных
        """
        return [var for var in self.variables if self.is_dummy(var)]
    
    def get_essential_variables(self) -> List[str]:
        """
        Получение списка всех существенных переменных.
        
        Returns:
            Список существенных переменных
        """
        return [var for var in self.variables if not self.is_dummy(var)]
    
    def display(self) -> str:
        """
        Форматированное отображение информации о фиктивных переменных.
        
        Returns:
            Строка с информацией
        """
        dummy = self.get_dummy_variables()
        essential = self.get_essential_variables()
        
        lines = ["Информация о переменных:"]
        
        if dummy:
            lines.append(f"  Фиктивные переменные: {', '.join(dummy)}")
        else:
            lines.append("  Фиктивные переменные: отсутствуют")
        
        if essential:
            lines.append(f"  Существенные переменные: {', '.join(essential)}")
        else:
            lines.append("  Существенные переменные: отсутствуют")
        
        return "\n".join(lines)

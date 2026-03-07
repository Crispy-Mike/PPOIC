"""
Модуль построения таблицы истинности и работы с ней.
"""

from typing import List, Dict, Tuple, Set
from itertools import product
from parser import ASTNode, parse_expression, get_all_variables


class TruthTable:
    """Класс для представления таблицы истинности."""
    
    def __init__(self, expression: str):
        """
        Инициализация таблицы истинности.
        
        Args:
            expression: Логическое выражение в строковом формате
        """
        self.expression = expression
        self.ast = parse_expression(expression)
        self.variables = sorted(self.ast.get_variables())
        self.num_vars = len(self.variables)
        self.rows: List[Dict] = []
        self._build_table()
    
    def _build_table(self) -> None:
        """Построение таблицы истинности."""
        self.rows = []
        
        for values in product([False, True], repeat=self.num_vars):
            row_values = dict(zip(self.variables, values))
            result = self.ast.evaluate(row_values)
            
            row = {
                'inputs': dict(zip(self.variables, values)),
                'result': result,
                'tuple': values,
                'index': self._tuple_to_index(values)
            }
            self.rows.append(row)
    
    def _tuple_to_index(self, values: Tuple[bool, ...]) -> int:
        """Преобразование кортежа значений в индекс (число)."""
        index = 0
        for i, val in enumerate(values):
            if val:
                index += (1 << (self.num_vars - 1 - i))
        return index
    
    def get_true_rows(self) -> List[Dict]:
        """Получение строк, где функция равна 1."""
        return [row for row in self.rows if row['result']]
    
    def get_false_rows(self) -> List[Dict]:
        """Получение строк, где функция равна 0."""
        return [row for row in self.rows if not row['result']]
    
    def get_function_values(self) -> List[int]:
        """Получение всех значений функции в виде списка 0/1."""
        return [1 if row['result'] else 0 for row in self.rows]
    
    def get_true_indices(self) -> List[int]:
        """Получение индексов наборов, где функция равна 1."""
        return [row['index'] for row in self.get_true_rows()]
    
    def get_false_indices(self) -> List[int]:
        """Получение индексов наборов, где функция равна 0."""
        return [row['index'] for row in self.get_false_rows()]
    
    def display(self) -> str:
        """Форматированное отображение таблицы истинности."""
        header = " | ".join(self.variables) + " | F"
        separator = "-" * len(header)
        
        lines = [header, separator]
        for row in self.rows:
            values_str = " | ".join("1" if row['inputs'][var] else "0" 
                                   for var in self.variables)
            result_str = "1" if row['result'] else "0"
            lines.append(f"{values_str} | {result_str}")
        
        return "\n".join(lines)
    
    def __len__(self) -> int:
        return len(self.rows)
    
    def __iter__(self):
        return iter(self.rows)

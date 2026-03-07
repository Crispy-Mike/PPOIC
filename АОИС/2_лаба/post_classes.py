"""
Модуль определения принадлежности функции к классам Поста.
Классы Поста:
- T0: Сохраняющие ноль (f(0,0,...,0) = 0)
- T1: Сохраняющие единицу (f(1,1,...,1) = 1)
- S: Самодвойственные (f(x) = ¬f(¬x))
- M: Монотонные (x ≤ y => f(x) ≤ f(y))
- L: Линейные (представимы полиномом Жегалкина без конъюнкций)
"""

from typing import Dict, List, Set, Tuple
from truth_table import TruthTable


class PostClasses:
    """Класс для определения принадлежности к классам Поста."""
    
    def __init__(self, truth_table: TruthTable):
        """
        Инициализация проверки классов Поста.
        
        Args:
            truth_table: Таблица истинности функции
        """
        self.truth_table = truth_table
        self.variables = truth_table.variables
        self.num_vars = len(self.variables)
        self.values = truth_table.get_function_values()
    
    def belongs_to_t0(self) -> bool:
        """
        Проверка принадлежности к классу T0 (сохраняющие ноль).
        Функция сохраняет ноль, если f(0,0,...,0) = 0.
        
        Returns:
            True если функция принадлежит T0
        """
        return self.values[0] == 0
    
    def belongs_to_t1(self) -> bool:
        """
        Проверка принадлежности к классу T1 (сохраняющие единицу).
        Функция сохраняет единицу, если f(1,1,...,1) = 1.
        
        Returns:
            True если функция принадлежит T1
        """
        return self.values[-1] == 1
    
    def belongs_to_s(self) -> bool:
        """
        Проверка принадлежности к классу S (самодвойственные).
        Функция самодвойственна, если f(x) = ¬f(¬x) для всех x.
        
        Returns:
            True если функция принадлежит S
        """
        num_rows = len(self.values)
        
        for i in range(num_rows):
            # Индекс инверсного набора
            inverted_index = num_rows - 1 - i
            
            # Проверка условия самодвойственности
            if self.values[i] == self.values[inverted_index]:
                return False
        
        return True
    
    def belongs_to_m(self) -> bool:
        """
        Проверка принадлежности к классу M (монотонные).
        Функция монотонна, если x ≤ y => f(x) ≤ f(y).
        
        Returns:
            True если функция принадлежит M
        """
        num_rows = len(self.values)
        
        for i in range(num_rows):
            for j in range(i + 1, num_rows):
                # Проверка: набор i <= набору j
                if self._is_less_or_equal(i, j):
                    if self.values[i] > self.values[j]:
                        return False
        
        return True
    
    def _is_less_or_equal(self, idx1: int, idx2: int) -> bool:
        """
        Проверка: набор с индексом idx1 <= набору с индексом idx2.
        
        Args:
            idx1: Индекс первого набора
            idx2: Индекс второго набора
            
        Returns:
            True если idx1 <= idx2 покомпонентно
        """
        row1 = self.truth_table.rows[idx1]
        row2 = self.truth_table.rows[idx2]
        
        for var in self.variables:
            if row1['inputs'][var] and not row2['inputs'][var]:
                return False
        
        return True
    
    def belongs_to_l(self) -> bool:
        """
        Проверка принадлежности к классу L (линейные).
        Функция линейна, если её полином Жегалкина не содержит конъюнкций.
        Проверяем через коэффициенты полинома Жегалкина.
        
        Returns:
            True если функция принадлежит L
        """
        # Вычисляем коэффициенты полинома Жегалкина
        coefficients = self._compute_zhegalkin_coefficients()
        
        # Проверяем, есть ли коэффициенты при конъюнкциях (степень > 1)
        for mask in range(1, 1 << self.num_vars):
            # Количество единиц в маске - это степень монома
            degree = bin(mask).count('1')
            if degree > 1 and coefficients[mask]:
                return False
        
        return True
    
    def _compute_zhegalkin_coefficients(self) -> List[int]:
        """
        Вычисление коэффициентов полинома Жегалкина.
        
        Returns:
            Список коэффициентов
        """
        coeffs = self.values.copy()
        
        for i in range(self.num_vars):
            for mask in range(1 << self.num_vars):
                if mask & (1 << i):
                    coeffs[mask] ^= coeffs[mask ^ (1 << i)]
        
        return coeffs
    
    def get_all_classes(self) -> Dict[str, bool]:
        """
        Получение информации о принадлежности ко всем классам.
        
        Returns:
            Словарь с результатами проверок
        """
        return {
            'T0': self.belongs_to_t0(),
            'T1': self.belongs_to_t1(),
            'S': self.belongs_to_s(),
            'M': self.belongs_to_m(),
            'L': self.belongs_to_l()
        }
    
    def is_complete(self) -> bool:
        """
        Проверка полноты системы функций.
        Система полна, если она не содержится ни в одном из классов Поста.
        
        Returns:
            True если функция образует полную систему
        """
        classes = self.get_all_classes()
        return not any(classes.values())
    
    def display(self) -> str:
        """
        Форматированное отображение принадлежности к классам.
        
        Returns:
            Строка с информацией о классах
        """
        classes = self.get_all_classes()
        
        lines = ["Принадлежность к классам Поста:"]
        
        class_descriptions = {
            'T0': 'Сохраняющие ноль',
            'T1': 'Сохраняющие единицу',
            'S': 'Самодвойственные',
            'M': 'Монотонные',
            'L': 'Линейные'
        }
        
        for class_name, belongs in classes.items():
            status = "Принадлежит" if belongs else "Не принадлежит"
            desc = class_descriptions[class_name]
            lines.append(f"  {class_name} ({desc}): {status}")
        
        completeness = "Полная" if self.is_complete() else "Неполная"
        lines.append(f"\nСистема: {completeness}")
        
        return "\n".join(lines)

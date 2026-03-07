"""
Модуль построения полинома Жегалкина.
Полином Жегалкина - представление булевой функции в виде суммы по модулю 2
конъюнкций переменных.
"""

from typing import List, Dict, Tuple
from truth_table import TruthTable


class ZhegalkinPolynomial:
    """Класс для работы с полиномом Жегалкина."""
    
    def __init__(self, truth_table: TruthTable):
        """
        Инициализация полинома Жегалкина.
        
        Args:
            truth_table: Таблица истинности функции
        """
        self.truth_table = truth_table
        self.variables = truth_table.variables
        self.num_vars = len(self.variables)
        self.values = truth_table.get_function_values()
        self.coefficients: List[int] = []
        self._compute_coefficients()
    
    def _compute_coefficients(self) -> None:
        """
        Вычисление коэффициентов полинома Жегалкина методом треугольника.
        """
        self.coefficients = self.values.copy()
        
        for i in range(self.num_vars):
            for mask in range(1 << self.num_vars):
                if mask & (1 << i):
                    self.coefficients[mask] ^= self.coefficients[mask ^ (1 << i)]
    
    def _mask_to_monomial(self, mask: int) -> str:
        """
        Преобразование маски в моном полинома.
        
        Args:
            mask: Битовая маска переменных
            
        Returns:
            Строковое представление монома
        """
        if mask == 0:
            return "1"
        
        terms = []
        for i, var in enumerate(self.variables):
            if mask & (1 << (self.num_vars - 1 - i)):
                terms.append(var)
        
        return "".join(terms)
    
    def get_polynomial(self) -> str:
        """
        Получение строкового представления полинома Жегалкина.
        
        Returns:
            Строка полинома
        """
        terms = []
        
        for mask in range(1 << self.num_vars):
            if self.coefficients[mask]:
                monomial = self._mask_to_monomial(mask)
                terms.append(monomial)
        
        if not terms:
            return "0"
        
        return " ^ ".join(terms)
    
    def get_coefficients(self) -> List[int]:
        """
        Получение списка коэффициентов.
        
        Returns:
            Список коэффициентов (0 или 1)
        """
        return self.coefficients.copy()
    
    def get_terms(self) -> List[Tuple[int, str]]:
        """
        Получение списка членов полинома.
        
        Returns:
            Список кортежей (маска, моном)
        """
        terms = []
        for mask in range(1 << self.num_vars):
            if self.coefficients[mask]:
                terms.append((mask, self._mask_to_monomial(mask)))
        return terms
    
    def display_table(self) -> str:
        """
        Табличное представление коэффициентов полинома.
        
        Returns:
            Форматированная таблица
        """
        lines = ["Коэффициенты полинома Жегалкина:"]
        lines.append("-" * 40)
        
        for mask in range(1 << self.num_vars):
            monomial = self._mask_to_monomial(mask)
            coeff = self.coefficients[mask]
            lines.append(f"  {monomial:>10}: {coeff}")
        
        return "\n".join(lines)

"""
Модуль минимизации булевых функций.
Методы:
- Расчетный метод (склеивание и поглощение)
- Расчетно-табличный метод
- Табличный метод (карта Карно)
"""

from typing import List, Dict, Tuple, Set, Optional
from itertools import combinations
from truth_table import TruthTable


class Implicant:
    """Класс для представления импликанты."""
    
    def __init__(self, variables: List[str], values: List[Optional[bool]], minterms: List[int]):
        """
        Инициализация импликанты.
        
        Args:
            variables: Список переменных
            values: Список значений (True, False, None для "не важно")
            minterms: Список индексов минтермов
        """
        self.variables = variables
        self.values = values
        self.minterms = set(minterms)
        self.used = False
    
    def __repr__(self) -> str:
        return f"Implicant({self.to_string()}, {sorted(self.minterms)})"
    
    def to_string(self) -> str:
        """Строковое представление импликанты."""
        terms = []
        for var, val in zip(self.variables, self.values):
            if val is None:
                continue
            elif val:
                terms.append(var)
            else:
                terms.append(f"!{var}")

        if not terms:
            return "1"
        return "".join(terms)
    
    def to_pattern(self) -> str:
        """Представление в виде паттерна (0, 1, X)."""
        pattern = []
        for val in self.values:
            if val is None:
                pattern.append("X")
            elif val:
                pattern.append("1")
            else:
                pattern.append("0")
        return "".join(pattern)
    
    def covers(self, minterm: int) -> bool:
        """Проверка, покрывает ли импликанта данный минтерм."""
        return minterm in self.minterms
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Implicant):
            return False
        return self.variables == other.variables and self.values == other.values
    
    def __hash__(self) -> int:
        return hash(tuple(self.values))


class Minimization:
    """Класс для минимизации булевых функций."""
    
    def __init__(self, truth_table: TruthTable):
        """
        Инициализация минимизации.
        
        Args:
            truth_table: Таблица истинности функции
        """
        self.truth_table = truth_table
        self.variables = truth_table.variables
        self.num_vars = len(self.variables)
        self.true_indices = truth_table.get_true_indices()
    
    def _create_minterm_implicant(self, index: int) -> Implicant:
        """Создание импликанты из минтерма."""
        values = []
        for i in range(self.num_vars - 1, -1, -1):
            values.append(bool(index & (1 << i)))
        return Implicant(self.variables, values, [index])
    
    def _can_combine(self, imp1: Implicant, imp2: Implicant) -> bool:
        """Проверка возможности склеивания двух импликант."""
        diff_count = 0
        for v1, v2 in zip(imp1.values, imp2.values):
            if v1 != v2:
                if v1 is not None and v2 is not None:
                    diff_count += 1
                else:
                    return False
        
        return diff_count == 1
    
    def _combine_implicants(self, imp1: Implicant, imp2: Implicant) -> Implicant:
        """Склеивание двух импликант."""
        new_values = []
        for v1, v2 in zip(imp1.values, imp2.values):
            if v1 != v2:
                new_values.append(None)
            else:
                new_values.append(v1)
        
        new_minterms = list(imp1.minterms | imp2.minterms)
        return Implicant(self.variables, new_values, new_minterms)
    
    def minimize_calculated(self) -> Tuple[List[Implicant], List[str]]:
        """
        Минимизация расчетным методом.
        
        Returns:
            Кортеж (список простых импликант, история этапов)
        """
        history = []
        
        # Создаем начальные импликанты (минтермы)
        current_implicants = [
            self._create_minterm_implicant(idx) for idx in self.true_indices
        ]
        
        history.append(f"Исходные минтермы: {[imp.to_string() for imp in current_implicants]}")
        
        # Этап склеивания
        stage = 1
        while True:
            new_implicants = []
            used = set()
            
            for i, imp1 in enumerate(current_implicants):
                for j, imp2 in enumerate(current_implicants):
                    if i >= j:
                        continue
                    
                    if self._can_combine(imp1, imp2):
                        combined = self._combine_implicants(imp1, imp2)
                        if combined not in new_implicants:
                            new_implicants.append(combined)
                        used.add(i)
                        used.add(j)
            
            if not new_implicants:
                break
            
            history.append(f"\nЭтап склеивания {stage}:")
            for imp in new_implicants:
                history.append(f"  {imp.to_string()} ({imp.to_pattern()})")
            
            current_implicants = new_implicants
            stage += 1
        
        # Убираем дубликаты
        unique_implicants = []
        seen = set()
        for imp in current_implicants:
            key = tuple(imp.values)
            if key not in seen:
                seen.add(key)
                unique_implicants.append(imp)
        
        # Этап поглощения (удаление лишних импликант)
        history.append("\nПроверка на лишние импликанты:")
        final_implicants = self._remove_redundant(unique_implicants, history)
        
        return final_implicants, history
    
    def _remove_redundant(self, implicants: List[Implicant], history: List[str]) -> List[Implicant]:
        """Удаление лишних импликант."""
        result = implicants.copy()
        
        for imp in implicants:
            # Проверяем, покрывается ли импликанта остальными
            others = [i for i in result if i != imp]
            
            # Проверяем все минтермы этой импликанты
            all_covered = True
            for minterm in imp.minterms:
                covered_by_others = any(i.covers(minterm) for i in others)
                if not covered_by_others:
                    all_covered = False
                    break
            
            if all_covered and len(others) > 0:
                history.append(f"  {imp.to_string()} - лишняя импликанта")
                result.remove(imp)
            else:
                history.append(f"  {imp.to_string()} - необходимая импликанта")
        
        return result
    
    def minimize_calculated_table(self) -> Tuple[List[Implicant], str, List[str]]:
        """
        Минимизация расчетно-табличным методом.
        
        Returns:
            Кортеж (импликанты, таблица покрытия, история)
        """
        history = []
        
        # Получаем простые импликанты через склеивание
        implicants, calc_history = self.minimize_calculated()
        history.extend(calc_history)
        
        # Строим таблицу покрытия
        table_lines = ["\nТаблица покрытия:"]
        
        # Заголовок
        header = "Импликанта | " + " ".join(f"{m:>3}" for m in self.true_indices)
        table_lines.append(header)
        table_lines.append("-" * len(header))
        
        # Строки таблицы
        for imp in implicants:
            row = f"{imp.to_string():>10} |"
            for m in self.true_indices:
                if imp.covers(m):
                    row += "  X "
                else:
                    row += "    "
            table_lines.append(row)
        
        table_str = "\n".join(table_lines)
        
        return implicants, table_str, history
    
    def minimize_karnaugh(self) -> Tuple[List[Implicant], str]:
        """
        Минимизация с помощью карты Карно.
        
        Returns:
            Кортеж (импликанты, представление карты)
        """
        if self.num_vars < 2 or self.num_vars > 4:
            raise ValueError("Карта Карно поддерживается для 2-4 переменных")
        
        # Для простоты реализуем для 2-4 переменных
        if self.num_vars == 2:
            return self._karnaugh_2var()
        elif self.num_vars == 3:
            return self._karnaugh_3var()
        else:
            return self._karnaugh_4var()
    
    def _karnaugh_2var(self) -> Tuple[List[Implicant], str]:
        """Карта Карно для 2 переменных."""
        var_a, var_b = self.variables
        
        # Создаем карту
        kmap = [[0, 0], [0, 0]]
        for idx in self.true_indices:
            a = (idx >> 1) & 1
            b = idx & 1
            kmap[a][b] = 1
        
        lines = ["\nКарта Карно:"]
        lines.append(f"      {var_b}=0  {var_b}=1")
        lines.append(f"  +-----------+")
        lines.append(f"{var_a}=0 |  {kmap[0][0]}    {kmap[0][1]}")
        lines.append(f"{var_a}=1 |  {kmap[1][0]}    {kmap[1][1]}")
        
        # Находим группы
        implicants = self._find_kmap_groups(kmap, 2)
        
        return implicants, "\n".join(lines)
    
    def _karnaugh_3var(self) -> Tuple[List[Implicant], str]:
        """Карта Карно для 3 переменных."""
        var_a, var_b, var_c = self.variables
        
        # Создаем карту (a по строкам, bc по столбцам в порядке Грея)
        kmap = [[0, 0, 0, 0], [0, 0, 0, 0]]
        gray_order = [0, 1, 3, 2]  # Порядок Грея для 2 бит
        
        for idx in self.true_indices:
            a = (idx >> 2) & 1
            bc = idx & 3
            col = gray_order.index(bc) if bc in gray_order else 0
            kmap[a][col] = 1
        
        lines = ["\nКарта Карно:"]
        lines.append(f"       {var_b}{var_c}=00  01  11  10")
        lines.append(f"   +--------------------+")
        lines.append(f"{var_a}=0 |  {kmap[0][0]}    {kmap[0][1]}   {kmap[0][2]}   {kmap[0][3]}")
        lines.append(f"{var_a}=1 |  {kmap[1][0]}    {kmap[1][1]}   {kmap[1][2]}   {kmap[1][3]}")
        
        # Находим группы
        implicants = self._find_kmap_groups_3var(kmap)
        
        return implicants, "\n".join(lines)
    
    def _karnaugh_4var(self) -> Tuple[List[Implicant], str]:
        """Карта Карно для 4 переменных."""
        var_a, var_b, var_c, var_d = self.variables
        
        # Создаем карту 4x4
        kmap = [[0] * 4 for _ in range(4)]
        gray_order = [0, 1, 3, 2]
        
        for idx in self.true_indices:
            ab = (idx >> 2) & 3
            cd = idx & 3
            row = gray_order.index(ab) if ab in gray_order else 0
            col = gray_order.index(cd) if cd in gray_order else 0
            kmap[row][col] = 1
        
        lines = ["\nКарта Карно:"]
        lines.append(f"         {var_c}{var_d}=00  01  11  10")
        lines.append(f"     +--------------------------+")
        lines.append(f"{var_a}{var_b}=00 |  {kmap[0][0]}    {kmap[0][1]}   {kmap[0][2]}   {kmap[0][3]}")
        lines.append(f"{var_a}{var_b}=01 |  {kmap[1][0]}    {kmap[1][1]}   {kmap[1][2]}   {kmap[1][3]}")
        lines.append(f"{var_a}{var_b}=11 |  {kmap[2][0]}    {kmap[2][1]}   {kmap[2][2]}   {kmap[2][3]}")
        lines.append(f"{var_a}{var_b}=10 |  {kmap[3][0]}    {kmap[3][1]}   {kmap[3][2]}   {kmap[3][3]}")
        
        # Находим группы
        implicants = self._find_kmap_groups_4var(kmap)
        
        return implicants, "\n".join(lines)
    
    def _find_kmap_groups(self, kmap: List[List[int]], num_vars: int) -> List[Implicant]:
        """Поиск групп на карте Карно."""
        implicants = []
        covered = set()
        
        # Приоритет: большие группы сначала
        sizes = [4, 2, 1] if num_vars == 2 else [8, 4, 2, 1]
        
        for size in sizes:
            for i in range(len(kmap)):
                for j in range(len(kmap[0])):
                    if kmap[i][j] == 1 and (i, j) not in covered:
                        # Пытаемся найти группу размера size
                        group = self._find_group(kmap, i, j, size, covered)
                        if group:
                            implicants.append(self._group_to_implicant(group, num_vars))
                            covered.update(group)
        
        return implicants
    
    def _find_group(
        self, 
        kmap: List[List[int]], 
        row: int, 
        col: int, 
        size: int,
        covered: Set[Tuple[int, int]]
    ) -> Optional[Set[Tuple[int, int]]]:
        """Поиск группы заданного размера."""
        if kmap[row][col] == 0:
            return None
        
        # Простая реализация для размера 1
        if size == 1:
            return {(row, col)}
        
        # Проверка горизонтальной группы
        if size == 2 and col + 1 < len(kmap[0]):
            if kmap[row][col + 1] == 1:
                return {(row, col), (row, col + 1)}
        
        # Проверка вертикальной группы
        if size == 2 and row + 1 < len(kmap):
            if kmap[row + 1][col] == 1:
                return {(row, col), (row + 1, col)}
        
        return {(row, col)}
    
    def _find_kmap_groups_3var(self, kmap: List[List[int]]) -> List[Implicant]:
        """Поиск групп на карте Карно для 3 переменных."""
        implicants = []
        covered = set()
        
        gray_order = [0, 1, 3, 2]
        
        # Проверяем все возможные группы
        # Группа из 4 клеток (вся строка или 2x2)
        for row in range(2):
            if all(kmap[row][c] == 1 for c in range(4)):
                group = {(row, c) for c in range(4)}
                if not group <= covered:
                    implicants.append(self._group_to_implicant_3var(group, gray_order))
                    covered.update(group)
        
        # Группа из 2 клеток
        for row in range(2):
            for col in range(4):
                if (row, col) in covered or kmap[row][col] == 0:
                    continue
                
                # Горизонтальная пара (с учетом цикличности)
                next_col = (col + 1) % 4
                if kmap[row][next_col] == 1 and (row, next_col) not in covered:
                    group = {(row, col), (row, next_col)}
                    implicants.append(self._group_to_implicant_3var(group, gray_order))
                    covered.update(group)
                    continue
                
                # Вертикальная пара
                if kmap[1 - row][col] == 1:
                    group = {(row, col), (1 - row, col)}
                    implicants.append(self._group_to_implicant_3var(group, gray_order))
                    covered.update(group)
                    continue
                
                # Одиночная клетка
                group = {(row, col)}
                implicants.append(self._group_to_implicant_3var(group, gray_order))
                covered.add((row, col))
        
        return implicants
    
    def _find_kmap_groups_4var(self, kmap: List[List[int]]) -> List[Implicant]:
        """Поиск групп на карте Карно для 4 переменных."""
        implicants = []
        covered = set()
        
        gray_order = [0, 1, 3, 2]
        
        # Проверяем группы по размеру (от больших к меньшим)
        for size in [16, 8, 4, 2, 1]:
            for row in range(4):
                for col in range(4):
                    if (row, col) in covered or kmap[row][col] == 0:
                        continue
                    
                    group = self._find_max_group_4var(kmap, row, col, size)
                    if group and len(group) >= size:
                        implicants.append(self._group_to_implicant_4var(group, gray_order))
                        covered.update(group)
        
        return implicants
    
    def _find_max_group_4var(
        self, 
        kmap: List[List[int]], 
        row: int, 
        col: int, 
        target_size: int
    ) -> Optional[Set[Tuple[int, int]]]:
        """Поиск максимальной группы на карте 4 переменных."""
        if kmap[row][col] == 0:
            return None
        
        # Упрощенная реализация
        return {(row, col)}
    
    def _group_to_implicant(self, group: Set[Tuple[int, int]], num_vars: int) -> Implicant:
        """Преобразование группы в импликанту."""
        values = [None] * num_vars
        
        rows = [r for r, c in group]
        cols = [c for r, c in group]
        
        if num_vars >= 1:
            if len(set(rows)) == 1:
                values[0] = bool(rows[0])
        
        if num_vars >= 2:
            if len(set(cols)) == 1:
                values[1] = bool(cols[0])
        
        minterms = []
        for r, c in group:
            idx = (r << 1) | c
            minterms.append(idx)
        
        return Implicant(self.variables, values, minterms)
    
    def _group_to_implicant_3var(
        self, 
        group: Set[Tuple[int, int]], 
        gray_order: List[int]
    ) -> Implicant:
        """Преобразование группы в импликанту для 3 переменных."""
        values = [None, None, None]
        
        rows = list(set(r for r, c in group))
        cols = list(set(c for c in group))
        
        # Переменная a
        if len(rows) == 1:
            values[0] = bool(rows[0])
        
        # Переменные b и c
        if len(cols) == 1:
            col_val = cols[0] if isinstance(cols[0], int) else cols[0][0]
            bc_val = gray_order[col_val]
            values[1] = bool(bc_val & 2)
            values[2] = bool(bc_val & 1)
        elif len(cols) == 2:
            # Проверяем, какая переменная постоянна
            col_vals = [c if isinstance(c, int) else c[0] for c in cols]
            bc_vals = [gray_order[c] for c in col_vals]
            if all(v & 2 == bc_vals[0] & 2 for v in bc_vals):
                values[1] = bool(bc_vals[0] & 2)
            if all(v & 1 == bc_vals[0] & 1 for v in bc_vals):
                values[2] = bool(bc_vals[0] & 1)

        minterms = []
        for r, c in group:
            col_val = c if isinstance(c, int) else c[0]
            bc_val = gray_order[col_val]
            idx = (r << 2) | bc_val
            minterms.append(idx)
        
        return Implicant(self.variables, values, minterms)
    
    def _group_to_implicant_4var(
        self, 
        group: Set[Tuple[int, int]],
        gray_order: List[int]
    ) -> Implicant:
        """Преобразование группы в импликанту для 4 переменных."""
        values = [None, None, None, None]

        rows = list(set(r for r, c in group))
        cols = list(set(c for c in group))

        # Переменные a и b
        if len(rows) == 1:
            row_val = rows[0] if isinstance(rows[0], int) else rows[0][0]
            ab_val = gray_order[row_val]
            values[0] = bool(ab_val & 2)
            values[1] = bool(ab_val & 1)

        # Переменные c и d
        if len(cols) == 1:
            col_val = cols[0] if isinstance(cols[0], int) else cols[0][0]
            cd_val = gray_order[col_val]
            values[2] = bool(cd_val & 2)
            values[3] = bool(cd_val & 1)

        minterms = []
        for r, c in group:
            row_val = r if isinstance(r, int) else r[0]
            col_val = c if isinstance(c, int) else c[0]
            ab_val = gray_order[row_val]
            cd_val = gray_order[col_val]
            idx = (ab_val << 2) | cd_val
            minterms.append(idx)

        return Implicant(self.variables, values, minterms)
    
    def get_minimized_dnf(self, implicants: List[Implicant]) -> str:
        """
        Получение минимизированной ДНФ.
        
        Args:
            implicants: Список импликант
            
        Returns:
            Строка минимизированной ДНФ
        """
        if not implicants:
            return "0"
        
        terms = [imp.to_string() for imp in implicants]
        return " v ".join(terms)

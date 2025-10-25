class Student:
    """Пользовательский класс для демонстрации сортировки"""

    def __init__(self, name: str, age: int, grade: float):
        self.name = name
        self.age = age
        self.grade = grade

    def __lt__(self, other: 'Student') -> bool:
        # Сравнение по возрасту
        return self.age < other.age

    def __gt__(self, other: 'Student') -> bool:
        # Сравнение по возрасту
        return self.age > other.age

    def __eq__(self, other: 'Student') -> bool:
        if not isinstance(other, Student):
            return False
        return self.age == other.age and self.name == other.name and self.grade == other.grade

    def __str__(self) -> str:
        return f"Student(name='{self.name}', age={self.age}, grade={self.grade})"

    def __repr__(self) -> str:
        return self.__str__()

    @staticmethod
    def compare_by_grade(student1: 'Student', student2: 'Student') -> bool:
        """Альтернативный компаратор для сортировки по оценке"""
        return student1.grade < student2.grade

    @staticmethod
    def compare_by_name(student1: 'Student', student2: 'Student') -> bool:
        """Альтернативный компаратор для сортировки по имени"""
        return student1.name < student2.name
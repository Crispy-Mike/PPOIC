import unittest
from Student import Student


class TestStudent(unittest.TestCase):

    def test_init(self):
        """Тест инициализации студента"""
        student = Student("Иван", 85)
        self.assertEqual(student.name, "Иван")
        self.assertEqual(student.score, 85)

    def test_lt(self):
        """Тест оператора меньше"""
        student1 = Student("Анна", 75)
        student2 = Student("Петр", 85)
        self.assertTrue(student1 < student2)
        self.assertFalse(student2 < student1)

    def test_le(self):
        """Тест оператора меньше или равно"""
        student1 = Student("Анна", 75)
        student2 = Student("Петр", 85)
        student3 = Student("Мария", 75)

        self.assertTrue(student1 <= student2)
        self.assertTrue(student1 <= student3)
        self.assertFalse(student2 <= student1)

    def test_gt(self):
        """Тест оператора больше"""
        student1 = Student("Анна", 75)
        student2 = Student("Петр", 85)
        self.assertTrue(student2 > student1)
        self.assertFalse(student1 > student2)

    def test_ge(self):
        """Тест оператора больше или равно"""
        student1 = Student("Анна", 75)
        student2 = Student("Петр", 85)
        student3 = Student("Мария", 75)

        self.assertTrue(student2 >= student1)
        self.assertTrue(student1 >= student3)
        self.assertFalse(student1 >= student2)

    def test_eq(self):
        """Тест оператора равенства"""
        student1 = Student("Иван", 85)
        student2 = Student("Иван", 85)
        student3 = Student("Петр", 85)
        student4 = Student("Иван", 90)

        self.assertTrue(student1 == student2)
        self.assertFalse(student1 == student3)
        self.assertFalse(student1 == student4)
        self.assertFalse(student1 == "not a student")

    def test_ne(self):
        """Тест оператора неравенства"""
        student1 = Student("Иван", 85)
        student2 = Student("Петр", 85)
        student3 = Student("Иван", 85)

        self.assertTrue(student1 != student2)
        self.assertFalse(student1 != student3)

    def test_repr(self):
        """Тест строкового представления"""
        student = Student("Мария", 92)
        expected_repr = "Student('Мария', 92)"
        self.assertEqual(repr(student), expected_repr)


if __name__ == '__main__':
    unittest.main(verbosity=2)
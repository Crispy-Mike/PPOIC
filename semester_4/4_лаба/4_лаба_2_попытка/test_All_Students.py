import unittest
from unittest.mock import patch, MagicMock
from All_Students import All_Students
from Student import Student



class TestAllStudents(unittest.TestCase):
    def setUp(self):
        self.all_students = All_Students()
        self.all_students.students = []
        self.all_students.library = MagicMock()
        self.all_students.library.books = []

        self.test_student = Student("Иван", "Иванов", "ГР-101", "Информатика")
        self.test_student.educational_materials = ["Математика", "Физика"]
        self.test_student.exams = ["Математика"]
        self.test_student.schedule = {"Пн": ["Математика", "-", "Физика", "-"]}

    @patch('os.path.exists')
    @patch('os.remove')
    @patch('builtins.print')
    def test_clear_data(self, mock_print, mock_remove, mock_exists):
        self.all_students.students = [self.test_student]
        self.all_students.library.books = [MagicMock()]
        mock_exists.return_value = True

        self.all_students.clear_data("test.json")

        self.assertEqual(self.all_students.students, [])
        self.assertEqual(self.all_students.library.books, [])
        mock_remove.assert_called_once_with("test.json")

    @patch('builtins.open')
    @patch('json.dump')
    @patch('builtins.print')
    def test_save_data(self, mock_print, mock_json_dump, mock_open):
        self.all_students.students = [self.test_student]
        self.all_students.save_data("test.json")
        mock_json_dump.assert_called_once()

    @patch('os.path.exists')
    @patch('builtins.print')
    def test_load_data_file_not_found(self, mock_print, mock_exists):
        mock_exists.return_value = False
        self.all_students.load_data("test.json")
        mock_print.assert_called_with("Файл не найден, начинаем с пустыми данными")

    @patch('builtins.input')
    @patch('builtins.print')
    def test_new_student_existing_group(self, mock_print, mock_input):
        self.all_students.students = [self.test_student]
        mock_input.side_effect = ["Петр", "Петров", "ГР-101", "да"]

        self.all_students.new_student()

        self.assertEqual(len(self.all_students.students), 2)

    @patch('builtins.input')
    @patch('builtins.print')
    def test_new_student_new_group(self, mock_print, mock_input):
        self.all_students.students = []
        mock_input.side_effect = [
            "Анна", "Смирнова", "ГР-202", "нет",
            "Информатика", "2", "Математика", "Физика", "1", "Математика",
            "", "", "", "", "", "", ""
        ]

        self.all_students.new_student()

        self.assertEqual(len(self.all_students.students), 1)
        self.assertEqual(self.all_students.students[0].name, "Анна")

    @patch('builtins.input')
    @patch('builtins.print')
    def test_new_student_empty_name(self, mock_print, mock_input):
        self.all_students.students = []
        mock_input.side_effect = [
            "", "Иван", "Иванов", "ГР-101", "нет",
            "Информатика", "1", "Математика", "0",
            "", "", "", "", "", "", ""
        ]

        self.all_students.new_student()

        mock_print.assert_any_call("Имя не может быть пустым!")
        self.assertEqual(len(self.all_students.students), 1)

    @patch('builtins.input')
    @patch('builtins.print')
    def test_redact_student_change_name(self, mock_print, mock_input):
        self.all_students.students = [self.test_student]
        mock_input.side_effect = ["Иван", "Иванов", "1", "Петр", "0"]

        self.all_students.redact_student()

        self.assertEqual(self.all_students.students[0].name, "Петр")

    @patch('builtins.input')
    @patch('builtins.print')
    def test_redact_student_change_surname(self, mock_print, mock_input):
        self.all_students.students = [self.test_student]
        mock_input.side_effect = ["Иван", "Иванов", "2", "Петров", "0"]

        self.all_students.redact_student()

        self.assertEqual(self.all_students.students[0].surname, "Петров")

    @patch('builtins.input')
    @patch('builtins.print')
    def test_redact_student_change_group(self, mock_print, mock_input):
        self.all_students.students = [self.test_student]
        mock_input.side_effect = ["Иван", "Иванов", "3", "ГР-202", "0"]

        self.all_students.redact_student()

        self.assertEqual(self.all_students.students[0].group, "ГР-202")

    @patch('builtins.input')
    @patch('builtins.print')
    def test_redact_student_add_material(self, mock_print, mock_input):
        self.all_students.students = [self.test_student]
        mock_input.side_effect = ["Иван", "Иванов", "5", "1", "История", "0"]

        self.all_students.redact_student()

        self.assertIn("История", self.all_students.students[0].educational_materials)

    @patch('builtins.input')
    @patch('builtins.print')
    def test_redact_student_remove_material(self, mock_print, mock_input):
        self.all_students.students = [self.test_student]
        mock_input.side_effect = ["Иван", "Иванов", "5", "2", "1", "0"]

        self.all_students.redact_student()

        self.assertNotIn("Математика", self.all_students.students[0].educational_materials)

    @patch('builtins.input')
    @patch('builtins.print')
    def test_redact_student_add_exam(self, mock_print, mock_input):
        self.all_students.students = [self.test_student]
        mock_input.side_effect = ["Иван", "Иванов", "6", "1", "Физика", "0"]

        self.all_students.redact_student()

        self.assertIn("Физика", self.all_students.students[0].exams)

    @patch('builtins.input')
    @patch('builtins.print')
    def test_redact_student_not_found(self, mock_print, mock_input):
        self.all_students.students = [self.test_student]
        mock_input.side_effect = ["Петр", "Петров"]

        self.all_students.redact_student()

        mock_print.assert_any_call("Студент Петр Петров не найден!")

    @patch('builtins.input')
    @patch('builtins.print')
    def test_redact_student_empty_list(self, mock_print, mock_input):
        self.all_students.students = []

        self.all_students.redact_student()

        mock_print.assert_called_with("Список студентов пуст! Нечего редактировать.")

    @patch('builtins.input')
    @patch('builtins.print')
    def test_delete_student_success(self, mock_print, mock_input):
        self.all_students.students = [self.test_student]
        mock_input.side_effect = ["Иван", "Иванов", "да"]

        self.all_students.delete_student()

        self.assertEqual(len(self.all_students.students), 0)
        mock_print.assert_any_call("Студент Иван Иванов удален!")

    @patch('builtins.input')
    @patch('builtins.print')
    def test_delete_student_cancelled(self, mock_print, mock_input):
        self.all_students.students = [self.test_student]
        mock_input.side_effect = ["Иван", "Иванов", "нет"]

        self.all_students.delete_student()

        self.assertEqual(len(self.all_students.students), 1)
        mock_print.assert_any_call("Удаление отменено")

    @patch('builtins.input')
    @patch('builtins.print')
    def test_delete_student_not_found(self, mock_print, mock_input):
        self.all_students.students = [self.test_student]
        mock_input.side_effect = ["Петр", "Петров", "да"]

        self.all_students.delete_student()

        self.assertEqual(len(self.all_students.students), 1)
        mock_print.assert_any_call("Студент Петр Петров не найден!")

    @patch('builtins.input')
    @patch('builtins.print')
    def test_delete_student_empty_list(self, mock_print, mock_input):
        self.all_students.students = []

        self.all_students.delete_student()

        mock_print.assert_called_with("Список студентов пуст!")

    @patch('builtins.input')
    @patch('builtins.print')
    def test_visit_of_last_week_new_visits(self, mock_print, mock_input):
        self.all_students.students = [self.test_student]
        self.test_student.visits = {}
        with patch.object(self.test_student, 'new_visit') as mock_new_visit:
            mock_input.side_effect = ["Иван", "Иванов"]
            self.all_students.visit_of_last_week()
            mock_new_visit.assert_called_once()

    @patch('builtins.input')
    @patch('builtins.print')
    def test_visit_of_last_week_student_not_found(self, mock_print, mock_input):
        self.all_students.students = [self.test_student]
        mock_input.side_effect = ["Петр", "Петров"]

        self.all_students.visit_of_last_week()

        mock_print.assert_any_call("Студент Петр Петров не найден!")

    @patch('builtins.input')
    @patch('builtins.print')
    def test_material_study_operation_success(self, mock_print, mock_input):
        self.all_students.students = [self.test_student]
        with patch.object(self.test_student, 'new_marks') as mock_new_marks:
            mock_input.side_effect = ["Иван", "Иванов"]
            self.all_students.material_study_operation()
            mock_new_marks.assert_called_once()

    @patch('builtins.input')
    @patch('builtins.print')
    def test_exam_preparation_operation_success(self, mock_print, mock_input):
        self.all_students.students = [self.test_student]
        with patch.object(self.test_student, 'exam_check') as mock_exam_check:
            mock_input.side_effect = ["Иван", "Иванов"]
            self.all_students.exam_preparation_operation()
            mock_exam_check.assert_called_once()

    @patch('builtins.input')
    @patch('builtins.print')
    def test_curricular_planning_operation_success(self, mock_print, mock_input):
        self.all_students.students = [self.test_student]
        with patch.object(self.test_student, 'get_schedule') as mock_get_schedule:
            mock_input.side_effect = ["Иван", "Иванов"]
            self.all_students.curricular_planning_operation()
            mock_get_schedule.assert_called_once()

    @patch('builtins.input')
    @patch('builtins.print')
    def test_library_borrow_book(self, mock_print, mock_input):
        self.all_students.students = [self.test_student]
        self.all_students.library.books = [MagicMock(), MagicMock()]
        mock_input.side_effect = [
            "Иван", "Иванов",
            "1",
            "Война и мир", "Толстой",
            "0"
        ]

        self.all_students.operation_of_using_library_resources()

    @patch('builtins.input')
    @patch('builtins.print')
    def test_library_student_not_found(self, mock_print, mock_input):
        self.all_students.students = [self.test_student]
        mock_input.side_effect = ["Петр", "Петров"]

        self.all_students.operation_of_using_library_resources()

        mock_print.assert_any_call("\n Студент Петр Петров не найден!")

    @patch('builtins.input')
    @patch('builtins.print')
    def test_new_book(self, mock_print, mock_input):
        with patch.object(self.all_students.library, 'new_book') as mock_new_book:
            self.all_students.new_book()
            mock_new_book.assert_called_once()

    @patch('builtins.print')
    def test_empty_list_redact(self, mock_print):
        self.all_students.students = []
        self.all_students.redact_student()
        mock_print.assert_called_with("Список студентов пуст! Нечего редактировать.")

    @patch('builtins.print')
    def test_empty_list_delete(self, mock_print):
        self.all_students.students = []
        self.all_students.delete_student()
        mock_print.assert_called_with("Список студентов пуст!")

    @patch('builtins.print')
    def test_empty_list_visit(self, mock_print):
        self.all_students.students = []
        self.all_students.visit_of_last_week()
        mock_print.assert_called_with("Список студентов пуст!")

    @patch('builtins.print')
    def test_empty_list_material(self, mock_print):
        self.all_students.students = []
        self.all_students.material_study_operation()
        mock_print.assert_called_with("Список студентов пуст!")

    @patch('builtins.print')
    def test_empty_list_exam(self, mock_print):
        self.all_students.students = []
        self.all_students.exam_preparation_operation()
        mock_print.assert_called_with("Список студентов пуст!")

    @patch('builtins.print')
    def test_empty_list_curricular(self, mock_print):
        self.all_students.students = []
        self.all_students.curricular_planning_operation()
        mock_print.assert_called_with("Список студентов пуст!")

    @patch('builtins.print')
    def test_empty_list_library(self, mock_print):
        self.all_students.students = []
        self.all_students.operation_of_using_library_resources()
        mock_print.assert_called_with("Список студентов пуст!")
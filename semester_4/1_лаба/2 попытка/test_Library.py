import unittest
from unittest.mock import patch, MagicMock, call
from Library import Library
from Book import Book

class TestLibrary(unittest.TestCase):
    def setUp(self):
        self.library = Library()
        self.test_book = Book("Война и мир", "Толстой", "Роман", "Много текста")
        self.test_book2 = Book("Преступление и наказание", "Достоевский", "Роман", "Тоже много текста")
        self.test_book3 = Book("Анна Каренина", "Толстой", "Роман", "Про Анну")

    @patch('builtins.input')
    @patch('builtins.print')
    def test_new_book_success(self, mock_print, mock_input):
        mock_input.side_effect = ["Война и мир", "Толстой", "Роман", "Много текста"]
        self.library.new_book()
        self.assertEqual(len(self.library.books), 1)
        self.assertEqual(self.library.books[0].name_of_book, "Война и мир")
        self.assertEqual(self.library.books[0].name_of_author, "Толстой")
        self.assertEqual(self.library.books[0].genre, "Роман")
        self.assertEqual(self.library.books[0].content, "Много текста")
        mock_print.assert_called_once_with("Книга добавлена!")

    @patch('builtins.input')
    @patch('builtins.print')
    def test_new_book_multiple_books(self, mock_print, mock_input):
        mock_input.side_effect = ["Война и мир", "Толстой", "Роман", "Много текста"]
        self.library.new_book()
        mock_input.side_effect = ["Преступление и наказание", "Достоевский", "Роман", "Много текста"]
        self.library.new_book()
        self.assertEqual(len(self.library.books), 2)
        self.assertEqual(self.library.books[0].name_of_book, "Война и мир")
        self.assertEqual(self.library.books[1].name_of_book, "Преступление и наказание")

    @patch('builtins.input')
    @patch('builtins.print')
    def test_redact_book_change_name(self, mock_print, mock_input):
        self.library.books = [self.test_book]
        mock_input.side_effect = ["1", "Новое название", "5"]
        self.library.redact("Война и мир", "Толстой")
        self.assertEqual(self.library.books[0].name_of_book, "Новое название")
        mock_print.assert_any_call("Название изменено!")

    @patch('builtins.input')
    @patch('builtins.print')
    def test_redact_book_change_author(self, mock_print, mock_input):
        self.library.books = [self.test_book]
        mock_input.side_effect = ["2", "Достоевский", "5"]
        self.library.redact("Война и мир", "Толстой")
        self.assertEqual(self.library.books[0].name_of_author, "Достоевский")
        mock_print.assert_any_call("Имя автора изменено!")

    @patch('builtins.input')
    @patch('builtins.print')
    def test_redact_book_change_genre(self, mock_print, mock_input):
        self.library.books = [self.test_book]
        mock_input.side_effect = ["3", "Эпопея", "5"]
        self.library.redact("Война и мир", "Толстой")
        self.assertEqual(self.library.books[0].genre, "Эпопея")
        mock_print.assert_any_call("Жанр изменен!")

    @patch('builtins.input')
    @patch('builtins.print')
    def test_redact_book_change_content(self, mock_print, mock_input):
        self.library.books = [self.test_book]
        mock_input.side_effect = ["4", "Новое содержание", "5"]
        self.library.redact("Война и мир", "Толстой")
        self.assertEqual(self.library.books[0].content, "Новое содержание")
        mock_print.assert_any_call("Содержание изменено!")

    @patch('builtins.input')
    @patch('builtins.print')
    def test_redact_book_multiple_changes(self, mock_print, mock_input):
        self.library.books = [self.test_book]
        mock_input.side_effect = ["1", "Новое название", "2", "Новый автор", "3", "Новый жанр", "5"]
        self.library.redact("Война и мир", "Толстой")
        self.assertEqual(self.library.books[0].name_of_book, "Новое название")
        self.assertEqual(self.library.books[0].name_of_author, "Новый автор")
        self.assertEqual(self.library.books[0].genre, "Новый жанр")

    @patch('builtins.input')
    @patch('builtins.print')
    def test_redact_book_not_found(self, mock_print, mock_input):
        self.library.books = [self.test_book]
        self.library.redact("Не та книга", "Не тот автор")
        mock_print.assert_any_call("Книга не найдена!")

    @patch('builtins.input')
    @patch('builtins.print')
    def test_redact_book_empty_library_add_book_yes(self, mock_print, mock_input):
        self.library.books = []
        mock_input.side_effect = ["1", "Новая книга", "Автор", "Жанр", "Контент"]
        self.library.redact("любое", "любое")
        self.assertEqual(len(self.library.books), 1)
        self.assertEqual(self.library.books[0].name_of_book, "Новая книга")

    @patch('builtins.input')
    @patch('builtins.print')
    def test_redact_book_empty_library_add_book_no(self, mock_print, mock_input):
        self.library.books = []
        mock_input.side_effect = ["2"]
        self.library.redact("любое", "любое")
        self.assertEqual(len(self.library.books), 0)

    @patch('builtins.input')
    @patch('builtins.print')
    def test_redact_book_empty_library_invalid_then_valid(self, mock_print, mock_input):
        self.library.books = []
        mock_input.side_effect = ["3", "", "1", "Новая книга", "Автор", "Жанр", "Контент"]
        self.library.redact("любое", "любое")
        mock_print.assert_any_call("Вы ввели неправильное значение")
        self.assertEqual(len(self.library.books), 1)

    @patch('builtins.input')
    @patch('builtins.print')
    def test_redact_book_invalid_menu_choice_then_exit(self, mock_print, mock_input):
        self.library.books = [self.test_book]
        mock_input.side_effect = ["99", "", "5"]
        self.library.redact("Война и мир", "Толстой")
        mock_print.assert_any_call("Вы ввели неправильное значение")

    @patch('builtins.input')
    @patch('builtins.print')
    def test_redact_book_invalid_menu_choice_then_valid(self, mock_print, mock_input):
        self.library.books = [self.test_book]
        mock_input.side_effect = ["99", "", "1", "Новое название", "5"]
        self.library.redact("Война и мир", "Толстой")
        self.assertEqual(self.library.books[0].name_of_book, "Новое название")

    @patch('builtins.input')
    @patch('builtins.print')
    def test_delete_book_success(self, mock_print, mock_input):
        self.library.books = [self.test_book, self.test_book2]
        self.library.delete_book("Война и мир", "Толстой")
        self.assertEqual(len(self.library.books), 1)
        self.assertEqual(self.library.books[0].name_of_book, "Преступление и наказание")
        mock_print.assert_any_call("Книга 'Война и мир' удалена!")

    @patch('builtins.input')
    @patch('builtins.print')
    def test_delete_book_last_book(self, mock_print, mock_input):
        self.library.books = [self.test_book]
        self.library.delete_book("Война и мир", "Толстой")
        self.assertEqual(len(self.library.books), 0)

    @patch('builtins.input')
    @patch('builtins.print')
    def test_delete_book_not_found(self, mock_print, mock_input):
        self.library.books = [self.test_book, self.test_book2]
        self.library.delete_book("Не та книга", "Не тот автор")
        mock_print.assert_any_call("Книга не найдена!")
        self.assertEqual(len(self.library.books), 2)

    @patch('builtins.input')
    @patch('builtins.print')
    def test_delete_book_multiple_same_author_different_books(self, mock_print, mock_input):
        book1 = Book("Война и мир", "Толстой", "Роман", "1")
        book2 = Book("Анна Каренина", "Толстой", "Роман", "2")
        self.library.books = [book1, book2]
        self.library.delete_book("Война и мир", "Толстой")
        self.assertEqual(len(self.library.books), 1)
        self.assertEqual(self.library.books[0].name_of_book, "Анна Каренина")

    @patch('builtins.input')
    @patch('builtins.print')
    def test_delete_book_empty_library_add_book_yes(self, mock_print, mock_input):
        self.library.books = []
        mock_input.side_effect = ["1", "Новая книга", "Автор", "Жанр", "Контент"]
        self.library.delete_book("любое", "любое")
        self.assertEqual(len(self.library.books), 1)

    @patch('builtins.input')
    @patch('builtins.print')
    def test_delete_book_empty_library_add_book_no(self, mock_print, mock_input):
        self.library.books = []
        mock_input.side_effect = ["2"]
        self.library.delete_book("любое", "любое")
        self.assertEqual(len(self.library.books), 0)

    @patch('builtins.input')
    @patch('builtins.print')
    def test_delete_book_empty_library_invalid_then_valid(self, mock_print, mock_input):
        self.library.books = []
        mock_input.side_effect = ["3", "", "1", "Новая книга", "Автор", "Жанр", "Контент"]
        self.library.delete_book("любое", "любое")
        mock_print.assert_any_call("Вы ввели неправильное значение")
        self.assertEqual(len(self.library.books), 1)

    @patch('builtins.input')
    @patch('builtins.print')
    def test_delete_book_empty_library_multiple_invalid(self, mock_print, mock_input):
        self.library.books = []
        mock_input.side_effect = ["4", "5", "abc", "", "2"]
        self.library.delete_book("любое", "любое")
        self.assertEqual(len(self.library.books), 0)

    def test_redact_no_books_but_not_called(self):
        with patch('builtins.input') as mock_input, patch('builtins.print') as mock_print:
            mock_input.side_effect = ["2"]
            self.library.redact("любое", "любое")
            self.assertEqual(len(self.library.books), 0)

    def test_delete_no_books_but_not_called(self):
        with patch('builtins.input') as mock_input, patch('builtins.print') as mock_print:
            mock_input.side_effect = ["2"]
            self.library.delete_book("любое", "любое")
            self.assertEqual(len(self.library.books), 0)

    def test_redact_edit_exit_immediately(self):
        with patch('builtins.input') as mock_input, patch('builtins.print') as mock_print:
            mock_input.side_effect = ["5"]
            self.library.books = [self.test_book]
            self.library.redact("Война и мир", "Толстой")
            self.assertEqual(self.library.books[0].name_of_book, "Война и мир")

    def test_redact_find_by_different_criteria(self):
        with patch('builtins.input') as mock_input, patch('builtins.print') as mock_print:
            mock_input.side_effect = ["5"]
            self.library.books = [self.test_book, self.test_book2]
            self.library.redact("Преступление и наказание", "Достоевский")
            self.assertEqual(self.library.books[1].name_of_author, "Достоевский")

    def test_redact_case_sensitivity(self):
        with patch('builtins.input') as mock_input, patch('builtins.print') as mock_print:
            mock_input.side_effect = ["1", "Новое название", "5"]
            self.library.books = [self.test_book]
            self.library.redact("война и мир", "толстой")
            mock_print.assert_any_call("Книга не найдена!")

    def test_delete_case_sensitivity(self):
        with patch('builtins.print') as mock_print:
            self.library.books = [self.test_book]
            self.library.delete_book("война и мир", "толстой")
            mock_print.assert_any_call("Книга не найдена!")
            self.assertEqual(len(self.library.books), 1)

    def test_redact_edit_all_fields_in_sequence(self):
        with patch('builtins.input') as mock_input, patch('builtins.print') as mock_print:
            mock_input.side_effect = ["1", "Н1", "2", "А1", "3", "Ж1", "4", "С1", "5"]
            self.library.books = [self.test_book]
            self.library.redact("Война и мир", "Толстой")
            self.assertEqual(self.library.books[0].name_of_book, "Н1")
            self.assertEqual(self.library.books[0].name_of_author, "А1")
            self.assertEqual(self.library.books[0].genre, "Ж1")
            self.assertEqual(self.library.books[0].content, "С1")

    def test_redact_book_keep_editing_after_change(self):
        with patch('builtins.input') as mock_input, patch('builtins.print') as mock_print:
            mock_input.side_effect = ["1", "Н1", "2", "А1", "5"]
            self.library.books = [self.test_book]
            self.library.redact("Война и мир", "Толстой")
            self.assertEqual(self.library.books[0].name_of_book, "Н1")
            self.assertEqual(self.library.books[0].name_of_author, "А1")

    def test_redact_edit_non_existent_then_exit(self):
        with patch('builtins.input') as mock_input, patch('builtins.print') as mock_print:
            mock_input.side_effect = ["1", "Н1", "5"]
            self.library.books = [self.test_book, self.test_book2]
            self.library.redact("Не та книга", "Не тот автор")
            mock_print.assert_any_call("Книга не найдена!")

    def test_delete_book_multiple_calls(self):
        with patch('builtins.print') as mock_print:
            self.library.books = [self.test_book, self.test_book2, self.test_book3]
            self.library.delete_book("Война и мир", "Толстой")
            self.library.delete_book("Анна Каренина", "Толстой")
            self.assertEqual(len(self.library.books), 1)
            self.assertEqual(self.library.books[0].name_of_book, "Преступление и наказание")

    def test_redact_book_after_delete(self):
        with patch('builtins.input') as mock_input, patch('builtins.print') as mock_print:
            mock_input.side_effect = ["1", "Обновленное название", "5"]
            self.library.books = [self.test_book, self.test_book2]
            self.library.delete_book("Война и мир", "Толстой")
            self.library.redact("Преступление и наказание", "Достоевский")
            self.assertEqual(self.library.books[0].name_of_book, "Обновленное название")

    def test_redact_edit_and_cancel(self):
        with patch('builtins.input') as mock_input, patch('builtins.print') as mock_print:
            mock_input.side_effect = ["1", "Новое название", "5"]
            self.library.books = [self.test_book]
            self.library.redact("Война и мир", "Толстой")
            self.assertEqual(self.library.books[0].name_of_book, "Новое название")

    def test_new_book_unicode_characters(self):
        with patch('builtins.input') as mock_input, patch('builtins.print') as mock_print:
            mock_input.side_effect = ["Книга ©", "Автор ®", "Жанр ✓", "Текст "]
            self.library.new_book()
            self.assertEqual(self.library.books[0].name_of_book, "Книга ©")
            self.assertEqual(self.library.books[0].name_of_author, "Автор ®")
            self.assertEqual(self.library.books[0].genre, "Жанр ✓")
            self.assertEqual(self.library.books[0].content, "Текст ")

    def test_redact_empty_string_fields(self):
        with patch('builtins.input') as mock_input, patch('builtins.print') as mock_print:
            mock_input.side_effect = ["1", "", "5"]
            self.library.books = [self.test_book]
            self.library.redact("Война и мир", "Толстой")
            self.assertEqual(self.library.books[0].name_of_book, "")

    def test_delete_book_after_redact(self):
        with patch('builtins.input') as mock_input, patch('builtins.print') as mock_print:
            mock_input.side_effect = ["1", "Новое название", "5"]
            self.library.books = [self.test_book]
            self.library.redact("Война и мир", "Толстой")
            self.library.delete_book("Новое название", "Толстой")
            self.assertEqual(len(self.library.books), 0)

    def test_multiple_operations_sequence(self):
        with patch('builtins.input') as mock_input, patch('builtins.print') as mock_print:
            mock_input.side_effect = ["Книга1", "Автор1", "Жанр1", "Текст1"]
            self.library.new_book()
            mock_input.side_effect = ["Книга2", "Автор2", "Жанр2", "Текст2"]
            self.library.new_book()
            mock_input.side_effect = ["1", "Измененная книга1", "5"]
            self.library.redact("Книга1", "Автор1")
            self.library.delete_book("Книга2", "Автор2")
            self.assertEqual(len(self.library.books), 1)
            self.assertEqual(self.library.books[0].name_of_book, "Измененная книга1")
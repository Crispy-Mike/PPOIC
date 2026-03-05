import unittest
from unittest.mock import patch, MagicMock
from Book import Book


class TestBook(unittest.TestCase):
    def setUp(self):
        self.book = Book("Война и мир", "Толстой", "Роман", "Много текста")

    def test_init_sets_attributes_correctly(self):
        book = Book("Преступление и наказание", "Достоевский", "Роман", "Текст")
        self.assertEqual(book.name_of_book, "Преступление и наказание")
        self.assertEqual(book.name_of_author, "Достоевский")
        self.assertEqual(book.genre, "Роман")
        self.assertEqual(book.content, "Текст")

    def test_init_with_empty_strings(self):
        book = Book("", "", "", "")
        self.assertEqual(book.name_of_book, "")
        self.assertEqual(book.name_of_author, "")
        self.assertEqual(book.genre, "")
        self.assertEqual(book.content, "")

    def test_init_with_whitespace(self):
        book = Book("  Название  ", "  Автор  ", "  Жанр  ", "  Контент  ")
        self.assertEqual(book.name_of_book, "  Название  ")
        self.assertEqual(book.name_of_author, "  Автор  ")
        self.assertEqual(book.genre, "  Жанр  ")
        self.assertEqual(book.content, "  Контент  ")

    def test_init_with_special_characters(self):
        book = Book("!@#$%", "^*&()", "_-=+", "[]{};:'")
        self.assertEqual(book.name_of_book, "!@#$%")
        self.assertEqual(book.name_of_author, "^*&()")
        self.assertEqual(book.genre, "_-=+")
        self.assertEqual(book.content, "[]{};:'")

    def test_init_with_unicode(self):
        book = Book("Книга ©", "Автор ®", "Жанр ✓", "Текст ")
        self.assertEqual(book.name_of_book, "Книга ©")
        self.assertEqual(book.name_of_author, "Автор ®")
        self.assertEqual(book.genre, "Жанр ✓")
        self.assertEqual(book.content, "Текст ")

    def test_attributes_are_strings(self):
        self.assertIsInstance(self.book.name_of_book, str)
        self.assertIsInstance(self.book.name_of_author, str)
        self.assertIsInstance(self.book.genre, str)
        self.assertIsInstance(self.book.content, str)

    def test_attributes_can_be_modified(self):
        self.book.name_of_book = "Новое название"
        self.book.name_of_author = "Новый автор"
        self.book.genre = "Новый жанр"
        self.book.content = "Новое содержание"

        self.assertEqual(self.book.name_of_book, "Новое название")
        self.assertEqual(self.book.name_of_author, "Новый автор")
        self.assertEqual(self.book.genre, "Новый жанр")
        self.assertEqual(self.book.content, "Новое содержание")

    def test_modifying_one_attribute_preserves_others(self):
        original_author = self.book.name_of_author
        original_genre = self.book.genre
        original_content = self.book.content

        self.book.name_of_book = "Новое название"

        self.assertEqual(self.book.name_of_author, original_author)
        self.assertEqual(self.book.genre, original_genre)
        self.assertEqual(self.book.content, original_content)

    def test_different_books_are_different_objects(self):
        book1 = Book("Книга1", "Автор1", "Жанр1", "Содержание1")
        book2 = Book("Книга2", "Автор2", "Жанр2", "Содержание2")
        self.assertIsNot(book1, book2)
        self.assertNotEqual(book1.name_of_book, book2.name_of_book)
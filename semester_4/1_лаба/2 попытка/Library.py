    from Book import Book
    
    
    class Library:
        def __init__(self):
            self.books = []
    
        def new_book(self):
            name_of_book = input("Введите название книги:\n")
            name_of_author = input("Введите имя автора:\n")
            genre = input("Введите жанр книги:\n")
            content = input("Содержание книги:\n")
            book = Book(name_of_book, name_of_author, genre, content)
            self.books.append(book)
            print("Книга добавлена!")
    
        def redact(self, name_of_book, name_of_author):
            if len(self.books) == 0:
                while True:
                    print("Книг нет, хотите добавить новую? (1-да,2-нет)")
                    choice = input("Ваш ответ: ").strip()
                    if choice == "1":
                        self.new_book()
                        return
                    elif choice == "2":
                        return
                    else:
                        print("Вы ввели неправильное значение")
                        input("Нажмите \"Enter\" для продолжения")
            else:
                for x in self.books:
                    if x.name_of_book == name_of_book and x.name_of_author == name_of_author:
                        while True:
                            print("\n" * 50)
                            print(f"Название книги: {x.name_of_book}")
                            print(f"Имя автора: {x.name_of_author}")
                            print(f"Жанр: {x.genre}")
                            print(f"Содержание: {x.content}")
                            print("Что вы хотите изменить?")
                            print("1. Название книги")
                            print("2. Имя автора")
                            print("3. Жанр")
                            print("4. Содержание")
                            print("5. Выйти")
                            choice = input("Ваш выбор: ").strip()
                            if choice == "1":
                                new_name_of_book = input("Введите новое название: ")
                                x.name_of_book = new_name_of_book
                                print("Название изменено!")
                            elif choice == "2":
                                new_name_of_author = input("Введите новое имя автора: ")
                                x.name_of_author = new_name_of_author
                                print("Имя автора изменено!")
                            elif choice == "3":
                                new_genre = input("Введите новый жанр: ")
                                x.genre = new_genre
                                print("Жанр изменен!")
                            elif choice == "4":
                                new_content = input("Введите новое содержание: ")
                                x.content = new_content
                                print("Содержание изменено!")
                            elif choice == "5":
                                return
                            else:
                                print("Вы ввели неправильное значение")
                                input("Нажмите \"Enter\" для продолжения")
                        return
                print("Книга не найдена!")
    
        def delete_book(self, name_of_book, name_of_author):
            if len(self.books) == 0:
                while True:
                    print("Книг нет, хотите добавить новую? (1-да,2-нет)")
                    choice = input("Ваш ответ: ").strip()
                    if choice == "1":
                        self.new_book()
                        return
                    elif choice == "2":
                        return
                    else:
                        print("Вы ввели неправильное значение")
                        input("Нажмите \"Enter\" для продолжения")
            else:
                for book in self.books:
                    if book.name_of_book == name_of_book and book.name_of_author == name_of_author:
                        self.books.remove(book)
                        print(f"Книга '{name_of_book}' удалена!")
                        return
                print("Книга не найдена!")
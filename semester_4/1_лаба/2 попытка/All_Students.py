from Student import Student
from Global_variables import DAYS, TIME_OF_CLASSES
from Library import Library
from Book import Book
import json
import os


class All_Students:
    def __init__(self):
        self.students = []
        self.library = Library()
        self.load_data()

    def clear_data(self, filename="students_data.json"):
        self.students.clear()
        self.library.books.clear()

        if os.path.exists(filename):
            os.remove(filename)
            print(f"Файл {filename} удалён")

        print(" Все данные полностью очищены!")

    def save_data(self, filename="students_data.json"):
        data = []

        for student in self.students:
            student_data = {
                "name": student.name,
                "surname": student.surname,
                "group": student.group,
                "specialty": student.specialty,
                "educational_materials": student.educational_materials,
                "exams": student.exams,
                "schedule": student.schedule,
                "visits": student.visits,
                "marks": student.marks,
                "marks_of_materials": student.marks_of_materials,
                "books": [
                    {
                        "name_of_book": book.name_of_book,
                        "name_of_author": book.name_of_author,
                        "genre": book.genre,
                        "content": book.content
                    } for book in student.books
                ]
            }
            data.append(student_data)

        library_data = {
            "students": data,
            "library": {
                "books": [
                    {
                        "name_of_book": book.name_of_book,
                        "name_of_author": book.name_of_author,
                        "genre": book.genre,
                        "content": book.content
                    } for book in self.library.books
                ]
            }
        }

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(library_data, f, ensure_ascii=False, indent=4)
            print(f"Данные сохранены: {len(self.students)} студентов, {len(self.library.books)} книг в библиотеке")
        except Exception as e:
            print(f"Ошибка сохранения: {e}")

    def load_data(self, filename="students_data.json"):
        if not os.path.exists(filename):
            print("Файл не найден, начинаем с пустыми данными")
            return

        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)

            self.students.clear()
            self.library.books.clear()

            library_data = data.get("library", {}).get("books", [])
            for book_data in library_data:
                book = Book(
                    book_data["name_of_book"],
                    book_data["name_of_author"],
                    book_data["genre"],
                    book_data.get("content", "")
                )
                self.library.books.append(book)

            students_data = data.get("students", [])
            for student_data in students_data:
                student = Student(
                    student_data["name"],
                    student_data["surname"],
                    student_data["group"],
                    student_data["specialty"]
                )

                for field in ["educational_materials", "exams", "schedule",
                              "visits", "marks", "marks_of_materials"]:
                    setattr(student, field, student_data.get(field, []))

                student.books.clear()
                for book_data in student_data.get("books", []):
                    book = Book(
                        book_data["name_of_book"],
                        book_data["name_of_author"],
                        book_data["genre"],
                        book_data.get("content", "")
                    )
                    student.books.append(book)

                self.students.append(student)

            print(f"Загружено: {len(self.students)} студентов, "
                  f"{len(self.library.books)} книг в библиотеке из {filename}")

        except json.JSONDecodeError as e:
            print(f"Ошибка формата JSON: {e}")
        except Exception as e:
            print(f"Ошибка загрузки: {e}")

    def new_student(self):
        while True:
            name = input("Введите имя: ").strip()
            if name:
                break
            print("Имя не может быть пустым!")

        while True:
            surname = input("Введите фамилию: ").strip()
            if surname:
                break
            print("Фамилия не может быть пустой!")

        while True:
            group = input("Введите группу: ").strip()
            if group:
                break
            print("Группа не может быть пустой!")

        existing_group = None
        for student in self.students:
            if student.group == group:
                existing_group = student
                break

        if existing_group:
            print(f"Найдена группа {group} со специальностью: {existing_group.specialty}")
            print("Скопировать данные группы? (да/нет): ", end="")
            use_group_data = input().strip().lower()

            if use_group_data in ["да", "д", "y", "1"]:
                student = Student(name, surname, group, existing_group.specialty)
                student.educational_materials = existing_group.educational_materials.copy()
                student.exams = existing_group.exams.copy()
                student.schedule = {day: sched.copy() for day, sched in existing_group.schedule.items()}
                self.students.append(student)
                print(f"Студент {name} {surname} добавлен в группу {group}")
                return
            else:
                use_new_data = True
        else:
            use_new_data = True

        while True:
            specialty = input("Введите специальность: ").strip()
            if specialty:
                break
            print("Специальность не может быть пустой!")

        while True:
            try:
                qty_materials = input("Количество учебных предметов (1-20): ").strip()
                quantity_of_educational_materials = int(qty_materials)
                if 1 <= quantity_of_educational_materials <= 20:
                    break
                print("Введите число от 1 до 20!")
            except ValueError:
                print("Введите целое число!")

        educational_materials = []
        for x in range(quantity_of_educational_materials):
            while True:
                ed_material = input(f"Предмет {x + 1}: ").strip()
                if not ed_material:
                    print("Название не может быть пустым!")
                elif ed_material in educational_materials:
                    print("Этот предмет уже добавлен!")
                else:
                    educational_materials.append(ed_material)
                    print(f"Добавлен: {ed_material}")
                    break

        while True:
            try:
                qty_exams = input(f"Количество экзаменов (0-{quantity_of_educational_materials}): ").strip()
                quantity_of_exams = int(qty_exams)
                if 0 <= quantity_of_exams <= quantity_of_educational_materials:
                    break
                print(f"Максимум {quantity_of_educational_materials} экзаменов!")
            except ValueError:
                print("Введите целое число!")

        exams = []
        for x in range(quantity_of_exams):
            while True:
                print(f"Доступные предметы: {', '.join(educational_materials)}")
                exam = input(f"Экзамен {x + 1}: ").strip()
                if not exam:
                    print("Название не может быть пустым!")
                elif exam not in educational_materials:
                    print("Экзамен только по существующим предметам!")
                elif exam in exams:
                    print("Этот экзамен уже добавлен!")
                else:
                    exams.append(exam)
                    print(f"Добавлен экзамен: {exam}")
                    break

        schedule = {}
        for day in DAYS:
            print(f"\n--- Расписание на {day} ---")
            for index, time in enumerate(TIME_OF_CLASSES, start=1):
                print(f"{index}. {time}")

            while True:
                classes_input = input("Номера пар через пробел (или Enter для пустого дня): ").strip()
                if not classes_input:
                    schedule[day] = ["-"] * len(TIME_OF_CLASSES)
                    print(f"На {day} пар нет")
                    break

                try:
                    class_numbers = [int(x) for x in classes_input.split()]
                    invalid_numbers = [n for n in class_numbers if not (1 <= n <= len(TIME_OF_CLASSES))]
                    if invalid_numbers:
                        print(f"Неверные номера пар: {invalid_numbers}")
                        print(f"Допустимые номера: 1-{len(TIME_OF_CLASSES)}")
                        continue

                    duplicates = len(class_numbers) != len(set(class_numbers))
                    if duplicates:
                        print("Нельзя указывать одну пару дважды!")
                        continue

                    student_day_schedule = ["-"] * len(TIME_OF_CLASSES)
                    for class_num in class_numbers:
                        i = class_num - 1
                        while True:
                            name_of_class = input(f"Предмет на {TIME_OF_CLASSES[i]}: ").strip()
                            if not name_of_class:
                                print("Название предмета обязательно!")
                                continue
                            if name_of_class not in educational_materials:
                                print(f"Предмет должен быть из списка: {', '.join(educational_materials)}")
                                continue
                            student_day_schedule[i] = name_of_class
                            print(f"Запланировано: {name_of_class}")
                            break

                    schedule[day] = student_day_schedule
                    break
                except ValueError:
                    print("Введите номера через пробел (например: 1 3 5)!")

        student = Student(name, surname, group, specialty)
        student.educational_materials = educational_materials
        student.exams = exams
        student.schedule = schedule
        self.students.append(student)

        print(f"\nСтудент {name} {surname} успешно добавлен!")
        print(f"Группа: {group}, Специальность: {specialty}")
        print(f"Предметов: {len(educational_materials)}, Экзаменов: {len(exams)}")

    def redact_student(self):
        if not self.students:
            print("Список студентов пуст! Нечего редактировать.")
            return

        name = input("Введите имя студента: ").strip()
        surname = input("Введите фамилию студента: ").strip()

        for student in self.students:
            if student.name == name and student.surname == surname:
                student.get_information()

                while True:
                    print("\nВыберите то, что вы хотите изменить:")
                    print("1. Имя")
                    print("2. Фамилию")
                    print("3. Номер группы")
                    print("4. Специальность")
                    print("5. Учебные предметы")
                    print("6. Экзамены")
                    print("7. Книги")
                    print("8. Расписание")
                    print("9. Посещения")
                    print("0. Выйти")

                    choice = input("Ваш выбор: ").strip()

                    if choice == "1":
                        new_name = input("Введите новое имя: ").strip()
                        student.name = new_name
                        print("Имя изменено!")

                    elif choice == "2":
                        new_surname = input("Введите новую фамилию: ").strip()
                        student.surname = new_surname
                        print("Фамилия изменена!")

                    elif choice == "3":
                        new_group = input("Введите новый номер группы: ").strip()
                        student.group = new_group
                        print("Номер группы изменен!")

                    elif choice == "4":
                        new_specialty = input("Введите новую специальность: ").strip()
                        student.specialty = new_specialty
                        print("Специальность изменена!")

                    elif choice == "5":
                        print("Текущие предметы:", student.educational_materials)
                        print("1. Добавить предмет")
                        print("2. Удалить предмет")
                        sub_choice = input("Ваш выбор: ").strip()

                        if sub_choice == "1":
                            new_material = input("Введите название предмета: ").strip()
                            if new_material and new_material not in student.educational_materials:
                                student.educational_materials.append(new_material)
                                print(f"Предмет '{new_material}' добавлен!")
                            else:
                                print("Предмет уже существует или название пустое!")

                        elif sub_choice == "2":
                            if student.educational_materials:
                                for i, m in enumerate(student.educational_materials, 1):
                                    print(f"{i}. {m}")
                                del_choice = input("Введите номер предмета для удаления: ").strip()
                                try:
                                    idx = int(del_choice) - 1
                                    if 0 <= idx < len(student.educational_materials):
                                        removed = student.educational_materials.pop(idx)
                                        print(f"Предмет '{removed}' удален!")
                                    else:
                                        print("Неверный номер!")
                                except ValueError:
                                    print("Введите число!")
                            else:
                                print("Список предметов пуст!")

                    elif choice == "6":
                        print("Текущие экзамены:", student.exams)
                        print("1. Добавить экзамен")
                        print("2. Удалить экзамен")
                        sub_choice = input("Ваш выбор: ").strip()

                        if sub_choice == "1":
                            new_exam = input("Введите название экзамена: ").strip()
                            if new_exam in student.educational_materials:
                                if new_exam not in student.exams:
                                    student.exams.append(new_exam)
                                    print(f"Экзамен '{new_exam}' добавлен!")
                                else:
                                    print("Такой экзамен уже есть!")
                            else:
                                print("Нельзя добавить экзамен по предмету, которого нет в учебных материалах!")

                        elif sub_choice == "2":
                            if student.exams:
                                for i, e in enumerate(student.exams, 1):
                                    print(f"{i}. {e}")
                                del_choice = input("Введите номер экзамена для удаления: ").strip()
                                try:
                                    idx = int(del_choice) - 1
                                    if 0 <= idx < len(student.exams):
                                        removed = student.exams.pop(idx)
                                        print(f"Экзамен '{removed}' удален!")
                                    else:
                                        print("Неверный номер!")
                                except ValueError:
                                    print("Введите число!")
                            else:
                                print("Список экзаменов пуст!")

                    elif choice == "7":
                        if not self.library.books:
                            print("В библиотеке нет книг!")
                        else:
                            print("Книги в библиотеке:")
                            for i, book in enumerate(self.library.books, 1):
                                print(f"{i}. {book.name_of_book} - {book.name_of_author}")
                            book_choice = input("Введите номер книги для выдачи студенту (0 - отмена): ").strip()
                            try:
                                idx = int(book_choice) - 1
                                if idx >= 0 and idx < len(self.library.books):
                                    book = self.library.books[idx]
                                    student.books.append(book)
                                    self.library.books.remove(book)
                                    print(f"Книга '{book.name_of_book}' выдана студенту!")
                                elif idx == -1:
                                    print("Операция отменена")
                                else:
                                    print("Неверный номер!")
                            except ValueError:
                                print("Введите число!")

                    elif choice == "8":
                        print("Редактирование расписания:")
                        student.get_schedule()
                        print("\n1. Изменить расписание")
                        print("2. Вернуться")
                        sub_choice = input("Ваш выбор: ").strip()

                        if sub_choice == "1":
                            student.schedule = {}
                            for day in DAYS:
                                try:
                                    quantity = int(input(f"Введите количество пар в день {day}: ").strip())
                                    if quantity <= 0:
                                        student.schedule[day] = ["-"] * len(TIME_OF_CLASSES)
                                        continue

                                    for index, time in enumerate(TIME_OF_CLASSES, 1):
                                        print(f"{index}. {time}")

                                    classes = input("Введите номера пар через пробел: ").split()
                                    class_numbers = [int(x) for x in classes if x.strip().isdigit()]

                                    day_schedule = []
                                    for i in range(len(TIME_OF_CLASSES)):
                                        if (i + 1) in class_numbers:
                                            subject = input(f"Введите предмет на {TIME_OF_CLASSES[i]}: ").strip()
                                            day_schedule.append(subject if subject else "-")
                                        else:
                                            day_schedule.append("-")
                                    student.schedule[day] = day_schedule
                                except ValueError:
                                    print("Ошибка ввода! Пропускаем день.")
                                    student.schedule[day] = ["-"] * len(TIME_OF_CLASSES)
                            print("Расписание обновлено!")

                    elif choice == "9":
                        print("Редактирование посещений:")
                        student.new_visit()

                    elif choice == "0":
                        print("Выход из редактирования")
                        return

                    else:
                        print("Неверный выбор! Попробуйте снова.")

                return

        print(f"Студент {name} {surname} не найден!")

    def delete_student(self):
        if not self.students:
            print("Список студентов пуст!")
            return

        name = input("Введите имя студента: ")
        surname = input("Введите фамилию студента: ")

        for student in self.students:
            if student.name == name and student.surname == surname:
                print(f"\nНайден студент: {student.name} {student.surname}")
                print(f"Группа: {student.group}")
                print(f"Специальность: {student.specialty}")

                confirm = input("\nВы уверены, что хотите удалить этого студента? (да/нет): ")
                if confirm.lower() == "да":
                    self.students.remove(student)
                    print(f"Студент {name} {surname} удален!")
                else:
                    print("Удаление отменено")
                return

        print(f"Студент {name} {surname} не найден!")

    def visit_of_last_week(self):
        if not self.students:
            print("Список студентов пуст!")
            return

        name = input("Введите имя студента: ")
        surname = input("Введите фамилию студента: ")
        for student in self.students:
            if student.name == name and student.surname == surname:
                if student.visits:
                    while True:
                        answer = input("Его посещения расставлены, вы уверены, что хотите изменить их?(1-да,2-нет)")
                        if answer in ["1", "да"]:
                            student.new_visit()
                            return
                        elif answer in ["2", "нет"]:
                            return
                        else:
                            print("Неправильный ввод")
                else:
                    student.new_visit()
                    return
        print(f"Студент {name} {surname} не найден!")
        return

    def material_study_operation(self):
        if not self.students:
            print("Список студентов пуст!")
            return

        name = input("Введите имя студента: ").strip()
        surname = input("Введите фамилию студента: ").strip()

        for student in self.students:
            if student.name == name and student.surname == surname:
                student.new_marks()
                return

        print(f"Студент {name} {surname} не найден!")

    def exam_preparation_operation(self):
        if not self.students:
            print("Список студентов пуст!")
            return

        name = input("Введите имя студента: ").strip()
        surname = input("Введите фамилию студента: ").strip()

        for student in self.students:
            if student.name == name and student.surname == surname:
                student.exam_check()
                return

        print(f"Студент {name} {surname} не найден!")

    def curricular_planning_operation(self):
        if not self.students:
            print("Список студентов пуст!")
            return

        name = input("Введите имя студента: ").strip()
        surname = input("Введите фамилию студента: ").strip()

        for student in self.students:
            if student.name == name and student.surname == surname:
                student.get_schedule()
                return

        print(f"Студент {name} {surname} не найден!")

    def operation_of_using_library_resources(self):
        if not self.students:
            print("Список студентов пуст!")
            return

        library = self.library
        name = input("Введите имя студента: ").strip()
        surname = input("Введите фамилию студента: ").strip()

        student_found = False

        for student in self.students:
            if student.name == name and student.surname == surname:
                student_found = True

                while True:
                    print("\n" + "=" * 40)
                    print("БИБЛИОТЕКА")
                    print("=" * 40)
                    print("1 - Взять книгу")
                    print("2 - Вернуть книгу")
                    print("0 - Выйти")
                    print("-" * 40)
                    answer = input("Ваш ответ: ").strip()

                    if answer == "1":  # ВЗЯТЬ
                        if not library.books:
                            while True:
                                print("\n В библиотеке нет книг!")
                                add_answer = input("Хотите добавить книги? (1-да, 2-нет): ").strip()
                                if add_answer in ["1", "да"]:
                                    library.new_book()
                                    break
                                elif add_answer in ["2", "нет"]:
                                    break
                                else:
                                    print("Неверный ввод!")
                            continue

                        print("\n КНИГИ В БИБЛИОТЕКЕ:")
                        for i, book in enumerate(library.books, 1):
                            print(f"{i}. {book.name_of_book} | {book.name_of_author} | {book.genre}")

                        name_book = input("\nВведите название книги: ").strip()
                        name_author = input("Введите имя автора: ").strip()

                        book_found = None
                        for book in library.books:
                            if book.name_of_book == name_book and book.name_of_author == name_author:
                                book_found = book
                                break

                        if book_found:
                            student.books.append(book_found)
                            library.books.remove(book_found)
                            print(f"\n Книга '{name_book}' выдана студенту {student.name}")
                        else:
                            print("\n Книга не найдена!")

                    elif answer == "2":  # ВЕРНУТЬ
                        if not student.books:
                            print("\n📭 У студента нет книг для возврата")
                            continue

                        print("\nКНИГИ У СТУДЕНТА:")
                        for i, book in enumerate(student.books, 1):
                            print(f"{i}. {book.name_of_book} | {book.name_of_author} | {book.genre}")

                        name_book = input("\nВведите название книги: ").strip()
                        name_author = input("Введите имя автора: ").strip()

                        book_found = None
                        for book in student.books:
                            if book.name_of_book == name_book and book.name_of_author == name_author:
                                book_found = book
                                break

                        if book_found:
                            library.books.append(book_found)
                            student.books.remove(book_found)
                            print(f"\n Книга '{name_book}' возвращена в библиотеку")
                        else:
                            print("\n У студента нет такой книги!")

                    elif answer == "0":  # ВЫХОД
                        print("\n Выход из библиотеки")
                        return

                    else:
                        print("\n Неверный ввод! Выберите 1, 2 или 0")

        if not student_found:
            print(f"\n Студент {name} {surname} не найден!")

    def new_book(self):
        self.library.new_book()

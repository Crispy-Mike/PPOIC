from Global_variables import DAYS, TIME_OF_CLASSES


class Student:
    def __init__(self, name, surname, group, specialty):
        self.name = name
        self.surname = surname
        self.group = group
        self.specialty = specialty
        self.educational_materials = []
        self.exams = []
        self.books = []
        self.schedule = {}
        self.visits = {}
        self.marks = {}
        self.marks_of_materials={}

    def get_information(self):
        print("-" * 100)
        print(f"{self.name} {self.surname}, группа: {self.group}, специальность: {self.specialty}")
        print("-" * 100)

        print("\nРАСПИСАНИЕ ЗАНЯТИЙ:")
        print("-" * 30)

        for day in DAYS:
            print(f"\n{day}:")
            print("-" * 20)

            day_schedule = self.schedule.get(day, ["-"] * len(TIME_OF_CLASSES))
            for time, subject in zip(TIME_OF_CLASSES, day_schedule):
                if subject != "-":
                    print(f"{time:15} - {subject}")
                else:
                    print(f"{time:15} - нет пары")

        if self.exams:
            print("\nЭКЗАМЕНЫ:")
            print("-" * 30)
            for index, exam in enumerate(self.exams, 1):
                print(f"{index}. {exam}")
        else:
            print("\nЭкзамены: нет назначенных экзаменов")

        if self.educational_materials:
            print("\nУЧЕБНЫЕ МАТЕРИАЛЫ:")
            print("-" * 30)
            for index, material in enumerate(self.educational_materials, 1):
                print(f"{index}. {material}")
        else:
            print("\nУчебные материалы: отсутствуют")

        if self.books:
            print("\n📚 КНИГИ У СТУДЕНТА:")
            print("-" * 30)
            for index, book in enumerate(self.books, 1):
                print(f"{index}. {book.name_of_book} - {book.name_of_author} ({book.genre})")
        else:
            print("\nКниги: нет взятых книг")

    def get_schedule(self):
        print("\nРАСПИСАНИЕ ЗАНЯТИЙ:")
        print("-" * 30)

        for day in DAYS:
            print(f"\n{day}:")
            print("-" * 20)

            day_schedule = self.schedule.get(day, ["-"] * len(TIME_OF_CLASSES))
            for time, subject in zip(TIME_OF_CLASSES, day_schedule):
                if subject != "-":
                    print(f"{time:15} - {subject}")
                else:
                    print(f"{time:15} - нет пары")

    def new_visit(self):

        self.get_schedule()


        for day in DAYS:

            if day not in self.schedule:
                print(f"\n Нет расписания на {day}")
                input("Нажмите Enter для продолжения...")
                continue


            day_schedule = self.schedule[day]

            day_visit = []


            for class_day in day_schedule:

                if class_day == "-":
                    day_visit.append("нет пары")
                    continue

                else:
                    while True:
                        print(f"\n Предмет: {class_day}")
                        print(f" Студент: {self.name} {self.surname}")
                        answer = input("Был на паре? (1-да, 2-нет): ").strip()

                        if answer in ["1", "да"]:
                            day_visit.append("+")
                            print(" Отмечено: был")
                            break

                        elif answer in ["2", "нет"]:
                            day_visit.append("-")
                            print(" Отмечено: не был")
                            break

                        else:
                            print(" Неправильный ввод! Введите 1/да или 2/нет")

            self.visits[day] = day_visit
            print(f" Посещения за {day} сохранены")


        print("\n" + "=" * 50)
        print(" ИТОГОВАЯ СТАТИСТИКА ПОСЕЩАЕМОСТИ:")
        print("=" * 50)
        self.get_visit()

    def get_visit(self):
        max_visits = 0
        absences = 0
        visits = 0

        for day in DAYS:
            print(f"\n{day}:")
            print("-" * 20)

            day_visit = self.visits.get(day, ["-"] * len(TIME_OF_CLASSES))
            day_schedule = self.schedule.get(day, ["-"] * len(TIME_OF_CLASSES))

            for index, (time, subject) in enumerate(zip(TIME_OF_CLASSES, day_schedule)):
                if subject != "-":
                    print(f"{time:15} - {subject}")
                    max_visits += 2

                    if index < len(day_visit):
                        if day_visit[index] == "+":
                            print(f"{'Был':>20}")
                            visits += 2
                        elif day_visit[index] == "-":
                            print(f"{'Не был':>20}")
                            absences += 2
                        else:
                            print(f"{'не отмечено':>20}")
                    else:
                        print(f"{'не отмечено':>20}")
                else:
                    print(f"{time:15} - нет пары")

        print("\n" + "=" * 40)
        print("СТАТИСТИКА ПОСЕЩАЕМОСТИ:")
        print("=" * 40)
        print(f"Посещений: {visits} ч.")
        print(f"Пропусков: {absences} ч.")
        print(f"Всего пар: {max_visits} ч.")
        if max_visits > 0:
            print(f"Процент: {(visits / max_visits * 100):.1f}%")

    def new_marks(self):
        if not self.visits:
            print("Сначала расставьте посещения!")
            input("Нажмите Enter...")
            return

        if self.marks:
            while True:
                answer = input("Уже есть оценки. Перезаписать? (1-да, 2-нет): ").strip()
                if answer in ["1", "да"]:
                    break
                elif answer in ["2", "нет"]:
                    return
                else:
                    print("Неправильный ввод! Введите 1 или 2")
        else:
            print("Ставим новые оценки...")

        self.get_visit()

        for day in DAYS:
            day_schedule = self.schedule.get(day, [])
            day_visit = self.visits.get(day, [])

            if not day_schedule or not day_visit:
                continue

            day_mark = ["-"] * len(TIME_OF_CLASSES)

            for index, class_day in enumerate(day_schedule):
                if day_visit[index] != "+":
                    continue

                while True:
                    ans = input(f"Урок '{class_day}' ({TIME_OF_CLASSES[index]}): отметка? (1-да, 2-нет): ").strip()
                    if ans in ["1", "да"]:
                        while True:
                            try:
                                mark = int(input("Отметка (1-10): ").strip())
                                if 1 <= mark <= 10:
                                    day_mark[index] = mark
                                    print(f"Поставлено: {mark}")
                                    break
                                print("Только 1-10!")
                            except ValueError:
                                print("Введите число!")
                        break
                    elif ans in ["2", "нет"]:
                        break
                    else:
                        print("Введите 1 (да) или 2 (нет)!")

            self.marks[day] = day_mark

        print("\n Оценки сохранены!")
        self.get_marks()

    def get_marks(self):
        if not self.marks:
            print("Оценки не расставлены")
            return

        for day, day_marks in self.marks.items():
            print(f"{day}:")
            schedule = self.schedule.get(day, [])
            for i, (subject, mark) in enumerate(zip(schedule, day_marks)):
                print(f"  {i + 1:2d}. {subject:<15} | {mark}")
            print()

    def exam_check(self):
        self.marks_of_materials = {}
        for material in self.educational_materials:
            self.marks_of_materials[material] = []

        for day in DAYS:
            day_marks = self.marks.get(day, [])
            day_schedule = self.schedule.get(day, [])

            for subject, mark in zip(day_schedule, day_marks):
                if subject in self.educational_materials:
                    if mark != "-":
                        self.marks_of_materials[subject].append(mark)

        print("\n" + "=" * 50)
        print("Оценки:")
        print("=" * 50)

        for material in self.educational_materials:
            marks = self.marks_of_materials.get(material, [])
            if marks:
                avg = sum(marks) / len(marks)
                print(f" {material}:")
                print(f"   Оценки: {marks}")
                print(f"   Средний балл: {avg:.2f}")
                print(f"   Количество оценок: {len(marks)}")
                if avg < 8:
                    print("Средний балл ниже 8. Рекомендуется подготовиться к экзамену!")
            else:
                print(f" {material}: нет оценок")
            print()


        return self.marks_of_materials



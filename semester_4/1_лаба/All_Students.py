from Student import Student
from helpers import check_1, select_week_for_attendance

DAYS = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]

class All_Students:
    def __init__(self):
        self.all_students = []

    def new_student(self):
        name = input("Имя: ")
        surname = input("Фамилия: ")
        number_of_group = int(input("Номер группы: "))

        student = Student(name, surname, number_of_group)
        student.materials = check_1("предмет")
        student.exams = check_1("экзамен")
        marks_of_materials = {}
        for x in student.materials:
            mark = int(input(f"какая средняя оценка по предмету \"{x}\""))
            marks_of_materials[x] = mark
        student.marks_of_materials = marks_of_materials

        raspisanie = {}
        classes_per_week = 0
        classes = ["8.30-9.55",
                   "10.05-11.30",
                   "12.00-13.25",
                   "13.35-15.00",
                   "15.30-16.55"
                   "17.05-18.30"
                   "18.45-19.10"
                   "19.25-20.50"
                   "21.00-22.20"]
        for x in DAYS:
            while True:
                print("\n" * 50)
                answer_1 = input(f"Есть ли занятия в {x}(Да\Нет)")
                if answer_1 == "Да":
                    while True:
                        rasp_day = ["-"] * 9
                        print("\n" * 50)
                        answer_2 = int(input(f"Сколько занятий в {x}"))
                        if 1 <= answer_2 <= 9:
                            classes_per_week += answer_2
                            for y in range(answer_2):
                                for index,classe in enumerate(classes,start=1):
                                    print(f"{index}. ({classe})")
                                time_answer = int(input("Ваш выбор: "))
                                print("\n" * 50)
                                print("Теперь выберите предмет")
                                for index, material in enumerate(student.materials, start=1):
                                    print(f"{index}. {material}")
                                material_answer = int((input(f"Ваш выбор(1-{len(student.materials)}):")))
                                if rasp_day[time_answer] == "-":
                                    rasp_day[time_answer] = student.materials[material_answer - 1]
                            break
                        else:
                            print("Неверный ответ (должно быть в пределах 2-7 пар)")
                            o = input("Введите \"Enter\" чтобы продолжить")
                    raspisanie[x] = rasp_day
                    break
                elif answer_1 == "Нет":
                    raspisanie[x] = "-"
                    break
                else:
                    print("Вы ввели неправильный ответ")
                    o = input("Введите \"Enter\" чтобы продолжить")
        student.raspisanie = raspisanie
        student.classes_per_week = classes_per_week


        self.all_students.append(student)

    def visit_operation(self, name, surname):


        classes = ["8.30-9.55", "10.05-11.30", "12.00-13.25",
                   "13.35-15.00", "15.30-16.55", "17.05-18.30",
                   "18.45-19.10", "19.25-20.50", "21.00-22.20"]

        student = None
        for s in self.all_students:
            if s.name == name and s.surname == surname:
                student = s
                break

        print(f"\n{'='*50}")
        print(f"---Заполнение посещаемости---")
        print(f"Студент: {student.name} {student.surname}")
        print(f"Группа: {student.number_of_group}")
        print(f"{'-'*25}\n")

        if not student.attendance:
            student.attendance = {}
        week_key = select_week_for_attendance()

        if week_key in student.attendance:
            print(f"\nВнимание! Неделя {week_key} уже заполнена.")
            print("Что вы хотите сделать?")
            print("1. Просмотреть текущие данные")
            print("2. Перезаписать данные")
            print("3. Выбрать другую неделю")

            choice= input("Ваш выбор (1-3): ").strip()
            if choice == "1":
                self.view_attendance(name, surname, week_key)
                return
            elif choice == "3":
                week_key = self.select_week_for_attendance()
        else:




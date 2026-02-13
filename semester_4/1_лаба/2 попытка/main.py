from All_Students import All_Students


def main():
    all_students = All_Students()

    while True:
        print("\n" * 50)
        print("Добро пожаловать в модель Студента")
        print("Выберите пункт, который вам нужен:")
        print("1. Операция посещения занятий")
        print("2. Операция изучения материалов")
        print("3. Операция подготовки к экзаменам")
        print("4. Операция учебного планирования")
        print("5. Операция использования библиотечных ресурсов")
        print("6. Сохранить данные")
        print("7. Добавление нового студента")
        print("8. Удаление студента")
        print("9. Редактирование студента")
        print("10. Добавление книг в библиотеку")
        print("11. Очистить данные")
        print("12. Выход")
        print(f"Количество студентов {len(all_students.students)}")

        choice = input("Ваш выбор(1-12): ").strip()

        actions = {
            "1": all_students.visit_of_last_week,
            "2": all_students.material_study_operation,
            "3": all_students.exam_preparation_operation,
            "4": all_students.curricular_planning_operation,
            "5": all_students.operation_of_using_library_resources,
            "6": lambda: [all_students.save_data(), input("Нажмите Enter...")],
            "7": all_students.new_student,
            "8": all_students.delete_student,
            "9": all_students.redact_student,
            "10": all_students.new_book,
            "11": lambda: confirm_clear(all_students)
        }

        if choice == "12":
            print("Выход из программы")
            break
        elif choice in actions:
            try:
                actions[choice]()
                input("Нажмите Enter для продолжения...")
            except Exception as e:
                print(f"Ошибка: {e}")
                input("Нажмите Enter...")
        else:
            print("Неверный выбор!")
            input("Нажмите Enter для продолжения...")


def confirm_clear(all_students):
    confirm = input("Вы уверены, что хотите УДАЛИТЬ ВСЕ ДАННЫЕ? (да/нет): ").strip()
    if confirm.lower() in ["да", "1"]:
        all_students.clear_data()
    else:
        print("Очистка отменена")


if __name__=="__main__":
    main()
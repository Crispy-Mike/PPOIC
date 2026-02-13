DAYS = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]

def check_1(name: str):
    massive = []
    quan_of = int(input(f"Количество {name}ов: "))
    for x in range(quan_of):
        while True:
            check = False
            material = input("Введи предмет: ")

            for y in massive:
                if material == y:
                    check = True
                    break
            if not check:
                massive.append(material)
                break
    return massive

def date_check(data):
    try:
        parts=data.split('.')
        if len(parts)!=3:
            return False

        day,month,year=parts

        if not(day.isdigit() and month.isdigit() and year.isdigit()):
            return False

        day_int=int(day)
        month_int=int(month)
        year_int=int(year)

        if not (1<=day_int<=31 and 1<=month_int<=12 and 2000<=year_int<=2026):
            return False
        return True
    except:
        return False


def select_week_for_attendance():
    while True:
        print("\nВыбирете(1-3):")
        print("1. Ввести дату понедельника недели")

        choice = input("Ваш ответ: ").strip()

        if choice == "1":
            while True:
                date_of_monday = input("Введите дату Пн (Пример: 21.07.2007): ")
                if date_check(date_of_monday):
                    print(f"\nВыбрана неделя, начинающаяся с: {date_of_monday}")
                    return date_of_monday
                else:
                    print("Вы неправильно ввели дату, введити её заново")
                    ch = input("Нажмите \"Enter\" для продолжение")
                    print("\n" * 50)

def view_attendance(week_key,student):
    print("-"*80)
    print(f"Посещаемость студента: {student.name} {student.surname}")
    print(f"Неделя с: {week_key}")
    print("-"*80)
    for day in DAYS:
        print(f"{day:<12}",end="")
        print("\n"+"-"*len(DAYS)*12)



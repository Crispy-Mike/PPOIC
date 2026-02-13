import os
from All_Students import All_Students

def main():
    vuz=VUZ()


    while True:
        os.system('cls')
        print("\n" * 50)
        print("---Лаба_1---")
        print("Выберите, что вам нужно:")
        print("1. Создать нового студента")
        print("2. Создать учебный материал")
        print("3. Создать расписание")
        print("4. Изменение библиотеки")
        print("5. Сохранить данные")
        print("6. Подготовка к экзамену")
        print("7. Выйти")
        answer=int (input("Ваш ответ: "))

        if answer==1:
            All_Students.new_student()
        elif answer==2:

        elif answer==3:
            pass
        elif answer==4:
            pass
        elif answer==5:
            pass
        elif answer==5:
            pass
        elif answer==5:
            pass
        elif answer==5:
            pass
        else:
            print("Вы ввели неправильный ответ, поэтому введите ещё раз:")
            c=input("Нажмите \"Enter\" для продолжения")

if __name__=="__main__":
    main()
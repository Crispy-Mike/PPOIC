from algoritm_Markova import Algoritm_Markova



def main():
    algo = Algoritm_Markova()

    while True:
        print("=" * 50)
        print("ИНТЕРФЕЙС АЛГОРИТМА МАРКОВА")
        print("=" * 50)
        print("1. Добавить правило")
        print("2. Показать все правила")
        print("3. Выполнить алгоритм")
        print("4. Удалить правило")
        print("5. Удалить ВСЕ правила")
        print("6. Выход")
        print("=" * 50)

        choice = input("Выберите действие (1-6): ").strip()

        if choice == "1":
            algo.input_info()

        elif choice == "2":
            if not algo.rules:
                print("Правил нет!")
            else:
                algo.get_info()

        elif choice == "3":
            if not algo.rules:
                print("Сначала добавьте правила!")
                continue

            input_string = input("Введите строку для обработки: ")
            result = algo.main_algoritm(input_string)
            print(f"РЕЗУЛЬТАТ: '{result}'")

        elif choice == "4":
            algo.delete_rule()

        elif choice == "5":
            if not algo.rules:
                print("Правил и так нет!")
                continue

            confirm = input("Вы уверены? (да/нет): ").lower()
            if confirm == "да":
                algo.clear_all_rules()

        elif choice == "6":
            print("До свидания!")
            break

        else:
            print("Неверный выбор!")

        input("Нажмите Enter чтобы продолжить...")


if __name__ == "__main__":
    main()
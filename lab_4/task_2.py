from ui import test_graph, interactive_mode

def main():
    print("Выберите режим работы:")
    print("1. Тестирование графа")
    print("2. Интерактивный режим")

    choice = input("Ваш выбор (1-2): ").strip()

    if choice == "1":
        test_graph()
    elif choice == "2":
        interactive_mode()
    else:
        print("Неверный выбор! Запускаю тестирование.")
        test_graph()

if __name__ == "__main__":
    main()
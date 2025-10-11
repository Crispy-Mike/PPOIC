import sys
from Tag_Game import Tag_Game

def main():
    print("Добро пожаловать в игру \"Пятнашки\"")
    while True:
        show_menu()
        try:
            choice = int(input("Выберите один из подходящих для вас вариантов (1-3): "))
            if choice not in [1, 2, 3]:
                print("Выберите число от 1 до 3!")
                continue
        except ValueError:
            print("Нужно ввести число")
            continue

        match choice:
            case 1:
                rules()
            case 2:
                game_instance = Tag_Game()
                game(game_instance)
            case 3:
                print("Спасибо за игру!")
                sys.exit(0)

def show_menu():
    print("=" * 30)
    print("         МЕНЮ ИГРЫ")
    print("=" * 30)
    print("1. Правила игры")
    print("2. Начать игру")
    print("3. Выход")
    print("=" * 30)

def rules():
    print("\n📖 ПРАВИЛА ИГРЫ:")
    print("Цель игры - расставить числа по порядку")
    print("от 1 до 15, оставив пустую клетку в правом нижнем углу.")
    print("Используйте стрелки или WASD для перемещения клеток.")
    input("Нажмите Enter чтобы вернуться в меню...")

def print_board(board):
    size = len(board)
    print("\n" + "=" * (size * 3))
    for x in range(size):
        row = []
        for num in board[x]:
            if num != 0:
                row.append(f"{num:2d}")
            else:
                row.append("  ")
        print(" | ".join(row))
        if x < size - 1:
            print("-" * (size * 4 - 1))
    print("=" * (size * 3))

def game(game_instance):
    game_instance.create_board()
    while True:
        print("\nВыбери вариант:")
        print("W/S/D/A - ход (введи символ)")
        print("1. Пересоздание карты")
        print("2. Выход в меню")
        print_board(game_instance.get_board())

        choice = input("Твой ход: ").strip().lower()

        if choice not in ["1", "2", "w", "a", "s", "d"]:
            print("Выберите W/A/S/D, 1 или 2!")
            continue

        if choice in ["w", "a", "s", "d"]:
            if game_instance.move(choice):
                if game_instance.check_win():
                    print("Наливай, победа!")
                    input("Нажмите Enter чтобы вернуться в меню...")
                    return True
            else:
                print("Невозможный ход")

        elif choice == "1":
            game_instance.create_board()
            print("Доска пересоздана!")

        elif choice == "2":
            print("Ты всё равно победитель :)")
            return False

if __name__ == "__main__":
    main()
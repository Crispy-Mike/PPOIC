class Algoritm_Markova:
    def __init__(self):
        self.__first = ""
        self.__second = ""
        self.rules = []
        self.__terminal = False

    def input_info(self):
        self.__first = input("Введи на что нужно обратить внимание: ")
        self.__second = input("Введи на что нужно заменить предыдущее: ")
        terminal_input = input("Введи будет ли правило учитываться (Да/Нет): ").lower()
        self.__terminal = terminal_input == "да"

        self.rules.append((self.__first, self.__second, self.__terminal))
        print(f"Правило добавлено:{self.__first}->{self.__second}  ({self.__terminal})")

    def get_info(self):
        for i, x in enumerate(self.rules, 1):
            print(f"{i}. {x[0]}->{x[1]}  ({x[2]})")

    def main_algoritm(self, string: str):
        result = string
        for rule in self.rules:
            pattern, replacement, terminal = rule
            if terminal:
                result = result.replace(pattern, replacement)
        return result

    def delete_rule(self):
        if not self.rules:
            print("Правил нет!")
            return

        self.get_info()
        try:
            index = int(input("Введите номер правила для удаления: ")) - 1
            if 0 <= index < len(self.rules):
                deleted_rule = self.rules.pop(index)
                print(f"Правило удалено: {deleted_rule[0]} -> {deleted_rule[1]}")
            else:
                print("Неверный номер правила!")
        except:
            print("Ошибка ввода!")

    def clear_all_rules(self):
        self.rules.clear()
        print("Все правила удалены!")
class Algoritm_Markova:
    def __init__(self):
        self.__first = ""
        self.__second = ""
        self.rules = []
        self.__terminal = False

    def input_info(self):
        try:
            self.__first = input("Введи на что нужно обратить внимание: ")
            self.__second = input("Введи на что нужно заменить предыдущее: ")
            terminal_input = input("Введи будет ли правило учитываться (Да/Нет): ").lower()
            self.__terminal = terminal_input == "да"

            self.rules.append((self.__first, self.__second, self.__terminal))
            print(f"Правило добавлено:{self.__first}->{self.__second}  ({self.__terminal})")
        except Exception as e:
            print(f"Ошибка при вводе правила: {e}")

    def get_info(self):
        for i, x in enumerate(self.rules, 1):
            print(f"{i}. {x[0]}->{x[1]}  ({x[2]})")

    def main_algoritm(self, string: str):
        result = string
        applied_rule = True

        while applied_rule:
            applied_rule = False
            for pattern, replacement, terminal in self.rules:
                # Ищем первое вхождение паттерна
                pos = result.find(pattern)
                if pos != -1:
                    # Заменяем только первое вхождение
                    result = result[:pos] + replacement + result[pos + len(pattern):]
                    applied_rule = True

                    # Если правило терминальное - выходим сразу
                    if terminal:
                        return result
                    break  # Прерываем цикл после первого применения правила

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
        except Exception as e:
            print(f"Ошибка при удалении правила: {e}")

    def clear_all_rules(self):
        self.rules.clear()
        print("Все правила удалены!")
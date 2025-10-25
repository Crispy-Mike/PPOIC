from graph import DirectedGraph
import sys


def automatic_demo():
    """Автоматическая демонстрация работы графа"""
    print("=" * 60)
    print("АВТОМАТИЧЕСКАЯ ДЕМОНСТРАЦИЯ ОРИЕНТИРОВАННОГО ГРАФА")
    print("=" * 60)

    # Создаем граф с целыми числами
    graph = DirectedGraph[int]()

    print("1. Добавление вершин:")
    vertices = []
    for i in range(5):
        vertex_id = graph.add_vertex(i * 10)
        vertices.append(vertex_id)
        print(f"   Добавлена вершина {vertex_id} с данными {i * 10}")

    print(f"\n   Всего вершин: {graph.vertex_count()}")

    print("\n2. Добавление рёбер:")
    edges = [
        (vertices[0], vertices[1]),
        (vertices[0], vertices[2]),
        (vertices[1], vertices[3]),
        (vertices[2], vertices[3]),
        (vertices[3], vertices[4]),
        (vertices[4], vertices[0])  # Цикл
    ]

    for from_v, to_v in edges:
        graph.add_edge(from_v, to_v)
        print(f"   Добавлено ребро: {from_v} -> {to_v}")

    print(f"\n   Всего рёбер: {graph.edge_count()}")

    print("\n3. Степени вершин:")
    for vertex in vertices:
        out_deg, in_deg = graph.vertex_degree(vertex)
        data = graph.get_vertex_data(vertex)
        print(f"   Вершина {vertex} (данные: {data}): исходящая степень={out_deg}, входящая степень={in_deg}")

    print("\n4. Обход графа:")
    print("   Вершины:", list(graph.vertices()))
    print("   Рёбра:", list(graph.edges()))

    print("\n5. Смежные вершины:")
    for vertex in vertices:
        adjacent = list(graph.adjacent_vertices(vertex))
        print(f"   Смежные с {vertex}: {adjacent}")

    print("\n6. Удаление вершины и ребра:")
    removed_vertex = vertices[2]
    graph.remove_vertex(removed_vertex)
    print(f"   Удалена вершина {removed_vertex}")
    print(f"   Осталось вершин: {graph.vertex_count()}, рёбер: {graph.edge_count()}")

    # Демонстрация с пользовательским типом
    print("\n" + "=" * 60)
    print("ДЕМОНСТРАЦИЯ С ПОЛЬЗОВАТЕЛЬСКИМ ТИПОМ ДАННЫХ")
    print("=" * 60)

    class Person:
        def __init__(self, name: str, age: int):
            self.name = name
            self.age = age

        def __str__(self):
            return f"Person({self.name}, {self.age})"

        def __eq__(self, other):
            if not isinstance(other, Person):
                return False
            return self.name == other.name and self.age == other.age

    person_graph = DirectedGraph[Person]()

    p1 = person_graph.add_vertex(Person("Alice", 25))
    p2 = person_graph.add_vertex(Person("Bob", 30))
    p3 = person_graph.add_vertex(Person("Charlie", 35))

    person_graph.add_edge(p1, p2)
    person_graph.add_edge(p2, p3)
    person_graph.add_edge(p1, p3)

    print("Граф с персонами:")
    for vertex in person_graph.vertices():
        person_data = person_graph.get_vertex_data(vertex)
        print(f"   Вершина {vertex}: {person_data}")


def interactive_mode():
    """Интерактивный режим работы с графом"""
    graph = DirectedGraph[int]()

    while True:
        print("\n" + "=" * 40)
        print("ИНТЕРАКТИВНЫЙ РЕЖИМ РАБОТЫ С ГРАФОМ")
        print("=" * 40)
        print("1. Добавить вершину")
        print("2. Добавить ребро")
        print("3. Удалить вершину")
        print("4. Удалить ребро")
        print("5. Показать граф")
        print("6. Информация о вершине")
        print("7. Обход графа")
        print("8. Очистить граф")
        print("0. Выход")

        choice = input("\nВыберите действие: ").strip()

        if choice == '1':
            try:
                data = int(input("Введите данные вершины (целое число): "))
                vertex_id = graph.add_vertex(data)
                print(f"Добавлена вершина с ID: {vertex_id}")
            except ValueError:
                print("Ошибка: введите целое число!")

        elif choice == '2':
            try:
                from_v = int(input("Введите исходную вершину: "))
                to_v = int(input("Введите целевую вершину: "))
                if graph.add_edge(from_v, to_v):
                    print("Ребро успешно добавлено")
                else:
                    print("Ошибка: не удалось добавить ребро (вершины не существуют или ребро уже есть)")
            except ValueError:
                print("Ошибка: введите целые числа!")

        elif choice == '3':
            try:
                vertex = int(input("Введите ID вершины для удаления: "))
                if graph.remove_vertex(vertex):
                    print("Вершина успешно удалена")
                else:
                    print("Ошибка: вершина не существует")
            except ValueError:
                print("Ошибка: введите целое число!")

        elif choice == '4':
            try:
                from_v = int(input("Введите исходную вершину: "))
                to_v = int(input("Введите целевую вершину: "))
                if graph.remove_edge(from_v, to_v):
                    print("Ребро успешно удалено")
                else:
                    print("Ошибка: ребро не существует")
            except ValueError:
                print("Ошибка: введите целые числа!")

        elif choice == '5':
            print("\nТЕКУЩЕЕ СОСТОЯНИЕ ГРАФА:")
            print(graph)

        elif choice == '6':
            try:
                vertex = int(input("Введите ID вершины: "))
                if graph.has_vertex(vertex):
                    data = graph.get_vertex_data(vertex)
                    out_deg, in_deg = graph.vertex_degree(vertex)
                    print(f"Вершина {vertex}:")
                    print(f"  Данные: {data}")
                    print(f"  Исходящая степень: {out_deg}")
                    print(f"  Входящая степень: {in_deg}")
                    print(f"  Смежные вершины: {list(graph.adjacent_vertices(vertex))}")
                else:
                    print("Ошибка: вершина не существует")
            except ValueError:
                print("Ошибка: введите целое число!")

        elif choice == '7':
            print("\nОБХОД ГРАФА:")
            print(f"Вершины: {list(graph.vertices())}")
            print(f"Рёбра: {list(graph.edges())}")
            print(f"Обратный обход вершин: {list(graph.vertices_reverse())}")

        elif choice == '8':
            graph.clear()
            print("Граф очищен")

        elif choice == '0':
            break

        else:
            print("Неверный выбор! Попробуйте снова.")


def main():
    """Главная функция"""
    print("ЛАБОРАТОРНАЯ РАБОТА: ОРИЕНТИРОВАННЫЙ ГРАФ")
    print("(Модифицированная структура Вирта)")

    while True:
        print("\n" + "=" * 40)
        print("ГЛАВНОЕ МЕНЮ")
        print("=" * 40)
        print("1. Автоматическая демонстрация")
        print("2. Интерактивный режим")
        print("3. Запуск юнит-тестов")
        print("0. Выход")

        choice = input("\nВыберите режим: ").strip()

        if choice == '1':
            automatic_demo()

        elif choice == '2':
            interactive_mode()

        elif choice == '3':
            print("\nЗАПУСК ЮНИТ-ТЕСТОВ...")
            import subprocess
            import sys
            subprocess.run([sys.executable, "-m", "unittest", "test_graph.py"])

        elif choice == '0':
            print("Выход из программы.")
            break

        else:
            print("Неверный выбор! Попробуйте снова.")


if __name__ == "__main__":
    main()
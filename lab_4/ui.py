from DirectedGraph import DirectedGraph
from graph_utils import create_auto_graph, create_manual_graph

def test_graph():
    print("=" * 50)
    print("ТЕСТИРОВАНИЕ НАПРАВЛЕННОГО ГРАФА")
    print("=" * 50)

    print("\nВыберите режим:")
    print("1. Автоматическое создание графа")
    print("2. Ручное создание графа")

    mode = input("Ваш выбор (1-2): ").strip()

    if mode == "1":
        graph = create_auto_graph()
    elif mode == "2":
        graph = create_manual_graph()
    else:
        print("Неверный выбор! Использую автоматический режим.")
        graph = create_auto_graph()

    print("\n" + "=" * 50)
    print("СОЗДАННЫЙ ГРАФ:")
    print("=" * 50)
    print(graph)

    print("Количество вершин:", graph.vertex_count())
    print("Количество ребер:", graph.edge_count())

    if graph.vertex_count() > 0:
        print("Исходящая степень вершины 0:", graph.out_degree(0))
        print("Входящая степень вершины 0:", graph.in_degree(0))

    print("\nВсе вершины:")
    for vertex in graph.vertices_iter():
        print(f"Вершина {vertex}: {graph.get_vertex_data(vertex)}")

    print("\nВсе ребра:")
    for from_v, to_v in graph.edges_iter():
        print(f"Ребро: {from_v} -> {to_v}")

    if graph.vertex_count() > 0:
        print("\nИсходящие из вершины 0:")
        for neighbor in graph.outgoing_iter(0):
            print(f"  -> {neighbor}")

        print("\nВходящие в вершину 0:")
        for neighbor in graph.incoming_iter(0):
            print(f"  <- {neighbor}")

def interactive_mode():
    graph = DirectedGraph()

    while True:
        print("\n" + "=" * 30)
        print("ИНТЕРАКТИВНЫЙ РЕЖИМ")
        print("=" * 30)
        print("1. Добавить вершину")
        print("2. Добавить ребро")
        print("3. Удалить вершину")
        print("4. Удалить ребро")
        print("5. Показать граф")
        print("6. Информация о графе")
        print("7. Выход")

        choice = input("Выберите действие (1-7): ").strip()

        if choice == "1":
            data = input("Введите данные для вершины: ").strip()
            vertex_id = graph.add_vertex(data)
            print(f"Добавлена вершина {vertex_id}")

        elif choice == "2":
            if graph.vertex_count() == 0:
                print("Нет вершин!")
                continue

            print("Доступные вершины:")
            for i in range(graph.vertex_count()):
                print(f"{i}: {graph.get_vertex_data(i)}")

            try:
                from_v = int(input("Исходная вершина: "))
                to_v = int(input("Целевая вершина: "))

                if graph.has_vertex(from_v) and graph.has_vertex(to_v):
                    graph.add_edge(from_v, to_v)
                    print("Ребро добавлено")
                else:
                    print("Неверные вершины!")

            except ValueError:
                print("Введите числа!")

        elif choice == "3":
            if graph.vertex_count() == 0:
                print("Нет вершин!")
                continue

            try:
                vertex = int(input("Номер вершины для удаления: "))
                if graph.has_vertex(vertex):
                    graph.remove_vertex(vertex)
                    print("Вершина удалена")
                else:
                    print("Неверный номер!")

            except ValueError:
                print("Введите число!")

        elif choice == "4":
            if graph.edge_count() == 0:
                print("Нет ребер!")
                continue

            try:
                from_v = int(input("Исходная вершина: "))
                to_v = int(input("Целевая вершина: "))

                if graph.has_edge(from_v, to_v):
                    graph.remove_edge(from_v, to_v)
                    print("Ребро удалено")
                else:
                    print("Ребро не существует!")

            except ValueError:
                print("Введите числа!")

        elif choice == "5":
            print(graph)

        elif choice == "6":
            print(f"Вершин: {graph.vertex_count()}")
            print(f"Ребер: {graph.edge_count()}")

        elif choice == "7":
            break

        else:
            print("Неверный выбор!")
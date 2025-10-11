from DirectedGraph import DirectedGraph

def create_auto_graph():
    graph = DirectedGraph()

    a = graph.add_vertex("A")
    b = graph.add_vertex("B")
    c = graph.add_vertex("C")
    d = graph.add_vertex("D")

    graph.add_edge(a, b)
    graph.add_edge(b, c)
    graph.add_edge(c, a)
    graph.add_edge(a, d)
    graph.add_edge(c, d)

    return graph

def create_manual_graph():
    graph = DirectedGraph()

    print("\nСоздание графа:")
    print("1. Добавить вершины")
    print("2. Добавить рёбра")
    print("3. Завершить создание")

    while True:
        choice = input("\nВыберите действие (1-3): ").strip()

        if choice == "1":
            data = input("Введите данные для вершины: ").strip()
            vertex_id = graph.add_vertex(data)
            print(f"Добавлена вершина {vertex_id} с данными: {data}")

        elif choice == "2":
            if graph.vertex_count() == 0:
                print("Сначала добавьте вершины!")
                continue

            print("Доступные вершины:")
            for i in range(graph.vertex_count()):
                print(f"{i}: {graph.get_vertex_data(i)}")

            try:
                from_v = int(input("Введите номер исходной вершины: "))
                to_v = int(input("Введите номер целевой вершины: "))

                if graph.has_vertex(from_v) and graph.has_vertex(to_v):
                    graph.add_edge(from_v, to_v)
                    print(f"Добавлено ребро: {from_v} -> {to_v}")
                else:
                    print("Неверные номера вершин!")

            except ValueError:
                print("Введите числа!")

        elif choice == "3":
            break

        else:
            print("Неверный выбор!")

    return graph
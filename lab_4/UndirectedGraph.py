class UndirectedGraph:
    def __init__(self):
        self.vertices = []  # Хранит данные вершин
        self.adj_matrix = []  # Матрица смежности

    def add_vertex(self, value):
        """Добавляет вершину и возвращает её ID"""
        self.vertices.append(value)
        for row in self.adj_matrix:
            row.append(0)
        self.adj_matrix.append([0] * len(self.vertices))
        return len(self.vertices) - 1  # Возвращаем ID новой вершины

    def add_edge(self, i, j):
        if 0 <= i < len(self.vertices) and 0 <= j < len(self.vertices):
            self.adj_matrix[i][j] = 1
            self.adj_matrix[j][i] = 1

    def remove_vertex(self, vertex_id):
        """Удаляет вершину по ID"""
        if 0 <= vertex_id < len(self.vertices):
            # Удаляем строку и столбец из матрицы смежности
            del self.adj_matrix[vertex_id]
            for row in self.adj_matrix:
                del row[vertex_id]
            del self.vertices[vertex_id]

    def remove_edge(self, i, j):
        if 0 <= i < len(self.vertices) and 0 <= j < len(self.vertices):
            self.adj_matrix[i][j] = 0
            self.adj_matrix[j][i] = 0

    def has_vertex(self, vertex_id):
        return 0 <= vertex_id < len(self.vertices)

    def has_edge(self, i, j):
        if 0 <= i < len(self.vertices) and 0 <= j < len(self.vertices):
            return self.adj_matrix[i][j] == 1
        return False

    def vertex_count(self):
        return len(self.vertices)

    def edge_count(self):
        count = 0
        for i in range(len(self.vertices)):
            for j in range(i + 1, len(self.vertices)):  # Учитываем только верхний треугольник
                if self.adj_matrix[i][j] == 1:
                    count += 1
        return count

    def get_vertex_data(self, vertex_id):
        if 0 <= vertex_id < len(self.vertices):
            return self.vertices[vertex_id]
        return None

    # Методы для совместимости с UI
    def vertices_iter(self):
        return range(len(self.vertices))

    def edges_iter(self):
        edges = []
        for i in range(len(self.vertices)):
            for j in range(i + 1, len(self.vertices)):  # Уникальные рёбра
                if self.adj_matrix[i][j] == 1:
                    edges.append((i, j))
        return edges

    def outgoing_iter(self, vertex_id):
        """Для ненаправленного графа исходящие = входящие = все смежные"""
        neighbors = []
        if 0 <= vertex_id < len(self.vertices):
            for j in range(len(self.vertices)):
                if self.adj_matrix[vertex_id][j] == 1:
                    neighbors.append(j)
        return neighbors

    def incoming_iter(self, vertex_id):
        """Для ненаправленного графа входящие = исходящие"""
        return self.outgoing_iter(vertex_id)

    def out_degree(self, vertex_id):
        if 0 <= vertex_id < len(self.vertices):
            return sum(self.adj_matrix[vertex_id])
        return 0

    def in_degree(self, vertex_id):
        """Для ненаправленного графа входящая степень = исходящей"""
        return self.out_degree(vertex_id)

    def __str__(self):
        result = "Граф (ненаправленный):\n"
        result += f"Вершины: {self.vertices}\n"
        result += "Матрица смежности:\n"
        result += "   " + "  ".join(str(i) for i in range(len(self.vertices))) + "\n"
        for i, row in enumerate(self.adj_matrix):
            result += f"{i}: " + "  ".join(str(x) for x in row) + "\n"
        return result
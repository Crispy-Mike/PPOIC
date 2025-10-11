class DirectedGraph:
    class VertexIterator:
        def __init__(self, graph):
            self.graph = graph
            self.index = 0

        def __iter__(self):
            return self

        def __next__(self):
            if self.index >= len(self.graph.vertices):
                raise StopIteration
            result = self.index
            self.index += 1
            return result

        def __prev__(self):
            if self.index <= 0:
                raise StopIteration
            self.index -= 1
            return self.index

    class EdgeIterator:
        def __init__(self, graph):
            self.graph = graph
            self.i = 0
            self.j = 0

        def __iter__(self):
            return self

        def __next__(self):
            while self.i < len(self.graph.matrix):
                while self.j < len(self.graph.matrix):
                    if self.graph.matrix[self.i][self.j]:
                        result = (self.i, self.j)
                        self.j += 1
                        return result
                    self.j += 1
                self.i += 1
                self.j = 0
            raise StopIteration

    class NeighborIterator:
        def __init__(self, graph, vertex, outgoing=True):
            self.graph = graph
            self.vertex = vertex
            self.outgoing = outgoing
            self.index = 0

        def __iter__(self):
            return self

        def __next__(self):
            if self.outgoing:
                while self.index < len(self.graph.matrix):
                    if self.graph.matrix[self.vertex][self.index]:
                        result = self.index
                        self.index += 1
                        return result
                    self.index += 1
            else:
                while self.index < len(self.graph.matrix):
                    if self.graph.matrix[self.index][self.vertex]:
                        result = self.index
                        self.index += 1
                        return result
                    self.index += 1
            raise StopIteration

    def __init__(self):
        self.vertices = []
        self.matrix = []

    def add_vertex(self, data):
        self.vertices.append(data)
        for row in self.matrix:
            row.append(False)
        new_row = [False] * len(self.vertices)
        self.matrix.append(new_row)
        return len(self.vertices) - 1

    def add_edge(self, from_vertex, to_vertex):
        if from_vertex < len(self.matrix) and to_vertex < len(self.matrix):
            self.matrix[from_vertex][to_vertex] = True

    def remove_vertex(self, vertex):
        if vertex >= len(self.vertices):
            return

        del self.vertices[vertex]
        del self.matrix[vertex]

        for row in self.matrix:
            del row[vertex]

    def remove_edge(self, from_vertex, to_vertex):
        if from_vertex < len(self.matrix) and to_vertex < len(self.matrix):
            self.matrix[from_vertex][to_vertex] = False

    def has_vertex(self, vertex):
        return vertex < len(self.vertices)

    def has_edge(self, from_vertex, to_vertex):
        if from_vertex < len(self.matrix) and to_vertex < len(self.matrix):
            return self.matrix[from_vertex][to_vertex]
        return False

    def vertex_count(self):
        return len(self.vertices)

    def edge_count(self):
        count = 0
        for row in self.matrix:
            count += sum(row)
        return count

    def out_degree(self, vertex):
        if vertex < len(self.matrix):
            return sum(self.matrix[vertex])
        return 0

    def in_degree(self, vertex):
        if vertex < len(self.matrix):
            count = 0
            for row in self.matrix:
                if row[vertex]:
                    count += 1
            return count
        return 0

    def get_vertex_data(self, vertex):
        if vertex < len(self.vertices):
            return self.vertices[vertex]
        return None

    def set_vertex_data(self, vertex, data):
        if vertex < len(self.vertices):
            self.vertices[vertex] = data

    def vertices_iter(self):
        return self.VertexIterator(self)

    def edges_iter(self):
        return self.EdgeIterator(self)

    def outgoing_iter(self, vertex):
        return self.NeighborIterator(self, vertex, True)

    def incoming_iter(self, vertex):
        return self.NeighborIterator(self, vertex, False)

    def __str__(self):
        result = "Вершины:\n"
        for i, data in enumerate(self.vertices):
            result += f"  {i}: {data}\n"

        result += "\nМатрица смежности:\n   "
        for i in range(len(self.vertices)):
            result += f"{i} "
        result += "\n"

        for i, row in enumerate(self.matrix):
            result += f"{i}: "
            for val in row:
                result += "1 " if val else "0 "
            result += "\n"

        return result
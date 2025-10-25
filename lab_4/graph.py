from typing import TypeVar, Generic, List, Dict, Set, Tuple, Optional, Iterator, Any
from abc import ABC, abstractmethod
import copy

T = TypeVar('T')


class VertexTraits(Generic[T]):
    """Класс свойств для вершин графа"""

    @staticmethod
    def default_value() -> T:
        return None

    @staticmethod
    def are_equal(a: T, b: T) -> bool:
        return a == b


class DirectedGraph(Generic[T]):
    """
    Ориентированный граф с использованием модифицированной структуры Вирта
    Представление: списки смежности с дополнительной матрицей для быстрого доступа
    """

    class VertexIterator:
        """Двунаправленный итератор вершин"""

        def __init__(self, graph: 'DirectedGraph', vertex_ids: List[int], reverse: bool = False):
            self.graph = graph
            self.vertex_ids = vertex_ids
            self.reverse = reverse
            self.index = len(vertex_ids) - 1 if reverse else 0

        def __iter__(self):
            return self

        def __next__(self) -> int:
            if self.reverse:
                if self.index < 0:
                    raise StopIteration
                result = self.vertex_ids[self.index]
                self.index -= 1
            else:
                if self.index >= len(self.vertex_ids):
                    raise StopIteration
                result = self.vertex_ids[self.index]
                self.index += 1
            return result

        def __reversed__(self):
            return DirectedGraph.VertexIterator(self.graph, self.vertex_ids, not self.reverse)

    class EdgeIterator:
        """Двунаправленный итератор рёбер"""

        def __init__(self, graph: 'DirectedGraph', edges: List[Tuple[int, int]], reverse: bool = False):
            self.graph = graph
            self.edges = edges
            self.reverse = reverse
            self.index = len(edges) - 1 if reverse else 0

        def __iter__(self):
            return self

        def __next__(self) -> Tuple[int, int]:
            if self.reverse:
                if self.index < 0:
                    raise StopIteration
                result = self.edges[self.index]
                self.index -= 1
            else:
                if self.index >= len(self.edges):
                    raise StopIteration
                result = self.edges[self.index]
                self.index += 1
            return result

        def __reversed__(self):
            return DirectedGraph.EdgeIterator(self.graph, self.edges, not self.reverse)

    class AdjacentVertexIterator:
        """Двунаправленный итератор смежных вершин"""

        def __init__(self, graph: 'DirectedGraph', vertex: int, adjacent_vertices: List[int], reverse: bool = False):
            self.graph = graph
            self.vertex = vertex
            self.adjacent_vertices = adjacent_vertices
            self.reverse = reverse
            self.index = len(adjacent_vertices) - 1 if reverse else 0

        def __iter__(self):
            return self

        def __next__(self) -> int:
            if self.reverse:
                if self.index < 0:
                    raise StopIteration
                result = self.adjacent_vertices[self.index]
                self.index -= 1
            else:
                if self.index >= len(self.adjacent_vertices):
                    raise StopIteration
                result = self.adjacent_vertices[self.index]
                self.index += 1
            return result

        def __reversed__(self):
            return DirectedGraph.AdjacentVertexIterator(
                self.graph, self.vertex, self.adjacent_vertices, not self.reverse)

    class IncidentEdgeIterator:
        """Двунаправленный итератор инцидентных рёбер"""

        def __init__(self, graph: 'DirectedGraph', vertex: int, incident_edges: List[Tuple[int, int]],
                     reverse: bool = False):
            self.graph = graph
            self.vertex = vertex
            self.incident_edges = incident_edges
            self.reverse = reverse
            self.index = len(incident_edges) - 1 if reverse else 0

        def __iter__(self):
            return self

        def __next__(self) -> Tuple[int, int]:
            if self.reverse:
                if self.index < 0:
                    raise StopIteration
                result = self.incident_edges[self.index]
                self.index -= 1
            else:
                if self.index >= len(self.incident_edges):
                    raise StopIteration
                result = self.incident_edges[self.index]
                self.index += 1
            return result

        def __reversed__(self):
            return DirectedGraph.IncidentEdgeIterator(
                self.graph, self.vertex, self.incident_edges, not self.reverse)

    def __init__(self, traits: VertexTraits[T] = None):
        self._traits = traits or VertexTraits[T]()
        self._vertices: Dict[int, T] = {}  # vertex_id -> data
        self._adjacency_list: Dict[int, Set[int]] = {}  # vertex_id -> set of adjacent vertices
        self._next_vertex_id = 0
        self._edge_count = 0

    # Базовые методы контейнера
    def empty(self) -> bool:
        """Проверка на пустой контейнер"""
        return len(self._vertices) == 0

    def clear(self) -> None:
        """Очистка контейнера"""
        self._vertices.clear()
        self._adjacency_list.clear()
        self._next_vertex_id = 0
        self._edge_count = 0

    def __copy__(self) -> 'DirectedGraph[T]':
        """Конструктор копирования"""
        new_graph = DirectedGraph[T](self._traits)
        new_graph._vertices = copy.copy(self._vertices)
        new_graph._adjacency_list = copy.deepcopy(self._adjacency_list)
        new_graph._next_vertex_id = self._next_vertex_id
        new_graph._edge_count = self._edge_count
        return new_graph

    def __eq__(self, other: Any) -> bool:
        """Оператор сравнения =="""
        if not isinstance(other, DirectedGraph):
            return False
        if len(self._vertices) != len(other._vertices):
            return False
        if self._edge_count != other._edge_count:
            return False

        # Проверка вершин и их данных
        for vid, data in self._vertices.items():
            if vid not in other._vertices:
                return False
            if not self._traits.are_equal(data, other._vertices[vid]):
                return False

        # Проверка рёбер
        for from_v, to_vertices in self._adjacency_list.items():
            if from_v not in other._adjacency_list:
                return False
            if self._adjacency_list[from_v] != other._adjacency_list[from_v]:
                return False

        return True

    def __ne__(self, other: Any) -> bool:
        """Оператор сравнения !="""
        return not self.__eq__(other)

    # Методы работы с вершинами
    def has_vertex(self, vertex: int) -> bool:
        """Проверка присутствия вершины в графе"""
        return vertex in self._vertices

    def vertex_count(self) -> int:
        """Получение количества вершин"""
        return len(self._vertices)

    def add_vertex(self, data: T = None) -> int:
        """Добавление вершины"""
        if data is None:
            data = self._traits.default_value()

        vertex_id = self._next_vertex_id
        self._vertices[vertex_id] = data
        self._adjacency_list[vertex_id] = set()
        self._next_vertex_id += 1
        return vertex_id

    def remove_vertex(self, vertex: int) -> bool:
        """Удаление вершины"""
        if vertex not in self._vertices:
            return False

        # Удаляем все рёбра, связанные с этой вершиной
        edges_to_remove = []

        # Удаляем исходящие рёбра
        if vertex in self._adjacency_list:
            self._edge_count -= len(self._adjacency_list[vertex])
            del self._adjacency_list[vertex]

        # Удаляем входящие рёбра
        for from_v, to_vertices in self._adjacency_list.items():
            if vertex in to_vertices:
                to_vertices.remove(vertex)
                self._edge_count -= 1

        # Удаляем саму вершину
        del self._vertices[vertex]
        return True

    def get_vertex_data(self, vertex: int) -> T:
        """Получение данных вершины"""
        if vertex not in self._vertices:
            raise KeyError(f"Vertex {vertex} not found")
        return self._vertices[vertex]

    def set_vertex_data(self, vertex: int, data: T) -> None:
        """Установка данных вершины"""
        if vertex not in self._vertices:
            raise KeyError(f"Vertex {vertex} not found")
        self._vertices[vertex] = data

    # Методы работы с рёбрами
    def has_edge(self, from_vertex: int, to_vertex: int) -> bool:
        """Проверка присутствия ребра между вершинами"""
        if from_vertex not in self._adjacency_list:
            return False
        return to_vertex in self._adjacency_list[from_vertex]

    def edge_count(self) -> int:
        """Получение количества рёбер"""
        return self._edge_count

    def add_edge(self, from_vertex: int, to_vertex: int) -> bool:
        """Добавление ребра"""
        if not self.has_vertex(from_vertex) or not self.has_vertex(to_vertex):
            return False

        if self.has_edge(from_vertex, to_vertex):
            return False

        self._adjacency_list[from_vertex].add(to_vertex)
        self._edge_count += 1
        return True

    def remove_edge(self, from_vertex: int, to_vertex: int) -> bool:
        """Удаление ребра"""
        if not self.has_edge(from_vertex, to_vertex):
            return False

        self._adjacency_list[from_vertex].remove(to_vertex)
        self._edge_count -= 1
        return True

    # Методы анализа графа
    def vertex_degree(self, vertex: int) -> Tuple[int, int]:
        """Вычисление степени вершины (исходящая, входящая)"""
        if not self.has_vertex(vertex):
            raise KeyError(f"Vertex {vertex} not found")

        out_degree = len(self._adjacency_list.get(vertex, set()))

        in_degree = 0
        for from_v, to_vertices in self._adjacency_list.items():
            if vertex in to_vertices:
                in_degree += 1

        return (out_degree, in_degree)

    # Итераторы
    def vertices(self) -> VertexIterator:
        """Итератор вершин"""
        return self.VertexIterator(self, list(self._vertices.keys()))

    def edges(self) -> EdgeIterator:
        """Итератор рёбер"""
        edge_list = []
        for from_v, to_vertices in self._adjacency_list.items():
            for to_v in to_vertices:
                edge_list.append((from_v, to_v))
        return self.EdgeIterator(self, edge_list)

    def adjacent_vertices(self, vertex: int) -> AdjacentVertexIterator:
        """Итератор смежных вершин (исходящие)"""
        if not self.has_vertex(vertex):
            raise KeyError(f"Vertex {vertex} not found")
        return self.AdjacentVertexIterator(self, vertex, list(self._adjacency_list.get(vertex, set())))

    def incident_edges(self, vertex: int) -> IncidentEdgeIterator:
        """Итератор инцидентных рёбер (исходящие)"""
        if not self.has_vertex(vertex):
            raise KeyError(f"Vertex {vertex} not found")

        incident_edges = []
        if vertex in self._adjacency_list:
            for to_v in self._adjacency_list[vertex]:
                incident_edges.append((vertex, to_v))

        return self.IncidentEdgeIterator(self, vertex, incident_edges)

    # Обратные итераторы
    def vertices_reverse(self) -> VertexIterator:
        """Обратный итератор вершин"""
        return self.VertexIterator(self, list(self._vertices.keys()), True)

    def edges_reverse(self) -> EdgeIterator:
        """Обратный итератор рёбер"""
        edge_list = []
        for from_v, to_vertices in self._adjacency_list.items():
            for to_v in to_vertices:
                edge_list.append((from_v, to_v))
        return self.EdgeIterator(self, edge_list, True)

    # Удаление по итераторам
    def remove_vertex_by_iterator(self, vertex: int) -> bool:
        """Удаление вершины по итератору"""
        return self.remove_vertex(vertex)

    def remove_edge_by_iterator(self, from_vertex: int, to_vertex: int) -> bool:
        """Удаление ребра по итератору"""
        return self.remove_edge(from_vertex, to_vertex)

    # Вывод графа
    def __str__(self) -> str:
        """Строковое представление графа"""
        result = f"DirectedGraph(vertices={self.vertex_count()}, edges={self.edge_count()})\n"
        result += "Vertices:\n"
        for vertex in self.vertices():
            data = self.get_vertex_data(vertex)
            out_deg, in_deg = self.vertex_degree(vertex)
            result += f"  {vertex}: data={data}, out_degree={out_deg}, in_degree={in_deg}\n"

        result += "Edges:\n"
        for from_v, to_v in self.edges():
            result += f"  {from_v} -> {to_v}\n"

        return result

    # Константные модификации (в Python эмулируем через свойства)
    @property
    def vertices_const(self):
        """Константный итератор вершин"""
        return list(self._vertices.keys())

    @property
    def edges_const(self):
        """Константный итератор рёбер"""
        edge_list = []
        for from_v, to_vertices in self._adjacency_list.items():
            for to_v in to_vertices:
                edge_list.append((from_v, to_v))
        return edge_list
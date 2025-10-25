import unittest
import copy

from graph import DirectedGraph, VertexTraits


class TestDirectedGraph(unittest.TestCase):

    def setUp(self):
        self.graph = DirectedGraph[int]()

    def test_empty_graph(self):
        self.assertTrue(self.graph.empty())
        self.assertEqual(self.graph.vertex_count(), 0)
        self.assertEqual(self.graph.edge_count(), 0)

    def test_add_vertices(self):
        v1 = self.graph.add_vertex(10)
        v2 = self.graph.add_vertex(20)
        v3 = self.graph.add_vertex(30)

        self.assertEqual(self.graph.vertex_count(), 3)
        self.assertFalse(self.graph.empty())
        self.assertTrue(self.graph.has_vertex(v1))
        self.assertTrue(self.graph.has_vertex(v2))
        self.assertTrue(self.graph.has_vertex(v3))

    def test_vertex_data(self):
        v1 = self.graph.add_vertex(100)
        self.assertEqual(self.graph.get_vertex_data(v1), 100)

        self.graph.set_vertex_data(v1, 200)
        self.assertEqual(self.graph.get_vertex_data(v1), 200)

    def test_add_edges(self):
        v1 = self.graph.add_vertex(1)
        v2 = self.graph.add_vertex(2)
        v3 = self.graph.add_vertex(3)

        # Добавление рёбер
        self.assertTrue(self.graph.add_edge(v1, v2))
        self.assertTrue(self.graph.add_edge(v1, v3))
        self.assertTrue(self.graph.add_edge(v2, v3))

        self.assertEqual(self.graph.edge_count(), 3)
        self.assertTrue(self.graph.has_edge(v1, v2))
        self.assertTrue(self.graph.has_edge(v1, v3))
        self.assertTrue(self.graph.has_edge(v2, v3))
        self.assertFalse(self.graph.has_edge(v2, v1))  # Обратное ребро не должно существовать

    def test_remove_edges(self):
        v1 = self.graph.add_vertex(1)
        v2 = self.graph.add_vertex(2)

        self.graph.add_edge(v1, v2)
        self.assertTrue(self.graph.has_edge(v1, v2))

        self.assertTrue(self.graph.remove_edge(v1, v2))
        self.assertFalse(self.graph.has_edge(v1, v2))
        self.assertEqual(self.graph.edge_count(), 0)

    def test_remove_vertices(self):
        v1 = self.graph.add_vertex(1)
        v2 = self.graph.add_vertex(2)
        v3 = self.graph.add_vertex(3)

        self.graph.add_edge(v1, v2)
        self.graph.add_edge(v2, v3)
        self.graph.add_edge(v1, v3)

        self.assertTrue(self.graph.remove_vertex(v2))
        self.assertFalse(self.graph.has_vertex(v2))
        self.assertEqual(self.graph.vertex_count(), 2)
        self.assertEqual(self.graph.edge_count(), 1)  # Осталось только v1 -> v3
        self.assertTrue(self.graph.has_edge(v1, v3))

    def test_vertex_degree(self):
        v1 = self.graph.add_vertex(1)
        v2 = self.graph.add_vertex(2)
        v3 = self.graph.add_vertex(3)

        self.graph.add_edge(v1, v2)
        self.graph.add_edge(v1, v3)
        self.graph.add_edge(v2, v3)
        self.graph.add_edge(v3, v1)

        out_deg, in_deg = self.graph.vertex_degree(v1)
        self.assertEqual(out_deg, 2)  # v1 -> v2, v1 -> v3
        self.assertEqual(in_deg, 1)  # v3 -> v1

        out_deg, in_deg = self.graph.vertex_degree(v3)
        self.assertEqual(out_deg, 1)  # v3 -> v1
        self.assertEqual(in_deg, 2)  # v1 -> v3, v2 -> v3

    def test_vertex_iterator(self):
        vertices = []
        for i in range(5):
            vertices.append(self.graph.add_vertex(i * 10))

        # Прямой итератор
        iterated = list(self.graph.vertices())
        self.assertEqual(iterated, vertices)

        # Обратный итератор
        reversed_iterated = list(self.graph.vertices_reverse())
        self.assertEqual(reversed_iterated, list(reversed(vertices)))

    def test_edge_iterator(self):
        v1 = self.graph.add_vertex(1)
        v2 = self.graph.add_vertex(2)
        v3 = self.graph.add_vertex(3)

        self.graph.add_edge(v1, v2)
        self.graph.add_edge(v2, v3)
        self.graph.add_edge(v1, v3)

        edges = list(self.graph.edges())
        expected_edges = [(v1, v2), (v1, v3), (v2, v3)]
        self.assertEqual(sorted(edges), sorted(expected_edges))

    def test_adjacent_vertices_iterator(self):
        v1 = self.graph.add_vertex(1)
        v2 = self.graph.add_vertex(2)
        v3 = self.graph.add_vertex(3)
        v4 = self.graph.add_vertex(4)

        self.graph.add_edge(v1, v2)
        self.graph.add_edge(v1, v3)
        self.graph.add_edge(v1, v4)

        adjacent = list(self.graph.adjacent_vertices(v1))
        expected_adjacent = [v2, v3, v4]
        self.assertEqual(sorted(adjacent), sorted(expected_adjacent))

    def test_incident_edges_iterator(self):
        v1 = self.graph.add_vertex(1)
        v2 = self.graph.add_vertex(2)
        v3 = self.graph.add_vertex(3)

        self.graph.add_edge(v1, v2)
        self.graph.add_edge(v1, v3)

        incident = list(self.graph.incident_edges(v1))
        expected_incident = [(v1, v2), (v1, v3)]
        self.assertEqual(sorted(incident), sorted(expected_incident))

    def test_copy_and_equality(self):
        v1 = self.graph.add_vertex(1)
        v2 = self.graph.add_vertex(2)
        self.graph.add_edge(v1, v2)

        # Копирование
        graph_copy = copy.copy(self.graph)
        self.assertEqual(self.graph, graph_copy)

        # Изменение копии не должно влиять на оригинал
        graph_copy.set_vertex_data(v1, 100)
        self.assertNotEqual(self.graph, graph_copy)

    def test_clear(self):
        v1 = self.graph.add_vertex(1)
        v2 = self.graph.add_vertex(2)
        self.graph.add_edge(v1, v2)

        self.graph.clear()
        self.assertTrue(self.graph.empty())
        self.assertEqual(self.graph.vertex_count(), 0)
        self.assertEqual(self.graph.edge_count(), 0)


class TestVertexTraits(unittest.TestCase):
    def test_custom_traits(self):
        class StringTraits(VertexTraits[str]):
            @staticmethod
            def default_value():
                return "default"

            @staticmethod
            def are_equal(a, b):
                return a.lower() == b.lower()

        graph = DirectedGraph[str](StringTraits())
        v1 = graph.add_vertex("Hello")
        v2 = graph.add_vertex()  # Использует значение по умолчанию

        self.assertEqual(graph.get_vertex_data(v1), "Hello")
        self.assertEqual(graph.get_vertex_data(v2), "default")

        # Проверка кастомного сравнения
        graph2 = DirectedGraph[str](StringTraits())
        v3 = graph2.add_vertex("HELLO")
        # Графы не равны, так как разные ID вершин, но данные считаются равными по кастомному правилу


if __name__ == '__main__':
    unittest.main()
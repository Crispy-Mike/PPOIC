import unittest
from DirectedGraph import DirectedGraph


class TestDirectedGraph(unittest.TestCase):

    def setUp(self):
        """Настройка перед каждым тестом"""
        self.graph = DirectedGraph()

    def test_init(self):
        """Тест инициализации графа"""
        self.assertEqual(self.graph.vertex_count(), 0)
        self.assertEqual(self.graph.edge_count(), 0)
        self.assertEqual(len(self.graph.vertices), 0)
        self.assertEqual(len(self.graph.matrix), 0)

    def test_add_vertex(self):
        """Тест добавления вершины"""
        vertex_id = self.graph.add_vertex("A")
        self.assertEqual(vertex_id, 0)
        self.assertEqual(self.graph.vertex_count(), 1)
        self.assertEqual(self.graph.get_vertex_data(0), "A")

    def test_add_multiple_vertices(self):
        """Тест добавления нескольких вершин"""
        id1 = self.graph.add_vertex("A")
        id2 = self.graph.add_vertex("B")
        id3 = self.graph.add_vertex("C")

        self.assertEqual(id1, 0)
        self.assertEqual(id2, 1)
        self.assertEqual(id3, 2)
        self.assertEqual(self.graph.vertex_count(), 3)
        self.assertEqual(len(self.graph.matrix), 3)
        self.assertEqual(len(self.graph.matrix[0]), 3)

    def test_add_edge(self):
        """Тест добавления ребра"""
        self.graph.add_vertex("A")
        self.graph.add_vertex("B")
        self.graph.add_edge(0, 1)

        self.assertEqual(self.graph.edge_count(), 1)
        self.assertTrue(self.graph.has_edge(0, 1))
        self.assertTrue(self.graph.matrix[0][1])

    def test_add_edge_multiple(self):
        """Тест добавления нескольких ребер"""
        self.graph.add_vertex("A")
        self.graph.add_vertex("B")
        self.graph.add_vertex("C")
        self.graph.add_edge(0, 1)
        self.graph.add_edge(1, 2)
        self.graph.add_edge(0, 2)

        self.assertEqual(self.graph.edge_count(), 3)
        self.assertTrue(self.graph.has_edge(0, 1))
        self.assertTrue(self.graph.has_edge(1, 2))
        self.assertTrue(self.graph.has_edge(0, 2))

    def test_add_edge_invalid_vertices(self):
        """Тест добавления ребра с несуществующими вершинами"""
        self.graph.add_vertex("A")
        # Попытка добавить ребро к несуществующей вершине
        self.graph.add_edge(0, 5)
        # Не должно быть ошибки, но ребро не должно добавиться
        self.assertFalse(self.graph.has_edge(0, 5))

    def test_remove_vertex_with_edges(self):
        """Тест удаления вершины с ребрами"""
        self.graph.add_vertex("A")
        self.graph.add_vertex("B")
        self.graph.add_vertex("C")
        self.graph.add_edge(0, 1)
        self.graph.add_edge(1, 2)
        self.graph.add_edge(2, 0)

        self.graph.remove_vertex(1)

        self.assertEqual(self.graph.edge_count(), 1)  # Осталось только 2->0
        self.assertTrue(self.graph.has_edge(1, 0))  # Теперь 2 стало 1

    def test_remove_edge(self):
        """Тест удаления ребра"""
        self.graph.add_vertex("A")
        self.graph.add_vertex("B")
        self.graph.add_edge(0, 1)

        self.graph.remove_edge(0, 1)

        self.assertEqual(self.graph.edge_count(), 0)
        self.assertFalse(self.graph.has_edge(0, 1))
        self.assertFalse(self.graph.matrix[0][1])

    def test_remove_edge_invalid(self):
        """Тест удаления несуществующего ребра"""
        self.graph.add_vertex("A")
        self.graph.add_vertex("B")
        # Удаление несуществующего ребра не должно вызывать ошибку
        self.graph.remove_edge(0, 1)
        self.assertFalse(self.graph.has_edge(0, 1))

    def test_has_vertex(self):
        """Тест проверки существования вершины"""
        self.graph.add_vertex("A")

        self.assertTrue(self.graph.has_vertex(0))
        self.assertFalse(self.graph.has_vertex(1))

    def test_has_edge(self):
        """Тест проверки существования ребра"""
        self.graph.add_vertex("A")
        self.graph.add_vertex("B")
        self.graph.add_edge(0, 1)

        self.assertTrue(self.graph.has_edge(0, 1))
        self.assertFalse(self.graph.has_edge(1, 0))
        self.assertFalse(self.graph.has_edge(0, 5))  # Несуществующая вершина

    def test_get_vertex_data(self):
        """Тест получения данных вершины"""
        self.graph.add_vertex("Test Data")

        self.assertEqual(self.graph.get_vertex_data(0), "Test Data")

    def test_get_vertex_data_invalid(self):
        """Тест получения данных несуществующей вершины"""
        self.assertIsNone(self.graph.get_vertex_data(0))

    def test_set_vertex_data(self):
        """Тест установки данных вершины"""
        self.graph.add_vertex("Old Data")
        self.graph.set_vertex_data(0, "New Data")

        self.assertEqual(self.graph.get_vertex_data(0), "New Data")

    def test_set_vertex_data_invalid(self):
        """Тест установки данных несуществующей вершины"""
        # Не должно вызывать ошибку
        self.graph.set_vertex_data(0, "Data")

    def test_vertex_count(self):
        """Тест подсчета вершин"""
        self.assertEqual(self.graph.vertex_count(), 0)

        self.graph.add_vertex("A")
        self.assertEqual(self.graph.vertex_count(), 1)

        self.graph.add_vertex("B")
        self.assertEqual(self.graph.vertex_count(), 2)

    def test_edge_count(self):
        """Тест подсчета ребер"""
        self.assertEqual(self.graph.edge_count(), 0)

        self.graph.add_vertex("A")
        self.graph.add_vertex("B")
        self.graph.add_edge(0, 1)
        self.assertEqual(self.graph.edge_count(), 1)

        self.graph.add_edge(1, 0)
        self.assertEqual(self.graph.edge_count(), 2)

    def test_out_degree(self):
        """Тест исходящей степени"""
        self.graph.add_vertex("A")
        self.graph.add_vertex("B")
        self.graph.add_vertex("C")
        self.graph.add_edge(0, 1)
        self.graph.add_edge(0, 2)

        self.assertEqual(self.graph.out_degree(0), 2)
        self.assertEqual(self.graph.out_degree(1), 0)
        self.assertEqual(self.graph.out_degree(5), 0)  # Несуществующая вершина

    def test_in_degree(self):
        """Тест входящей степени"""
        self.graph.add_vertex("A")
        self.graph.add_vertex("B")
        self.graph.add_vertex("C")
        self.graph.add_edge(0, 1)
        self.graph.add_edge(2, 1)

        self.assertEqual(self.graph.in_degree(1), 2)
        self.assertEqual(self.graph.in_degree(0), 0)
        self.assertEqual(self.graph.in_degree(5), 0)  # Несуществующая вершина

    def test_vertices_iter(self):
        """Тест итератора по вершинам"""
        self.graph.add_vertex("A")
        self.graph.add_vertex("B")
        self.graph.add_vertex("C")

        vertices = list(self.graph.vertices_iter())
        self.assertEqual(vertices, [0, 1, 2])

    def test_vertices_iter_empty(self):
        """Тест итератора по вершинам для пустого графа"""
        vertices = list(self.graph.vertices_iter())
        self.assertEqual(vertices, [])

    def test_edges_iter(self):
        """Тест итератора по ребрам"""
        self.graph.add_vertex("A")
        self.graph.add_vertex("B")
        self.graph.add_vertex("C")
        self.graph.add_edge(0, 1)
        self.graph.add_edge(1, 2)

        edges = list(self.graph.edges_iter())
        self.assertEqual(edges, [(0, 1), (1, 2)])

    def test_edges_iter_empty(self):
        """Тест итератора по ребрам для пустого графа"""
        edges = list(self.graph.edges_iter())
        self.assertEqual(edges, [])

    def test_outgoing_iter(self):
        """Тест итератора по исходящим ребрам"""
        self.graph.add_vertex("A")
        self.graph.add_vertex("B")
        self.graph.add_vertex("C")
        self.graph.add_edge(0, 1)
        self.graph.add_edge(0, 2)
        self.graph.add_edge(1, 2)

        outgoing = list(self.graph.outgoing_iter(0))
        self.assertEqual(set(outgoing), {1, 2})

    def test_outgoing_iter_no_edges(self):
        """Тест итератора по исходящим ребрам без ребер"""
        self.graph.add_vertex("A")
        outgoing = list(self.graph.outgoing_iter(0))
        self.assertEqual(outgoing, [])

    def test_incoming_iter(self):
        """Тест итератора по входящим ребрам"""
        self.graph.add_vertex("A")
        self.graph.add_vertex("B")
        self.graph.add_vertex("C")
        self.graph.add_edge(0, 1)
        self.graph.add_edge(2, 1)
        self.graph.add_edge(0, 2)

        incoming = list(self.graph.incoming_iter(1))
        self.assertEqual(set(incoming), {0, 2})

    def test_incoming_iter_no_edges(self):
        """Тест итератора по входящим ребрам без ребер"""
        self.graph.add_vertex("A")
        incoming = list(self.graph.incoming_iter(0))
        self.assertEqual(incoming, [])

    def test_str_empty(self):
        """Тест строкового представления пустого графа"""
        graph_str = str(self.graph)
        self.assertIn("Вершины:", graph_str)
        self.assertIn("Матрица смежности:", graph_str)

    def test_complex_graph(self):
        """Тест сложного графа"""
        # Создаем граф: 0 -> 1 -> 2
        #               \-> 3 -/
        self.graph.add_vertex("Start")
        self.graph.add_vertex("Middle1")
        self.graph.add_vertex("End")
        self.graph.add_vertex("Middle2")

        self.graph.add_edge(0, 1)
        self.graph.add_edge(0, 3)
        self.graph.add_edge(1, 2)
        self.graph.add_edge(3, 2)

        self.assertEqual(self.graph.vertex_count(), 4)
        self.assertEqual(self.graph.edge_count(), 4)
        self.assertEqual(self.graph.out_degree(0), 2)
        self.assertEqual(self.graph.in_degree(2), 2)

        # Проверяем матрицу смежности
        self.assertTrue(self.graph.matrix[0][1])
        self.assertTrue(self.graph.matrix[0][3])
        self.assertTrue(self.graph.matrix[1][2])
        self.assertTrue(self.graph.matrix[3][2])


if __name__ == '__main__':
    unittest.main(verbosity=2)
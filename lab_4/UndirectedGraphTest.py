import unittest
from UndirectedGraph import UndirectedGraph


class TestUndirectedGraph(unittest.TestCase):

    def setUp(self):
        """Настройка тестового графа перед каждым тестом"""
        self.graph = UndirectedGraph()

    def test_empty_graph(self):
        """Тест пустого графа"""
        self.assertEqual(self.graph.vertex_count(), 0)
        self.assertEqual(self.graph.edge_count(), 0)
        self.assertEqual(list(self.graph.vertices_iter()), [])
        self.assertEqual(list(self.graph.edges_iter()), [])

    def test_add_vertices(self):
        """Тест добавления вершин"""
        # Добавляем вершины и проверяем возвращаемые ID
        id1 = self.graph.add_vertex("A")
        id2 = self.graph.add_vertex("B")
        id3 = self.graph.add_vertex("C")

        self.assertEqual(id1, 0)
        self.assertEqual(id2, 1)
        self.assertEqual(id3, 2)
        self.assertEqual(self.graph.vertex_count(), 3)

        # Проверяем данные вершин
        self.assertEqual(self.graph.get_vertex_data(0), "A")
        self.assertEqual(self.graph.get_vertex_data(1), "B")
        self.assertEqual(self.graph.get_vertex_data(2), "C")

        # Проверяем итератор вершин
        self.assertEqual(list(self.graph.vertices_iter()), [0, 1, 2])

    def test_add_edges(self):
        """Тест добавления рёбер"""
        # Создаём вершины
        self.graph.add_vertex("A")
        self.graph.add_vertex("B")
        self.graph.add_vertex("C")

        # Добавляем рёбра
        self.graph.add_edge(0, 1)
        self.graph.add_edge(1, 2)
        self.graph.add_edge(0, 2)

        # Проверяем существование рёбер
        self.assertTrue(self.graph.has_edge(0, 1))
        self.assertTrue(self.graph.has_edge(1, 0))  # Ненаправленный граф
        self.assertTrue(self.graph.has_edge(1, 2))
        self.assertTrue(self.graph.has_edge(2, 1))  # Ненаправленный граф
        self.assertTrue(self.graph.has_edge(0, 2))
        self.assertTrue(self.graph.has_edge(2, 0))  # Ненаправленный граф

        # Проверяем количество рёбер
        self.assertEqual(self.graph.edge_count(), 3)

        # Проверяем итератор рёбер
        edges = list(self.graph.edges_iter())
        self.assertEqual(len(edges), 3)
        self.assertIn((0, 1), edges)
        self.assertIn((1, 2), edges)
        self.assertIn((0, 2), edges)

    def test_remove_vertices(self):
        """Тест удаления вершин"""
        # Создаём граф
        self.graph.add_vertex("A")
        self.graph.add_vertex("B")
        self.graph.add_vertex("C")
        self.graph.add_edge(0, 1)
        self.graph.add_edge(1, 2)

        # Удаляем вершину
        self.graph.remove_vertex(1)

        # Проверяем оставшиеся вершины
        self.assertEqual(self.graph.vertex_count(), 2)
        self.assertEqual(self.graph.get_vertex_data(0), "A")
        self.assertEqual(self.graph.get_vertex_data(1), "C")  # Вершины переиндексированы

        # Проверяем, что рёбра удалились
        self.assertEqual(self.graph.edge_count(), 0)

    def test_remove_edges(self):
        """Тест удаления рёбер"""
        # Создаём граф
        self.graph.add_vertex("A")
        self.graph.add_vertex("B")
        self.graph.add_vertex("C")
        self.graph.add_edge(0, 1)
        self.graph.add_edge(1, 2)
        self.graph.add_edge(0, 2)

        # Удаляем ребро
        self.graph.remove_edge(0, 1)

        # Проверяем
        self.assertFalse(self.graph.has_edge(0, 1))
        self.assertFalse(self.graph.has_edge(1, 0))
        self.assertTrue(self.graph.has_edge(1, 2))
        self.assertTrue(self.graph.has_edge(0, 2))
        self.assertEqual(self.graph.edge_count(), 2)

    def test_degree_calculation(self):
        """Тест расчёта степеней вершин"""
        # Создаём граф-треугольник
        self.graph.add_vertex("A")
        self.graph.add_vertex("B")
        self.graph.add_vertex("C")
        self.graph.add_edge(0, 1)
        self.graph.add_edge(1, 2)
        self.graph.add_edge(0, 2)

        # Проверяем степени
        self.assertEqual(self.graph.out_degree(0), 2)
        self.assertEqual(self.graph.in_degree(0), 2)
        self.assertEqual(self.graph.out_degree(1), 2)
        self.assertEqual(self.graph.in_degree(1), 2)
        self.assertEqual(self.graph.out_degree(2), 2)
        self.assertEqual(self.graph.in_degree(2), 2)

    def test_neighbors(self):
        """Тест поиска соседей"""
        # Создаём граф
        self.graph.add_vertex("A")
        self.graph.add_vertex("B")
        self.graph.add_vertex("C")
        self.graph.add_vertex("D")
        self.graph.add_edge(0, 1)
        self.graph.add_edge(0, 2)
        self.graph.add_edge(1, 3)

        # Проверяем соседей
        self.assertEqual(list(self.graph.outgoing_iter(0)), [1, 2])
        self.assertEqual(list(self.graph.incoming_iter(0)), [1, 2])  # Для ненаправленного графа одинаково
        self.assertEqual(list(self.graph.outgoing_iter(1)), [0, 3])
        self.assertEqual(list(self.graph.outgoing_iter(2)), [0])
        self.assertEqual(list(self.graph.outgoing_iter(3)), [1])

    def test_edge_cases(self):
        """Тест граничных случаев"""
        # Проверка несуществующих вершин
        self.assertFalse(self.graph.has_vertex(0))
        self.assertIsNone(self.graph.get_vertex_data(0))
        self.assertEqual(self.graph.out_degree(0), 0)
        self.assertEqual(list(self.graph.outgoing_iter(0)), [])

        # Добавляем вершину и проверяем граничные индексы
        self.graph.add_vertex("A")
        self.assertTrue(self.graph.has_vertex(0))
        self.assertFalse(self.graph.has_vertex(1))

        # Проверка несуществующих рёбер
        self.assertFalse(self.graph.has_edge(0, 1))
        self.assertFalse(self.graph.has_edge(1, 0))

    def test_complex_graph(self):
        """Тест сложного графа"""
        # Создаём граф с 5 вершинами
        for i in range(5):
            self.graph.add_vertex(f"V{i}")

        # Создаём рёбра (граф-звезда)
        self.graph.add_edge(0, 1)
        self.graph.add_edge(0, 2)
        self.graph.add_edge(0, 3)
        self.graph.add_edge(0, 4)
        self.graph.add_edge(1, 2)

        # Проверяем
        self.assertEqual(self.graph.vertex_count(), 5)
        self.assertEqual(self.graph.edge_count(), 5)

        # Проверяем степени центральной вершины
        self.assertEqual(self.graph.out_degree(0), 4)

        # Проверяем матрицу смежности
        edges = list(self.graph.edges_iter())
        expected_edges = [(0, 1), (0, 2), (0, 3), (0, 4), (1, 2)]
        self.assertEqual(set(edges), set(expected_edges))


if __name__ == "__main__":
    # Запуск тестов с подробным выводом
    unittest.main(verbosity=2)
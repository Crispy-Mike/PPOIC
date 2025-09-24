import unittest
from task_2 import DirectedGraph


class TestDirectedGraph(unittest.TestCase):

    def test_add_vertex(self):
        graph = DirectedGraph()
        index = graph.add_vertex("A")
        self.assertEqual(index, 0)
        self.assertEqual(graph.vertex_count(), 1)
        self.assertEqual(graph.get_vertex_data(0), "A")

    def test_add_edge(self):
        graph = DirectedGraph()
        a = graph.add_vertex("A")
        b = graph.add_vertex("B")
        graph.add_edge(a, b)
        self.assertTrue(graph.has_edge(a, b))
        self.assertFalse(graph.has_edge(b, a))

    def test_remove_vertex(self):
        graph = DirectedGraph()
        a = graph.add_vertex("A")
        b = graph.add_vertex("B")
        graph.add_edge(a, b)
        graph.remove_vertex(a)
        self.assertEqual(graph.vertex_count(), 1)
        self.assertFalse(graph.has_edge(a, b))

    def test_remove_edge(self):
        graph = DirectedGraph()
        a = graph.add_vertex("A")
        b = graph.add_vertex("B")
        graph.add_edge(a, b)
        graph.remove_edge(a, b)
        self.assertFalse(graph.has_edge(a, b))

    def test_vertex_count(self):
        graph = DirectedGraph()
        graph.add_vertex("A")
        graph.add_vertex("B")
        graph.add_vertex("C")
        self.assertEqual(graph.vertex_count(), 3)

    def test_edge_count(self):
        graph = DirectedGraph()
        a = graph.add_vertex("A")
        b = graph.add_vertex("B")
        c = graph.add_vertex("C")
        graph.add_edge(a, b)
        graph.add_edge(b, c)
        self.assertEqual(graph.edge_count(), 2)

    def test_out_degree(self):
        graph = DirectedGraph()
        a = graph.add_vertex("A")
        b = graph.add_vertex("B")
        c = graph.add_vertex("C")
        graph.add_edge(a, b)
        graph.add_edge(a, c)
        self.assertEqual(graph.out_degree(a), 2)

    def test_in_degree(self):
        graph = DirectedGraph()
        a = graph.add_vertex("A")
        b = graph.add_vertex("B")
        c = graph.add_vertex("C")
        graph.add_edge(a, b)
        graph.add_edge(c, b)
        self.assertEqual(graph.in_degree(b), 2)

    def test_vertices_iter(self):
        graph = DirectedGraph()
        graph.add_vertex("A")
        graph.add_vertex("B")
        vertices = list(graph.vertices_iter())
        self.assertEqual(vertices, [0, 1])

    def test_edges_iter(self):
        graph = DirectedGraph()
        a = graph.add_vertex("A")
        b = graph.add_vertex("B")
        graph.add_edge(a, b)
        edges = list(graph.edges_iter())
        self.assertEqual(edges, [(0, 1)])

    def test_outgoing_iter(self):
        graph = DirectedGraph()
        a = graph.add_vertex("A")
        b = graph.add_vertex("B")
        c = graph.add_vertex("C")
        graph.add_edge(a, b)
        graph.add_edge(a, c)
        outgoing = list(graph.outgoing_iter(a))
        self.assertEqual(set(outgoing), {1, 2})

    def test_incoming_iter(self):
        graph = DirectedGraph()
        a = graph.add_vertex("A")
        b = graph.add_vertex("B")
        c = graph.add_vertex("C")
        graph.add_edge(a, b)
        graph.add_edge(c, b)
        incoming = list(graph.incoming_iter(b))
        self.assertEqual(set(incoming), {0, 2})


if __name__ == '__main__':
    unittest.main()
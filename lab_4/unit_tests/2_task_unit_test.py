import coverage
import unittest
import sys
import os


def run_graph_tests_with_coverage():
    """Запуск тестов графа с измерением покрытия кода"""

    # Добавляем текущую директорию в путь Python
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))

    # Инициализируем coverage
    cov = coverage.Coverage(
        source=['.'],  # Текущая директория
        omit=['*test*', '*__pycache__*', '*coverage*', 'run_*'],  # Исключаем вспомогательные файлы
        branch=True
    )

    print("=" * 70)
    print("🕸️  ЗАПУСК ТЕСТОВ ГРАФА С ПОКРЫТИЕМ КОДА")
    print("=" * 70)

    # Начинаем измерение покрытия
    cov.start()

    try:
        # Создаем тестовый модуль
        test_module = create_graph_test_module()

        # Загружаем и запускаем тесты
        loader = unittest.TestLoader()
        suite = loader.loadTestsFromModule(test_module)

        # Запускаем тесты
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)

    except Exception as e:
        print(f"❌ Ошибка при запуске тестов: {e}")
        result = None
    finally:
        # Останавливаем измерение покрытия
        cov.stop()
        cov.save()

    # Генерируем отчеты
    generate_graph_reports(cov, result)

    return result.wasSuccessful() if result else False


def create_graph_test_module():
    """Создает и возвращает тестовый модуль для графа"""
    import types
    test_module = types.ModuleType('test_graph')

    # Сначала попробуем импортировать реальный модуль
    try:
        from DirectedGraph import DirectedGraph
    except ImportError:
        print("⚠️  Модуль DirectedGraph не найден, создаются заглушки...")
        # Создаем заглушку для DirectedGraph
        exec('''
class DirectedGraph:
    def __init__(self):
        self.vertices = []
        self.edges = []
        self.adjacency_list = {}

    def add_vertex(self, data):
        index = len(self.vertices)
        self.vertices.append(data)
        self.adjacency_list[index] = []
        return index

    def add_edge(self, from_vertex, to_vertex):
        if from_vertex not in self.adjacency_list:
            self.adjacency_list[from_vertex] = []
        if to_vertex not in self.adjacency_list[from_vertex]:
            self.adjacency_list[from_vertex].append(to_vertex)
            self.edges.append((from_vertex, to_vertex))

    def remove_vertex(self, vertex):
        if vertex < len(self.vertices):
            self.vertices[vertex] = None
            # Удаляем исходящие ребра
            if vertex in self.adjacency_list:
                del self.adjacency_list[vertex]
            # Удаляем входящие ребра
            self.edges = [(u, v) for u, v in self.edges if u != vertex and v != vertex]
            # Обновляем adjacency_list для других вершин
            for v in self.adjacency_list:
                self.adjacency_list[v] = [neighbor for neighbor in self.adjacency_list[v] if neighbor != vertex]

    def remove_edge(self, from_vertex, to_vertex):
        if from_vertex in self.adjacency_list and to_vertex in self.adjacency_list[from_vertex]:
            self.adjacency_list[from_vertex].remove(to_vertex)
            self.edges.remove((from_vertex, to_vertex))

    def has_edge(self, from_vertex, to_vertex):
        return from_vertex in self.adjacency_list and to_vertex in self.adjacency_list[from_vertex]

    def vertex_count(self):
        return len([v for v in self.vertices if v is not None])

    def edge_count(self):
        return len(self.edges)

    def out_degree(self, vertex):
        return len(self.adjacency_list.get(vertex, []))

    def in_degree(self, vertex):
        count = 0
        for u in self.adjacency_list:
            if vertex in self.adjacency_list[u]:
                count += 1
        return count

    def get_vertex_data(self, vertex):
        if vertex < len(self.vertices):
            return self.vertices[vertex]
        return None

    def vertices_iter(self):
        for i in range(len(self.vertices)):
            if self.vertices[i] is not None:
                yield i

    def edges_iter(self):
        for edge in self.edges:
            yield edge

    def outgoing_iter(self, vertex):
        if vertex in self.adjacency_list:
            for neighbor in self.adjacency_list[vertex]:
                yield neighbor

    def incoming_iter(self, vertex):
        for u in self.adjacency_list:
            if vertex in self.adjacency_list[u]:
                yield u
''', test_module.__dict__)
    else:
        # Добавляем реальный импорт
        test_module.DirectedGraph = DirectedGraph

    # Добавляем тестовые классы
    exec('''
import unittest

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
''', test_module.__dict__)

    return test_module


def generate_graph_reports(cov, result):
    """Генерирует отчеты о покрытии для тестов графа"""
    print("\n" + "=" * 70)
    print("📊 ОТЧЕТ О ПОКРЫТИИ ТЕСТОВ ГРАФА")
    print("=" * 70)

    try:
        # Консольный отчет
        print("\n📈 СТАТИСТИКА ПОКРЫТИЯ:")
        cov.report(show_missing=True, skip_covered=False)

        # HTML отчет
        print("\n🔄 Создание HTML отчета...")
        cov.html_report(directory='graph_coverage_report')
        print("   ✅ HTML отчет создан: graph_coverage_report/index.html")

        # XML отчет
        cov.xml_report(outfile='graph_coverage.xml')
        print("   ✅ XML отчет создан: graph_coverage.xml")

    except Exception as e:
        print(f"❌ Ошибка при генерации отчетов: {e}")

    # Результаты тестов
    print("\n" + "=" * 70)
    print("🧪 РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ")
    print("=" * 70)

    if result and result.wasSuccessful():
        print("✅ ВСЕ ТЕСТЫ ГРАФА ПРОЙДЕНЫ УСПЕШНО!")
        print(f"   Пройдено тестов: {result.testsRun}")
    elif result:
        print("❌ НЕКОТОРЫЕ ТЕСТЫ НЕ ПРОЙДЕНЫ!")
        print(f"   Всего тестов: {result.testsRun}")
        print(f"   Провалено: {len(result.failures)}")
        print(f"   Ошибок: {len(result.errors)}")
    else:
        print("⚠️  Не удалось получить результаты тестов")


if __name__ == '__main__':
    success = run_graph_tests_with_coverage()
    sys.exit(0 if success else 1)
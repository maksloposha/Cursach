import sys
import networkx as nx
from tkinter import messagebox


class Graph(nx.DiGraph):
    def __init__(self, nodes, init_graph, is_undirected = False):
        nx.DiGraph.__init__(self)
        self._nodes = nodes
        if is_undirected:   # Якщо граф ненаправлений створюємо симетричні ребра
            self.init_graph = {}
            self.init_graph.update(init_graph)
            for node, edges in self.init_graph.items():
                for adjacent_node, value in edges.items():
                    if self.init_graph[adjacent_node].get(node, False) == False:
                        self.init_graph[adjacent_node][node] = value
        else:
            self.init_graph = init_graph

        for node in nodes:
            for an_node in init_graph[node]:
                self.add_edge(node, an_node)

    def dijkstra_algorithm(self, start_node):
        unvisited_nodes = list(self.nodes())
        shortest_path = {}
        previous_nodes = {}

        max_value = sys.maxsize
        for node in unvisited_nodes:
            shortest_path[node] = max_value   # ініціалізовуємо шлях до кожного з вузлів нескінченністю
        # Однак початковий вузол інціалізовуємо 0
        shortest_path[start_node] = 0

        # Алгоритм виконується до тих пір поки ми не відвідаємо всі вузли
        while unvisited_nodes:
            # Блок нижче знаходить вузол з найменшою
            current_min_node = None
            for node in unvisited_nodes:  # Ітеруємо по вузлах
                if current_min_node == None:
                    current_min_node = node
                elif shortest_path[node] < shortest_path[current_min_node]:
                    current_min_node = node

            # Блок нижче знаходить сусідів вузла і оновлює його відстані
            neighbors = self.neighbors(current_min_node)
            for neighbor in neighbors:
                tentative_value = shortest_path[current_min_node] + self.init_graph[current_min_node][neighbor]
                if tentative_value < shortest_path[neighbor]:
                    shortest_path[neighbor] = tentative_value
                    # Також оновлюємо найкращий шлях до поточного вузла
                    previous_nodes[neighbor] = current_min_node

            # Після виконання ітерації видаляємо поточний вузол, тим самим помічаємо його відвіданим
            unvisited_nodes.remove(current_min_node)

        return previous_nodes, shortest_path

    def bellman_ford(self, start_node):
        max_value = sys.maxsize
        shortest_path = {}
        previous_nodes = {}
        for node in self._nodes:
            shortest_path[node] = max_value # ініціалізовуємо шлях до кожного з вузлів нескінченністю
        # Однак початковий вузол інціалізовуємо 0
        shortest_path[start_node] = 0
        for i in range(len(self.nodes) - 1):
            for start in self.init_graph.keys(): #Проходимо по значеннях словника суміжності
                for finish in self.init_graph[start].keys(): # Проходимо по сусідах вузла start
                    if shortest_path[start] != max_value and shortest_path[start] + self.init_graph[start][finish] < shortest_path[finish]:
                        shortest_path[finish] = shortest_path[start] + self.init_graph[start][finish]  # Оновлюємо цінність шляху до сусідів вузла start
                        previous_nodes[finish] = start   # Оновлюємо шлях до сусідів вузла start
        # Якщо ми можемо зробити ще один такий прохід значить граф містить цикл негативної ваги
        for start in self.init_graph.keys():
            for finish in self.init_graph[start].keys():
                if shortest_path[start] != max_value and shortest_path[start] + self.init_graph[start][finish] < shortest_path[finish]:
                    with open('statistics.txt', 'a') as file:
                        file.write("Graph contains negative weight cycle\n")
                    messagebox.showinfo("Warning", "Graph contains negative weight cycle")
                    return
        return previous_nodes,shortest_path

    def colour(self, path):
        colour = []   # масив кольорів для візуального зображення найкоротшого шляху в графі
        count = 0
        seq = []      # послідовність графів які треба замлювати як найкоротший шлях
        edges = list(self.edges)
        while True:
            path_tup = tuple(path[count:count+2])    # створємо кортеж , який буде відповідати за ребро графа
            seq.append(edges.index(path_tup))
            count += 1
            if count == len(path) - 1:
                break
        for i in range(len(edges)):   #створюємо послідовність кольорів
            if i in seq:
                colour.append("red")
            else:
                colour.append("white")
        return colour

    def print_result(self, previous_nodes, shortest_path, start_node, target_node):
        node = target_node
        if shortest_path[target_node] == sys.maxsize:
            messagebox.showinfo("Неможливо досягти вузла", "Введіть кінцевий вузол ще раз")
            return
        path = []
        while node != start_node:    #створюємо список, який відповідає за найкоротший шлях від одного вузла до іншого
            path.append(node)
            node = previous_nodes[node]

        # Добавить начальный узел вручную
        path.append(start_node)
        messagebox.showinfo("Знайдено шлях", "Найкоротший шлях {}".format(shortest_path[target_node]))
        with open('statistics.txt','a') as file:
            file.write(("The shortest path of weight {} was found.".format(shortest_path[target_node])))
            file.write(" -> ".join(reversed(path)))
        return path[::-1]

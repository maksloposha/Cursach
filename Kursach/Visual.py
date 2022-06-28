from Parse import Parse
from tkinter import messagebox
from tkinter import *
import matplotlib
import networkx as nx
import matplotlib.pyplot as plt
import Graph_Logic
matplotlib.use("TkAgg")



class Visual(Parse):
    def __init__(self):
        self.root = Tk()       # головне вікно
        self.root.geometry("900x700")   # задаємо розмір
        self.root.resizable(False, False)   # заборона змінювати
        self.path = []        # масив найкоротшого шляху графа
        self.graph = nx.Graph
        self.table_of_entry = [] # таблиця полів вводу
        self.graph_matrix = []   # матриця графу
        self.frame_of_table = Frame(self.root)   # фрейм де розміщується матриця полів вводу
        self.frame_of_table.place(x=0, y=100)
        entry_size_graph = Entry(self.root)    # поле з якого парсимо інформацію про розмір матриці
        entry_size_graph.place(relx=.5, rely=.05, anchor="c", height=30, width=70, bordermode=OUTSIDE)
        self.size_of_matrix = 0    # розмір матриці
        btn_size = Button(text="Enter the number of nodes", command=lambda: self.set_label_text(entry_size_graph)) # кнопка введення розміру і сторення матриі полів вводу
        btn_size.place(relx=.5, rely=.1, anchor="c", height=30, bordermode=OUTSIDE)
        label_start_node = Label(self.root, text="Start node")                # підпис стартового вузла
        label_target_node = Label(self.root, text="Target node")              # підпис про кінцевий вузол
        label_start_node.place(relx=.35, rely=.65, anchor="c",  bordermode=OUTSIDE)
        label_target_node.place(relx=.5, rely=.65, anchor="c",  bordermode=OUTSIDE)
        start_node = Entry(self.root)                                     # поле вводу стартового вузла
        target_node = Entry(self.root)                                   # поле вводу кінцевого вузла
        start_node.place(relx=.42, rely=.65, anchor="c", height=20, width=50, bordermode=OUTSIDE)
        target_node.place(relx=.57, rely=.65, anchor="c", height=20, width=50, bordermode=OUTSIDE)
        btn_save_matrix = Button(self.root, text="Save matrix", command=lambda: self.get_info())
        btn_save_matrix.place(relx=.42, rely=.7, anchor="c", height=30, width=70, bordermode=OUTSIDE)  # зчитує і зберігає матрицю графа
        btn_show_graph = Button(self.root, text="Show graph",
                                 command=lambda: self.show_graph())
        btn_show_graph.place(relx=.57, rely=.7, anchor="c", height=30, width=70, bordermode=OUTSIDE)  # виконує команду показати граф і створити об'єкт класу Graph
        self.is_direct = BooleanVar()    # змінна яка відповідає за те, чи направлений граф
        self.is_direct.set(0)
        directed = Radiobutton(self.root, text='Орієнтований граф', variable=self.is_direct, value=0)
        directed.place(relx=.3, rely=.1, anchor="c")
        undirected = Radiobutton(self.root, text='Неорієнтований граф', variable=self.is_direct, value=1)
        undirected.place(relx=.7, rely=.1, anchor="c")
        self.r_algorithm = BooleanVar()      # змінна що відповідає за вибір алгоритму
        self.r_algorithm.set(0)
        r_dijkstra = Radiobutton(text='Алгоритм Дейкстри', variable=self.r_algorithm, value=0)
        r_bellman = Radiobutton(text='Алгоритм Беллмана-Форда', variable=self.r_algorithm, value=1)
        r_dijkstra.place(relx=.5, rely=.8, anchor="c")
        r_bellman.place(relx=.5, rely=.85, anchor="c")
        btn_draw_res_graph = Button(self.root, text="Show result",
                                    command=lambda: self.show_result(start_node, target_node))
        btn_draw_res_graph.place(relx=.5, rely=.9, anchor="c")
        self.root.mainloop()

    def set_label_text(self, entry):
        self.table_of_entry.clear()
        self.size_of_matrix = int(self.convert_to_int(entry))  # зчитуємо значення розміру матриці
        if not 2 <= self.size_of_matrix <= 15:
            messagebox.showinfo("Замале або завелике значення",
                                "Розміри графу нестандартні\n(Розмір повинен бути в діапазоні від 2 до 15)")
            return
        alphabet = "ABCDEFGHIJKLMNO"   # назви вузлів
        entry_text = []              #  масив текстових змінних
        for i in range(self.size_of_matrix):
            label_rows = Label(self.frame_of_table, width=7) # рядок підпису
            label_rows.grid(row=i + 1, column=0)
            label_rows['text'] = alphabet[i]
            for j in range(self.size_of_matrix):
                label_column = Label(self.frame_of_table, width=7)   # колонка підпису
                label_column.grid(row=0, column=j + 1)
                label_column['text'] = alphabet[j]
                entry_text.append(IntVar())
                if i == j:
                    self.table_of_entry.append(Entry(self.frame_of_table, textvariable=entry_text[-1], width=7)) # створення ячейки вводу
                    self.table_of_entry[-1].config(state="readonly")
                elif i < j and self.is_direct.get() != 0:
                    self.table_of_entry.append(Entry(self.frame_of_table, textvariable=entry_text[-1], width=7))
                    self.table_of_entry[-1].config(state="readonly")
                else:
                    self.table_of_entry.append(Entry(self.frame_of_table, textvariable=entry_text[-1], width=7))
                self.table_of_entry[-1].grid(row=i + 1, column=j + 1)

    def get_info(self):
        self.graph_matrix = []  # очищення матриці графу
        zero_matrix = True     # значення що відповідає за те, чи нульова матриця
        k = 0
        for i in range(self.size_of_matrix):
            row = list()
            for j in range(self.size_of_matrix):
                item = self.convert_to_int(self.table_of_entry[k])
                if item != 0:
                    zero_matrix = False
                if item is None:
                    return
                row.append(item)    # створюємо матрицю графа
                k += 1
            self.graph_matrix.append(row)
        if zero_matrix:
            messagebox.showinfo("Помилка", "Ви задали порожню матрицю")
            return
        with open('statistics.txt', 'a') as file:   # записуємо матрицю в файл
            file.write("\nMatrix of graph:\n")
            for i in range(len(self.graph_matrix)):
                for j in range(len(self.graph_matrix)):
                    file.write(str(self.graph_matrix[i][j]) + " ")
                file.write("\n")

    def show_graph(self):
        if not self.graph_matrix:
            messagebox.showinfo("Помилка", "Ви ще не заповнили матрицю графа або не зберегли матрицю")
            return
        nodes = []   # масив візлів
        init_graph = {}   # словник сумжності вузлів
        alphabet = "ABCDEFGHIJKLMNO"
        for i in range(len(self.graph_matrix)):
            nodes.append(alphabet[i])   # заповнення масиву вузлів
        labels = {}      # словник підписів , що відповідає за ваги
        for node in nodes:
            init_graph[node] = {}
        for i in range(len(self.graph_matrix)):
            for j in range(len(self.graph_matrix)):
                if self.graph_matrix[i][j] != 0:
                    init_graph[alphabet[i]][alphabet[j]] = self.graph_matrix[i][j]  # інііалізація словника суміжності
                    labels[(alphabet[i], alphabet[j])] = self.graph_matrix[i][j]   # інціалізаці словника підписів
        self.graph = Graph_Logic.Graph(nodes, init_graph, self.is_direct.get())   # створення графа
        nx.draw(self.graph, with_labels=True, pos=nx.circular_layout(self.graph))
        nx.draw_networkx_edge_labels(self.graph, pos=nx.circular_layout(self.graph), edge_labels=labels, font_size=10)
        plt.show()

    def show_result(self, start_node, target_node):
        if self.convert_to_str(start_node, self.graph.nodes) is None or self.convert_to_str(target_node,
                                                                                            self.graph.nodes) is None:
            return
        if self.r_algorithm.get() == 0:
            sign = False
            for i in range(len(self.graph_matrix)):
                for j in range(len(self.graph_matrix)):
                    if self.graph_matrix[i][j] < 0:
                        sign = True
            if sign:
                messagebox.showinfo("Помилка", "Для алгоритму Дейкстри не допускається використання негативних ваг")
                return

            unvisited_nodes, shortest_path = self.graph.dijkstra_algorithm("A")    # виконання алгоритму дейкстри для заданого графа
            self.path = self.graph.print_result(unvisited_nodes, shortest_path,   # створення масиву шляху
                                                start_node=self.convert_to_str(start_node, self.graph.nodes),
                                                target_node=self.convert_to_str(target_node, self.graph.nodes))
        else:
            unvisited_nodes, shortest_path = self.graph.bellman_ford(  # виконання алгоритму Беллмана-Форда для заданого графа
                self.convert_to_str(start_node, self.graph.nodes))
            self.path = self.graph.print_result(unvisited_nodes, shortest_path, # створення масиву шляху
                                                start_node=self.convert_to_str(start_node, self.graph.nodes),
                                                target_node=self.convert_to_str(target_node, self.graph.nodes))
        if self.is_direct.get() != 0:  # якщо граф неорієнтований створюємо екземпляр класу nx.Graph() і записуємо туди наші ребра
            graph = nx.Graph()
            graph.add_edges_from(self.graph.edges)
        else:
            graph = self.graph
        nx.draw(graph, edge_color=self.graph.colour(self.path), with_labels=True,
                pos=nx.circular_layout(graph))         # виводимо граф з пофарбованим найкоротшим шляхом
        plt.show()

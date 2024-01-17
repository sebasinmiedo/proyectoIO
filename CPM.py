import tkinter as tk
import networkx as nx
import matplotlib.pyplot as plt
from criticalpath import Node

class ProyectoApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Metodo CPM")
        self.master.geometry("500x500")

        self.tareas_label = tk.Label(master, text="Ingrese las tareas y sus duraciones (Formato: Nombre:Duracion):")
        self.tareas_label.pack()

        self.tareas_entry = tk.Text(master, height=10, width=30)
        self.tareas_entry.insert(tk.END, 'A:4\nB:2\nC:3\nD:1\nE:5')
        self.tareas_entry.pack()

        self.dependencias_label = tk.Label(master, text="Ingrese las dependencias (Formato: Fuente-Destino):")
        self.dependencias_label.pack()

        self.dependencias_entry = tk.Text(master, height=10, width=30)
        self.dependencias_entry.insert(tk.END, 'A-B\nA-C\nA-D\nB-E\nC-E')
        self.dependencias_entry.pack()

        self.calcular_button = tk.Button(master, text="Calcular", command=self.calcular_proyecto)
        self.calcular_button.pack()

    def calcular_proyecto(self):
        tareas_input = self.tareas_entry.get("1.0", tk.END).strip().split('\n')
        dependencias_input = self.dependencias_entry.get("1.0", tk.END).strip().split('\n')

        tareas = [task.split(':') for task in tareas_input]
        tareas = [(name, {"duracion": int(duration)}) for name, duration in tareas]

        dependencias = [dep.split('-') for dep in dependencias_input]
        dependencias = [(source, target) for source, target in dependencias]

        p = Node('proyecto')

        G = nx.DiGraph()

        for i in tareas:
            p.add(Node(i[0], duration=i[1]["duracion"]))
            G.add_node(i[0], duration=i[1]["duracion"])

        for j in dependencias:
            p.link(j[0], j[1])
            G.add_edge(j[0], j[1])

        p.update_all()

        critical_path = p.get_critical_path()
        duration = p.duration

        result_window = tk.Toplevel(self.master)
        result_window.title("Resultados")

        result_label = tk.Label(result_window, text=f"Ruta Crítica: {critical_path}\nDuración del proyecto: {duration}", height=10, width=50)
        result_label.pack()

        # Visualizar el grafo
        self.mostrar_grafo(G)

    def mostrar_grafo(self, G):
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_size=700, node_color='skyblue', font_size=8)
        plt.title('Grafo del Proyecto')
        plt.show()

def ventana_cpm():
    root = tk.Tk()
    app = ProyectoApp(root)
    root.mainloop()

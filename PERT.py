import tkinter as tk
import networkx as nx
import matplotlib.pyplot as plt
from criticalpath import Node

class ProyectoApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Metodo PERT")
        self.master.geometry("500x500")

        self.tareas_label = tk.Label(master, text="Ingrese las tareas y sus tiempos (Formato: Nombre:TO,TP,TPe):")
        self.tareas_label.pack()

        self.tareas_entry = tk.Text(master, height=10, width=30)
        self.tareas_entry.insert(tk.END, 'A:1,2,3\nB:1,2,3\nC:1,1,1\nD:1,2,3\nE:2,3,4\nF:1,1,1\nG:2,2,2\nH:1,1,1')
        self.tareas_entry.pack()

        self.dependencias_label = tk.Label(master, text="Ingrese las dependencias (Formato: Fuente-Destino):")
        self.dependencias_label.pack()

        self.dependencias_entry = tk.Text(master, height=10, width=30)
        self.dependencias_entry.insert(tk.END, 'A-B\nA-C\nB-D\nC-D\nD-E\nD-F\nD-G\nE-H\nF-H\nG-H')
        self.dependencias_entry.pack()

        self.calcular_button = tk.Button(master, text="Calcular", command=self.calcular_proyecto)
        self.calcular_button.pack()

    def calcular_proyecto(self):
        tareas_input = self.tareas_entry.get("1.0", tk.END).strip().split('\n')
        dependencias_input = self.dependencias_entry.get("1.0", tk.END).strip().split('\n')

        tareas = [task.split(':') for task in tareas_input]

        p = Node('proyecto')

        G = nx.DiGraph()

        for i in tareas:
            tiempos = i[1].split(',')
            tiempo_optimista, tiempo_mas_probable, tiempo_pessimista = map(int, tiempos)
            tiempo_esperado = (tiempo_optimista + 4 * tiempo_mas_probable + tiempo_pessimista) / 6
            p.add(Node(i[0], duration=tiempo_esperado))
            G.add_node(i[0], duration=tiempo_esperado)

        dependencias = [dep.split('-') for dep in dependencias_input]
        dependencias = [(source, target) for source, target in dependencias]

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

def ventana_pert():
    root = tk.Tk()
    app = ProyectoApp(root)
    root.mainloop()
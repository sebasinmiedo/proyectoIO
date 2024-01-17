import tkinter as tk
import networkx as nx
import matplotlib.pyplot as plt
from criticalpath import Node
import math
from scipy.stats import norm

class ProyectoApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Metodo PERT")
        self.master.geometry("500x600")

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

        self.tiempo_proyectado_label = tk.Label(master, text="Ingrese el tiempo proyectado:")
        self.tiempo_proyectado_label.pack()

        self.tiempo_proyectado_entry = tk.Entry(master)
        self.tiempo_proyectado_entry.pack()

        self.calcular_button = tk.Button(master, text="Calcular", command=self.calcular_proyecto)
        self.calcular_button.pack()

    def calcular_proyecto(self):
        tareas_input = self.tareas_entry.get("1.0", tk.END).strip().split('\n')
        dependencias_input = self.dependencias_entry.get("1.0", tk.END).strip().split('\n')
        tiempo_proyectado = float(self.tiempo_proyectado_entry.get())  # Obtener el tiempo proyectado

        tareas = [task.split(':') for task in tareas_input]

        p = Node('proyecto')

        G = nx.DiGraph()

        varianzas_todas_tareas = []  # Lista para almacenar las varianzas de todas las tareas
        nombre_a_indice = {}  # Diccionario para mapear nombres de tareas a índices

        for i, tarea_info in enumerate(tareas):
            tiempos = tarea_info[1].split(',')
            tiempo_optimista, tiempo_mas_probable, tiempo_pessimista = map(int, tiempos)
            tiempo_esperado = (tiempo_optimista + 4 * tiempo_mas_probable + tiempo_pessimista) / 6
            tarea = Node(tarea_info[0], duration=tiempo_esperado)
            p.add(tarea)
            G.add_node(tarea_info[0], duration=tiempo_esperado)

            # Calcular varianza de la tarea y agregarla a la lista
            varianza_tarea = ((tiempo_pessimista - tiempo_optimista) ** 2) / 36
            varianzas_todas_tareas.append(varianza_tarea)
            nombre_a_indice[tarea_info[0]] = i  # Mapear nombre de tarea a índice

        dependencias = [dep.split('-') for dep in dependencias_input]
        dependencias = [(source, target) for source, target in dependencias]

        for j in dependencias:
            p.link(j[0], j[1])
            G.add_edge(j[0], j[1])

        p.update_all()

        critical_path = p.get_critical_path()
        duration = p.duration

        # Calcular la desviación estándar de la ruta crítica
        desviacion_estandar_proyecto = self.calcular_desviacion_estandar_proyecto(varianzas_todas_tareas, critical_path, nombre_a_indice)

        # Calcular Z y P(z)
        z = (tiempo_proyectado - duration) / desviacion_estandar_proyecto
        probabilidad = norm.cdf(z)

        # Mostrar resultados
        result_window = tk.Toplevel(self.master)
        result_window.title("Resultados")

        result_label = tk.Label(result_window, text=f"Ruta Crítica: {critical_path}\nDuración del proyecto: {duration}\n"
                                                    f"Desviación Estándar del Proyecto: {desviacion_estandar_proyecto}\n"
                                                    f"Tiempo Proyectado: {tiempo_proyectado}\n"
                                                    f"Z: {z}\n"
                                                    f"P(Z): {probabilidad * 100:.3f}%",
                                height=15, width=50)
        result_label.pack()

        # Visualizar el grafo
        self.mostrar_grafo(G)

    def mostrar_grafo(self, G):
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_size=700, node_color='skyblue', font_size=8)
        plt.title('Grafo del Proyecto')
        plt.show()

    def calcular_desviacion_estandar_proyecto(self, varianzas_todas_tareas, critical_path, nombre_a_indice):
        # Extraer varianzas de la ruta crítica
        varianzas_criticas = [varianzas_todas_tareas[nombre_a_indice[node.name]] for node in critical_path]

        # Calcular la desviación estándar de las varianzas de la ruta crítica
        desviacion_estandar_proyecto = math.sqrt(sum(varianzas_criticas))
        return desviacion_estandar_proyecto

def ventana_pert():
    root = tk.Tk()
    app = ProyectoApp(root)
    root.mainloop()

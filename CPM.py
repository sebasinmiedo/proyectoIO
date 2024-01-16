import tkinter as tk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

nodos = []  # Lista para almacenar los nodos
grafo = nx.DiGraph()  # Grafo dirigido
critical_path = []  # Variable para almacenar la ruta crítica
ruta_critica_valor = 0  # Valor de la ruta crítica

def agregar_nodo(entry_nodo, entry_duracion, entry_predecesores, lista_nodos):
    nodo = entry_nodo.get()
    duracion = int(entry_duracion.get())
    predecesores = entry_predecesores.get().split(',') if entry_predecesores.get() else []  # Obtener predecesores como una lista separada por comas

    nodos.append((nodo, duracion, predecesores))
    entry_nodo.delete(0, tk.END)
    entry_duracion.delete(0, tk.END)
    entry_predecesores.delete(0, tk.END)
    mostrar_nodos(lista_nodos)

def generar_grafo():
    global critical_path, ruta_critica_valor
    grafo.clear()
    grafo.add_nodes_from([nodo[0] for nodo in nodos])

    for nodo, _, predecesores in nodos:
        for predecesor in predecesores:
            grafo.add_edge(predecesor.strip(), nodo.strip())

    critical_path = calcular_ruta_critica()
    dibujar_grafo()
    mostrar_valor_ruta_critica()

def calcular_ruta_critica():
    for nodo in grafo.nodes():
        grafo.nodes[nodo]['duracion'] = 0

    calcular_ruta = True
    while calcular_ruta:
        calcular_ruta = False
        for nodo in nodos:
            nodo_id, duracion, predecesores = nodo
            if not predecesores:
                grafo.nodes[nodo_id]['duracion'] = duracion
            else:
                max_duration = max([grafo.nodes[pred].get('duracion', 0) for pred in predecesores])
                if grafo.nodes[nodo_id].get('duracion', 0) != max_duration + duracion:
                    grafo.nodes[nodo_id]['duracion'] = max_duration + duracion
                    calcular_ruta = True

    critical_path = nx.dag_longest_path(grafo)
    return critical_path

def mostrar_nodos(lista_nodos):
    lista_nodos.delete(0, tk.END)
    for nodo, duracion, predecesores in nodos:
        lista_nodos.insert(tk.END, f"Nodo: {nodo}, Duración: {duracion}, Predecesores: {', '.join(predecesores)}")

def mostrar_valor_ruta_critica():
    global ruta_critica_valor
    ruta_critica_valor = sum([nodo[1] for nodo in nodos if nodo[0] in critical_path])
    dibujar_grafo()

def dibujar_grafo():
    global label_ruta_critica, ruta_critica_valor
    plt.figure(figsize=(8, 6))

    pos = nx.spring_layout(grafo)
    node_colors = ['skyblue' if node not in critical_path else 'red' for node in grafo.nodes()]

    nx.draw(grafo, pos, with_labels=True, node_size=800, node_color=node_colors, font_weight='bold', arrows=True)
    plt.title("Grafo de Nodos y Predecesores")
    plt.axis('off')

    if 'canvas' in globals():
        canvas.get_tk_widget().pack_forget()  # Eliminar canvas anterior si existe

    fig = plt.gcf()
    canvas = FigureCanvasTkAgg(fig, master=frame_grafo)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    # Recalcular el valor de la ruta crítica
    ruta_critica_valor = sum([nodo[1] for nodo in nodos if nodo[0] in critical_path])

    # Obtener la posición del último nodo en la ruta crítica
    if critical_path:
        last_node = critical_path[-1]
        x, y = pos[last_node]

        # Mostrar el valor de la ruta crítica en el último nodo de la ruta
        plt.text(x, y - 0.1, f"Valor de la ruta crítica: {ruta_critica_valor}", fontsize=10, ha='center', bbox=dict(facecolor='white', alpha=0.8))

    if 'label_ruta_critica' in globals():
        label_ruta_critica.destroy()

    label_ruta_critica = tk.Label(ventana_cpm, text=f"Valor de la ruta crítica: {ruta_critica_valor}", font=("Arial", 12))
    label_ruta_critica.pack()

def reset_variables():
    global nodos, grafo, critical_path, ruta_critica_valor
    nodos = []
    grafo = nx.DiGraph()
    critical_path = []
    ruta_critica_valor = 0
    ventana_cpm.destroy()  # Cierra la ventana de CPM

def ventana_cpm():
    global ventana_cpm  # Esto se utiliza para que la variable sea global y pueda ser accedida en otros lugares
    ventana_cpm = tk.Tk()  # Crear una nueva ventana, en lugar de utilizar Toplevel
    ventana_cpm.title("Datos para CPM")
    ventana_cpm.geometry("800x600")

    label_nodo = tk.Label(ventana_cpm, text="Nodo:")
    label_nodo.pack()

    entry_nodo = tk.Entry(ventana_cpm)
    entry_nodo.pack()

    label_duracion = tk.Label(ventana_cpm, text="Duración:")
    label_duracion.pack()

    entry_duracion = tk.Entry(ventana_cpm)
    entry_duracion.pack()

    label_predecesores = tk.Label(ventana_cpm, text="Predecesores (separados por coma):")
    label_predecesores.pack()

    entry_predecesores = tk.Entry(ventana_cpm)
    entry_predecesores.pack()

    lista_nodos = tk.Listbox(ventana_cpm)
    lista_nodos.pack()

    boton_agregar = tk.Button(ventana_cpm, text="Agregar Nodo", command=lambda: agregar_nodo(entry_nodo, entry_duracion, entry_predecesores, lista_nodos))
    boton_agregar.pack()

    boton_generar_grafo = tk.Button(ventana_cpm, text="Generar Grafo", command=generar_grafo)
    boton_generar_grafo.pack()

    boton_salir = tk.Button(ventana_cpm, text="Salir", command=reset_variables)
    boton_salir.pack()

    global frame_grafo
    frame_grafo = tk.Frame(ventana_cpm)
    frame_grafo.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

def mostrar_valor_ruta_critica():
    global ruta_critica_valor
    ruta_critica_valor = sum([nodo[1] for nodo in nodos if nodo[0] in critical_path])
    dibujar_grafo()
import tkinter as tk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

nodos = []  # Lista para almacenar los nodos
grafo = nx.DiGraph()  # Grafo dirigido
critical_path = []  # Variable para almacenar la ruta crítica
ruta_critica_valor = 0  # Valor de la ruta crítica

def agregar_nodo(entry_nodo, entry_optimista, entry_probable, entry_pesimista, entry_predecesores, lista_nodos):
    nodo = entry_nodo.get()
    optimista = int(entry_optimista.get())
    probable = int(entry_probable.get())
    pesimista = int(entry_pesimista.get())
    predecesores = entry_predecesores.get().split(',') if entry_predecesores.get() else []  # Obtener predecesores como una lista separada por comas

    nodos.append((nodo, optimista, probable, pesimista, predecesores))
    
    # Agregar el nodo al grafo
    grafo.add_node(nodo)
    
    entry_nodo.delete(0, tk.END)
    entry_optimista.delete(0, tk.END)
    entry_probable.delete(0, tk.END)
    entry_pesimista.delete(0, tk.END)
    entry_predecesores.delete(0, tk.END)
    mostrar_nodos(lista_nodos)

def generar_grafo_pert():
    global critical_path, ruta_critica_valor
    grafo.clear()

    for nodo, _, _, _, predecesores in nodos:
        grafo.add_node(nodo)
        for predecesor in predecesores:
            grafo.add_edge(predecesor.strip(), nodo.strip())

    critical_path = calcular_ruta_critica_pert()
    dibujar_grafo()

def calcular_ruta_critica_pert():
    for nodo in grafo.nodes():
        grafo.nodes[nodo]['tiempo_esperado'] = 0

    # Inicializar los tiempos esperados de los nodos hoja (sin predecesores)
    for nodo_data in nodos:
        nodo_id, optimista, probable, pesimista, predecesores = nodo_data
        if not predecesores:
            tiempo_esperado = (optimista + 4 * probable + pesimista) / 6
            grafo.nodes[nodo_id]['tiempo_esperado'] = tiempo_esperado

    # Calcular los tiempos esperados para el resto de los nodos
    calcular_ruta = True
    while calcular_ruta:
        calcular_ruta = False
        for nodo_data in nodos:
            nodo_id, optimista, probable, pesimista, predecesores = nodo_data
            if predecesores:
                max_tiempo_esperado = max([grafo.nodes[pred].get('tiempo_esperado', 0) for pred in predecesores])
                tiempo_esperado = (optimista + 4 * probable + pesimista) / 6
                if grafo.nodes[nodo_id].get('tiempo_esperado', 0) != max_tiempo_esperado + tiempo_esperado:
                    grafo.nodes[nodo_id]['tiempo_esperado'] = max_tiempo_esperado + tiempo_esperado
                    calcular_ruta = True

    critical_path = nx.dag_longest_path(grafo)
    return critical_path


def mostrar_valor_ruta_critica():
    global ruta_critica_valor

    for nodo_id in critical_path:
        nodo_data = next((n for n in nodos if n[0] == nodo_id), None)
        if nodo_data:
            optimista, probable, pesimista = nodo_data[1:4]
            tiempo_esperado = (optimista + 4 * probable + pesimista) / 6
            ruta_critica_valor += tiempo_esperado

    dibujar_grafo()


def mostrar_nodos(lista_nodos):
    lista_nodos.delete(0, tk.END)
    for nodo_data in nodos:
        nodo, optimista, probable, pesimista, predecesores = nodo_data
        lista_nodos.insert(tk.END, f"Nodo: {nodo}, Tiempo Optimista: {optimista}, Tiempo Probable: {probable}, Tiempo Pesimista: {pesimista}, Predecesores: {', '.join(predecesores)}")

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
    global ruta_critica_valor
    for nodo_id in critical_path:
        nodo_data = next((n for n in nodos if n[0] == nodo_id), None)
        if nodo_data:
            optimista, probable, pesimista = nodo_data[1:4]
            tiempo_esperado = (optimista + 4 * probable + pesimista) / 6
            ruta_critica_valor += tiempo_esperado

    # Obtener la posición del último nodo en la ruta crítica
    if critical_path:
        last_node = critical_path[-1]
        x, y = pos[last_node]

        # Mostrar el valor de la ruta crítica en el último nodo de la ruta
        plt.text(x, y - 0.1, f"Valor de la ruta crítica: {ruta_critica_valor}", fontsize=10, ha='center', bbox=dict(facecolor='white', alpha=0.8))

    if 'label_ruta_critica' in globals():
        label_ruta_critica.destroy()

    label_ruta_critica = tk.Label(ventana_pert, text=f"Valor de la ruta crítica: {ruta_critica_valor}", font=("Arial", 12))
    label_ruta_critica.pack()

def reset_variables_pert():
    global nodos, grafo, critical_path, ruta_critica_valor
    nodos = []
    grafo = nx.DiGraph()
    critical_path = []
    ruta_critica_valor = 0
    ventana_pert.destroy()  # Cierra la ventana de PERT

def ventana_pert():
    global ventana_pert
    ventana_pert = tk.Tk()
    ventana_pert.title("Datos para pert")
    ventana_pert.geometry("800x600")

    label_nodo = tk.Label(ventana_pert, text="Nodo:")
    label_nodo.pack()

    entry_nodo = tk.Entry(ventana_pert)
    entry_nodo.pack()

    label_optimista = tk.Label(ventana_pert, text="Tiempo Optimista:")
    label_optimista.pack()

    entry_optimista = tk.Entry(ventana_pert)
    entry_optimista.pack()

    label_probable = tk.Label(ventana_pert, text="Tiempo más Probable:")
    label_probable.pack()

    entry_probable = tk.Entry(ventana_pert)
    entry_probable.pack()

    label_pesimista = tk.Label(ventana_pert, text="Tiempo Pesimista:")
    label_pesimista.pack()

    entry_pesimista = tk.Entry(ventana_pert)
    entry_pesimista.pack()

    label_predecesores = tk.Label(ventana_pert, text="Predecesores (separados por coma):")
    label_predecesores.pack()

    entry_predecesores = tk.Entry(ventana_pert)
    entry_predecesores.pack()

    lista_nodos = tk.Listbox(ventana_pert)
    lista_nodos.pack()

    boton_agregar = tk.Button(ventana_pert, text="Agregar Nodo", command=lambda: agregar_nodo(entry_nodo, entry_optimista, entry_probable, entry_pesimista, entry_predecesores, lista_nodos))
    boton_agregar.pack()

    boton_generar_grafo = tk.Button(ventana_pert, text="Generar Grafo", command=generar_grafo_pert)
    boton_generar_grafo.pack()

    boton_salir = tk.Button(ventana_pert, text="Salir", command=reset_variables_pert)
    boton_salir.pack()

    global frame_grafo
    frame_grafo = tk.Frame(ventana_pert)
    frame_grafo.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    label_ruta_critica = tk.Label(ventana_pert, text=f"Valor de la ruta crítica: {ruta_critica_valor}", font=("Arial", 12))
    label_ruta_critica.pack()



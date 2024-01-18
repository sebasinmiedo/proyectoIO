import tkinter as tk
from tkinter import ttk
from fractions import Fraction

def ventana_DT():
    cantidad_criterios = 0
    matriz_criterios = []
    matrices_alternativas = []

    def generar_tablas():
        nonlocal cantidad_criterios, matriz_criterios, matrices_alternativas
        cantidad_criterios = int(entry_criterios.get())

        label_criterios.grid_forget()
        entry_criterios.grid_forget()
        boton_generar_tablas.grid_forget()

        # Crear espacio para la matriz de criterios
        for i in range(cantidad_criterios):
            fila = []
            for j in range(cantidad_criterios):
                label = tk.Label(frame_matrices, text=f"{i+1}; {j+1}:")
                label.grid(row=i+3, column=2*j)
                valor = tk.Entry(frame_matrices)
                valor.grid(row=i+3, column=2*j+1)
                fila.append(valor)
            matriz_criterios.append(fila)

        # Crear espacio para las matrices de alternativas
        for k in range(cantidad_criterios):
            matrices_alternativas.append([])
            for i in range(cantidad_criterios):
                fila = []
                for j in range(cantidad_criterios):
                    label = tk.Label(frame_matrices, text=f"A{k+1} - {i+1}; {j+1}:")
                    label.grid(row=i+3+(k+1)*cantidad_criterios, column=2*j)
                    valor = tk.Entry(frame_matrices)
                    valor.grid(row=i+3+(k+1)*cantidad_criterios, column=2*j+1)
                    fila.append(valor)
                matrices_alternativas[k].append(fila)

        boton_calcular = tk.Button(frame_matrices, text="Calcular", command=calcular_decision)
        boton_calcular.grid(row=(cantidad_criterios+1)*(cantidad_criterios+1), columnspan=2*cantidad_criterios)

    def calcular_decision():
        valores_criterios = obtener_valores(matriz_criterios)
        suma_columnas_criterios = [sum(columna) for columna in zip(*valores_criterios)]

        matriz_ponderada_criterios = []
        for fila in valores_criterios:
            fila_ponderada = [round(valor / suma, 3) for valor, suma in zip(fila, suma_columnas_criterios)]
            matriz_ponderada_criterios.append(fila_ponderada)

        vector_propio_criterios = calcular_vector_propio(matriz_ponderada_criterios)

        matrices_ponderadas_alternativas = []
        vectores_propios_alternativas = []

        for k in range(cantidad_criterios):
            valores_alternativas = obtener_valores(matrices_alternativas[k])
            suma_columnas_alternativas = [sum(columna) for columna in zip(*valores_alternativas)]

            matriz_ponderada_alternativas = []
            for fila in valores_alternativas:
                fila_ponderada = [round(valor / suma, 3) for valor, suma in zip(fila, suma_columnas_alternativas)]
                matriz_ponderada_alternativas.append(fila_ponderada)

            vector_propio_alternativas = calcular_vector_propio(matriz_ponderada_alternativas)

            matrices_ponderadas_alternativas.append(matriz_ponderada_alternativas)
            vectores_propios_alternativas.append(vector_propio_alternativas)

        matriz_vectores_propios_alternativas = list(zip(*vectores_propios_alternativas))

        resultado_producto = [[round(sum(a*b for a, b in zip(fila, vector_propio_criterios)), 3)] for fila in matriz_vectores_propios_alternativas]

        vector_A = [round(sum(a * b for a, b in zip(fila, vector_propio_criterios)), 3) for fila in matriz_ponderada_criterios]
        vector_division = [round(a / b, 3) for a, b in zip(vector_A, vector_propio_criterios)]
        promedio_division = round(sum(vector_division) / len(vector_division), 3)

        resultado_frame = tk.Frame(ventana)
        resultado_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        canvas = tk.Canvas(resultado_frame)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar_vertical = ttk.Scrollbar(resultado_frame, orient="vertical", command=canvas.yview)
        scrollbar_vertical.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar_vertical.set)

        scrollbar_horizontal = ttk.Scrollbar(resultado_frame, orient="horizontal", command=canvas.xview)
        scrollbar_horizontal.pack(side="bottom", fill="x")
        canvas.configure(xscrollcommand=scrollbar_horizontal.set)

        interior_frame = tk.Frame(canvas)
        interior_frame_id = canvas.create_window((0, 0), window=interior_frame, anchor="nw")

        canvas.bind("<Configure>", lambda event, canvas=canvas: on_configure(event, canvas))

        mostrar_matriz(interior_frame, "Matriz Ponderada Criterios", matriz_ponderada_criterios)
        mostrar_matriz(interior_frame, "Resultado del producto", resultado_producto)
        mostrar_matriz(interior_frame, "Vector A", [vector_A])
        mostrar_matriz(interior_frame, "Vector A / Vector propio", [vector_division])

        n = cantidad_criterios
        IC = (promedio_division - n) / (n - 1)
        IA = (1.98 * (n - 2)) / n
        RC = round(IC / IA, 3)

        resultado_label = tk.Label(interior_frame, text=f"Razón de consistencia: {RC}")
        resultado_label.grid(row=len(interior_frame.winfo_children()), columnspan=2)

    def on_configure(event, canvas):
        canvas.configure(scrollregion=canvas.bbox("all"))

    def obtener_valores(matriz):
        valores = []
        for fila in matriz:
            valores_fila = []
            for entry in fila:
                valor = entry.get()
                if valor.strip() == "":
                    tk.messagebox.showerror("Error", "Por favor, complete todos los valores.")
                    return
                valores_fila.append(Fraction(valor))
            valores.append(valores_fila)
        return valores

    def calcular_vector_propio(matriz_ponderada):
        return [round(sum(fila) / len(fila), 3) for fila in matriz_ponderada]

    def mostrar_matriz(frame, titulo, matriz):
        label_titulo = tk.Label(frame, text=titulo)
        label_titulo.grid(row=len(frame.winfo_children()), columnspan=2)

        for i in range(len(matriz)):
            for j in range(len(matriz[i])):
                tk.Label(frame, text=matriz[i][j]).grid(row=len(frame.winfo_children()), column=j)

    ventana = tk.Tk()
    ventana.title("Toma de decisiones")

    label_criterios = tk.Label(ventana, text="Cantidad de criterios:")
    label_criterios.grid(row=1, column=1)

    entry_criterios = tk.Entry(ventana)
    entry_criterios.grid(row=1, column=2)

    boton_generar_tablas = tk.Button(ventana, text="Generar Tablas", command=generar_tablas)
    boton_generar_tablas.grid(row=2, columnspan=2)

    frame_matrices = tk.Frame(ventana)
    frame_matrices.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

    ventana.mainloop()

# Llamar a ventana_DT() desde otro archivo para ejecutar la interfaz y los cálculos

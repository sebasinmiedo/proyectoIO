import tkinter as tk
from fractions import Fraction

def ventana_DT():
    cantidad_criterios = 0
    matriz_criterios = []

    def generar_tablas():
        nonlocal cantidad_criterios, matriz_criterios
        cantidad_criterios = int(entry_criterios.get())

        label_criterios.grid_forget()
        entry_criterios.grid_forget()
        boton_generar_tablas.grid_forget()

        for i in range(cantidad_criterios):
            fila = []
            for j in range(cantidad_criterios):
                label = tk.Label(ventana, text=f"{i+1}; {j+1}:")
                label.grid(row=i+3, column=2*j)
                valor = tk.Entry(ventana)
                valor.grid(row=i+3, column=2*j+1)
                fila.append(valor)
            matriz_criterios.append(fila)

        boton_calcular = tk.Button(ventana, text="Calcular", command=calcular_decision)
        boton_calcular.grid(row=cantidad_criterios+4, columnspan=2*cantidad_criterios)

    def calcular_decision():
        valores_criterios = []
        for fila in matriz_criterios:
            valores_fila = []
            for entry in fila:
                valor = entry.get()
                if valor.strip() == "":
                    tk.messagebox.showerror("Error", "Por favor, complete todos los valores.")
                    return
                valores_fila.append(Fraction(valor))
            valores_criterios.append(valores_fila)

        suma_columnas = [sum(columna) for columna in zip(*valores_criterios)]

        matriz_ponderada = []
        for fila in valores_criterios:
            fila_ponderada = [round(valor / suma, 2) for valor, suma in zip(fila, suma_columnas)]
            matriz_ponderada.append(fila_ponderada)

        vector_propio = [round(sum(fila) / len(fila), 2) for fila in matriz_ponderada]

        imprimir_matriz(matriz_ponderada)
        
        resultado_producto = [[round(sum(a*b for a, b in zip(fila, vector_propio)), 2)] for fila in matriz_ponderada]
        print("\nResultado del producto de la matriz ponderada por el vector propio:")
        imprimir_matriz(resultado_producto)
        
        resultado_division = [[round(a / b, 2)] for a, b in zip([fila[0] for fila in resultado_producto], vector_propio)]
        print("\nResultado de la división del producto entre el vector propio:")
        imprimir_matriz(resultado_division)
        
        promedio_division = sum([fila[0] for fila in resultado_division]) / len(resultado_division)
        print(f"\nPromedio de los valores de la división: {round(promedio_division, 2)}")

    def imprimir_matriz(matriz):
        for i in range(len(matriz)):
            for j in range(len(matriz[i])):
                print(matriz[i][j], end="\t")
            print()

    ventana = tk.Tk()
    ventana.title("Toma de decisiones")

    label_criterios = tk.Label(ventana, text="Cantidad de criterios:")
    label_criterios.grid(row=1, column=1)

    entry_criterios = tk.Entry(ventana)
    entry_criterios.grid(row=1, column=2)

    boton_generar_tablas = tk.Button(ventana, text="Generar Tablas", command=generar_tablas)
    boton_generar_tablas.grid(row=2, columnspan=2)

    ventana.mainloop()

# Llamar a ventana_DT() desde otro archivo para ejecutar la interfaz y los cálculos

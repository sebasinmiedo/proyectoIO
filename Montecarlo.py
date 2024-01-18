import pandas as pd
import random
import tkinter as tk
from tkinter import ttk

filas = 0
entry_consultas = []
entradas_consultas = []
frecuencias = []
tabla_frame = None

def generar_numeros_aleatorios(n):
    numeros_aleatorios = [random.random() for _ in range(n)]
    return numeros_aleatorios

def obtener_consulta(numero_aleatorio, df):
    for i, (limite_inferior, limite_superior) in enumerate(zip(df['Límite Inferior'], df['Límite Superior'])):
        if limite_inferior <= numero_aleatorio < limite_superior:
            return df['Consultas'].iloc[i]

def limpiar_ventana():
    # Destruir todas las entradas anteriores
    for entry in entradas_consultas:
        entry.destroy()

def generar_frecuencias():
    global filas, frecuencias
    try:
        # Limpiar la lista de frecuencias
        frecuencias.clear()

        # Obtener las frecuencias ingresadas
        for entry in entry_consultas:
            dato = entry.get()
            try:
                dato = int(dato)
                if dato < 0:
                    print("¡Error! Ingrese un valor entero no negativo para la frecuencia.")
                else:
                    frecuencias.append(dato)
            except ValueError:
                print("¡Error! Ingrese un valor entero para la frecuencia.")

        print("Frecuencias generadas:", frecuencias)

        # Crear la tabla
        crear_tabla()

    except Exception as e:
        print(f"Error al generar frecuencias: {e}")

def simular_montecarlo():
    global filas, frecuencias
    try:
        # Obtener el número de filas desde la interfaz
        filas = int(entry_filas.get())

        # Listas para almacenar los datos
        consultas = []
        entry_consultas.clear()  # Limpiar la lista de entry_consultas
        entradas_consultas.clear()  # Limpiar la lista de entradas_consultas

        # Solicitar datos de manera interactiva
        for i in range(filas):
            label_consulta = ttk.Label(root, text=f"Consulta {i}:")
            label_consulta.grid(column=0, row=i + 4, padx=10, pady=5)

            entry_consulta = ttk.Entry(root)
            entry_consulta.grid(column=1, row=i + 4, padx=10, pady=5)

            entry_consultas.append(entry_consulta)
            entradas_consultas.append(entry_consulta)

        # Resto del código aquí...

    except Exception as e:
        print(f"Error en la simulación: {e}")

def crear_tabla():
    global tabla_frame, filas, frecuencias
    # Destruir la tabla anterior si existe
    if tabla_frame:
        tabla_frame.destroy()

    # Crear un DataFrame con las columnas especificadas
    df = pd.DataFrame({'Consultas': [f"Consulta {i}" for i in range(filas)], 'Frecuencia': frecuencias})

    # Calcular la Frecuencia acumulativa y Frecuencia relativa
    df['Frecuencia Acumulativa'] = df['Frecuencia'].cumsum()
    df['Probabilidad de Ocurrencia'] = df['Frecuencia'] / df['Frecuencia'].sum()
    df['Probabilidad de Ocurrencia Acumulada'] = df['Probabilidad de Ocurrencia'].cumsum()

    # Calcular límites (ajustados según tus necesidades)
    df['Límite Inferior'] = [0] + list(df['Probabilidad de Ocurrencia Acumulada'][:-1])
    df['Límite Superior'] = df['Probabilidad de Ocurrencia Acumulada']

    # Crear el frame para la tabla
    tabla_frame = ttk.Frame(root)
    tabla_frame.grid(column=2, row=0, rowspan=100, padx=10, pady=10)

    # Crear el Treeview (tabla)
    tabla = ttk.Treeview(tabla_frame, columns=list(df.columns), show='headings', height=15)

    # Configurar encabezados
    for col in df.columns:
        tabla.heading(col, text=col)

    # Insertar datos en la tabla
    for i, row in df.iterrows():
        tabla.insert("", "end", values=list(row))

    # Configurar el scroll
    scroll_y = ttk.Scrollbar(tabla_frame, orient="vertical", command=tabla.yview)
    tabla.configure(yscroll=scroll_y.set)

    # Mostrar la tabla
    tabla.grid(row=0, column=0, sticky='nsew')
    scroll_y.grid(row=0, column=1, sticky='ns')

# Crear la ventana principal
root = tk.Tk()
root.title("Simulación Montecarlo")

# Crear y colocar widgets en la ventana
label_filas = ttk.Label(root, text="Número de filas:")
label_filas.grid(column=0, row=0, padx=10, pady=10)

entry_filas = ttk.Entry(root)
entry_filas.grid(column=1, row=0, padx=10, pady=10)

label_numeros_aleatorios = ttk.Label(root, text="Número de aleatorios:")
label_numeros_aleatorios.grid(column=0, row=1, padx=10, pady=10)

entry_numeros_aleatorios = ttk.Entry(root)
entry_numeros_aleatorios.grid(column=1, row=1, padx=10, pady=10)

# Botón para simular
button_simular = ttk.Button(root, text="Simular", command=simular_montecarlo)
button_simular.grid(column=0, row=2, columnspan=2, pady=10)

# Botón para generar frecuencias
button_generar = ttk.Button(root, text="Generar", command=generar_frecuencias)
button_generar.grid(column=0, row=3, columnspan=2, pady=10)

# Variable para mostrar el resultado
resultado_texto = tk.StringVar()
label_resultado = ttk.Label(root, textvariable=resultado_texto)
label_resultado.grid(column=0, row=4, columnspan=2, pady=10)

# Inicializar la interfaz gráfica
root.mainloop()

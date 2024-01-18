import tkinter as tk
from tkinter import messagebox
from CPM import *
from PERT import *
from DT import *
from EOQ import *
from TColas import *

# Funciones para cada modelo
def abrir_ventana_cpm():
    ventana_cpm()

def abrir_ventana_pert():
    ventana_pert()

def abrir_ventana_eoq():
    ventana_inventario()

def abrir_ventana_decisiones():
    ventana_DT()

def abrir_ventana_tcolas():
    ventana_tcolas()

# Nuevas funciones para los botones adicionales
def abrir_ventana_simulacion():
    # Agrega aquí la lógica para la simulación de MonteCarlo
    pass

def abrir_ventana_programacion_cuadratica():
    # Agrega aquí la lógica para la programación cuadrática
    pass

# Función para salir del programa
def salir():
    respuesta = messagebox.askyesno("Salir", "¿Seguro que quieres salir?")
    if respuesta:
        ventana.destroy()

# Configuración de la ventana principal
ventana = tk.Tk()
ventana.title("Menú de Modelos de Investigación Operativa II")
ventana.geometry("600x700")
ventana.configure(bg='#E0E0E0')  # Cambia el color de fondo de la ventana

# Estilo para los botones
estilo_boton = {
    "font": ("Arial", 14),
    "width": 30,
    "height": 2,
    "bg": '#4CAF50',  # Cambia el color de fondo de los botones
    "fg": 'white',    # Cambia el color del texto de los botones
    "borderwidth": 2,
    "relief": 'raised'
}

# Botones para los modelos existentes
boton_cpm = tk.Button(ventana, text="CPM", command=abrir_ventana_cpm, **estilo_boton)
boton_cpm.pack(pady=10)

boton_pert = tk.Button(ventana, text="PERT", command=abrir_ventana_pert, **estilo_boton)
boton_pert.pack(pady=10)

boton_eoq = tk.Button(ventana, text="EOQ", command=abrir_ventana_eoq, **estilo_boton)
boton_eoq.pack(pady=10)

boton_decisiones = tk.Button(ventana, text="Teoría de Decisiones", command=abrir_ventana_decisiones, **estilo_boton)
boton_decisiones.pack(pady=10)

boton_tcolas = tk.Button(ventana, text="Teoría de Colas", command=abrir_ventana_tcolas, **estilo_boton)
boton_tcolas.pack(pady=10)

# Nuevos botones
boton_simulacion = tk.Button(ventana, text="Simulación de MonteCarlo", command=abrir_ventana_simulacion, **estilo_boton)
boton_simulacion.pack(pady=10)

boton_programacion_cuadratica = tk.Button(ventana, text="Programación Cuadrática", command=abrir_ventana_programacion_cuadratica, **estilo_boton)
boton_programacion_cuadratica.pack(pady=10)

# Botón para salir del programa
boton_salir = tk.Button(ventana, text="Salir", command=salir, **estilo_boton)
boton_salir.pack(pady=10)

# Ejecutar la ventana
ventana.mainloop()

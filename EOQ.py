import tkinter as tk

def ventana_inventario():
    def calcular_inventario(demanda_anual, costo_mantener, costo_unitario, costo_pedido, tiempo_atender_pedido, dias_laborales):
        EOQ = ((2 * demanda_anual * costo_pedido) / costo_mantener) ** 0.5
        num_pedidos_por_periodo = demanda_anual / EOQ
        tiempo_entre_pedidos = dias_laborales / num_pedidos_por_periodo
        punto_reorden = (demanda_anual / dias_laborales) * tiempo_atender_pedido

        costos = {
            "Cantidad Económica de Pedido": EOQ,
            "Número de Pedidos por Período": num_pedidos_por_periodo,
            "Tiempo entre Pedidos (días)": tiempo_entre_pedidos,
            "Punto de Reorden": punto_reorden,
            "Costo Total": (demanda_anual * costo_unitario) + ((demanda_anual / EOQ) * costo_pedido) + ((EOQ / 2) * costo_mantener)
        }

        return costos

    def obtener_inputs():
        demanda_anual = float(entry_demanda_anual.get())
        costo_mantener = float(entry_costo_mantener.get())
        costo_unitario = float(entry_costo_unitario.get())
        costo_pedido = float(entry_costo_pedido.get())
        tiempo_atender_pedido = float(entry_tiempo_atender_pedido.get())
        dias_laborales = float(entry_dias_laborales.get())

        costos_inventario = calcular_inventario(demanda_anual, costo_mantener, costo_unitario, costo_pedido, tiempo_atender_pedido, dias_laborales)
        mostrar_resultados(costos_inventario)

    def mostrar_resultados(costos):
        resultados_texto = ""
        for key, value in costos.items():
            resultados_texto += f"{key}: {value}\n"

        resultado_text.delete(1.0, tk.END)
        resultado_text.insert(tk.END, resultados_texto)

    def resetear_valores():
        entry_demanda_anual.delete(0, tk.END)
        entry_costo_mantener.delete(0, tk.END)
        entry_costo_unitario.delete(0, tk.END)
        entry_costo_pedido.delete(0, tk.END)
        entry_tiempo_atender_pedido.delete(0, tk.END)
        entry_dias_laborales.delete(0, tk.END)
        resultado_text.delete(1.0, tk.END)

    ventana_inventario = tk.Tk()
    ventana_inventario.title("Cálculo de Inventarios")

    label_demanda_anual = tk.Label(ventana_inventario, text="Demanda Anual:")
    label_demanda_anual.pack()

    entry_demanda_anual = tk.Entry(ventana_inventario)
    entry_demanda_anual.pack()

    label_costo_mantener = tk.Label(ventana_inventario, text="Costo por Mantener:")
    label_costo_mantener.pack()

    entry_costo_mantener = tk.Entry(ventana_inventario)
    entry_costo_mantener.pack()

    label_costo_unitario = tk.Label(ventana_inventario, text="Costo Unitario:")
    label_costo_unitario.pack()

    entry_costo_unitario = tk.Entry(ventana_inventario)
    entry_costo_unitario.pack()

    label_costo_pedido = tk.Label(ventana_inventario, text="Costo por Pedido:")
    label_costo_pedido.pack()

    entry_costo_pedido = tk.Entry(ventana_inventario)
    entry_costo_pedido.pack()

    label_tiempo_atender_pedido = tk.Label(ventana_inventario, text="Tiempo para Atender Pedido:")
    label_tiempo_atender_pedido.pack()

    entry_tiempo_atender_pedido = tk.Entry(ventana_inventario)
    entry_tiempo_atender_pedido.pack()

    label_dias_laborales = tk.Label(ventana_inventario, text="Días Laborales:")
    label_dias_laborales.pack()

    entry_dias_laborales = tk.Entry(ventana_inventario)
    entry_dias_laborales.pack()

    boton_calcular = tk.Button(ventana_inventario, text="Calcular", command=obtener_inputs)
    boton_calcular.pack()

    resultado_text = tk.Text(ventana_inventario, height=10, width=40)
    resultado_text.pack()

    boton_salir = tk.Button(ventana_inventario, text="Salir", command=ventana_inventario.destroy)
    boton_salir.pack()

    ventana_inventario.mainloop()

# Si deseas llamar esta función desde otro archivo, simplemente importa este archivo y llama a ventana_inventario():
# Ejemplo:
# from nombre_de_tu_archivo import ventana_inventario
# ventana_inventario()

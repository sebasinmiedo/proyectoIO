import tkinter as tk
def ventana_tcolas():
    def abrir_ventana_MM1():
        ventana_MM1()

    def abrir_ventana_MG1():
        ventana_MG1()

    def ventana_MM1():
        def Calcular(lambda_t,mu_t,clientes):
            lambda_r=round(lambda_t/60,2)
            mu_r=round(mu_t/60,2)
            Ls=round((lambda_r)/(mu_r-lambda_r),2)
            Ws=round((1)/(mu_r-lambda_r),2)
            Wq=round((lambda_r)/(mu_r*(mu_r-lambda_r)),2)
            Lq=round(lambda_r*Wq,2)
            p=round((lambda_r/mu_r),2)
            pc=round((1-(lambda_r/mu_r)),2)
            pn=round((1-(lambda_r/mu_r))*((lambda_r/mu_r)**clientes) ,2)
            resultados = {
                    "Parametro λ en minutos":lambda_r,
                    "Parametro ρ en minutos":mu_r,
                    "Cantidad de clientes en el sistema (Ls)": Ls,
                    "Tiempo promedio de un cliente en el sistema (Ws)": Ws,
                    "Numero promedio de clientes en la fila (Lq)": Lq,
                    "Tiempo promedio que pasa un cliente en la file (Wq)": Wq,
                    "Factor de uso del sistema (ρ)":"{:.2%}".format(p),
                    "Porcentaje de tiempo inactivo(ρ0)": "{:.2%}".format(pc),
                    "Probabilidad que el sistema tenga "+ str(clientes)+" clientes": "{:.2%}".format(pn)
            }
            return resultados
    
        def obtener_inputs():
            lambda_t = int(entry_lambda.get())
            mu_t = int(entry_mu.get())
            clientes = int(entry_clientes.get())
            resultados_1 = Calcular(lambda_t,mu_t,clientes)
            mostrar_resultados(resultados_1)

        def mostrar_resultados(resultados):
            resultados_texto = ""
            for key, value in resultados.items():
                resultados_texto += f"{key}: {value}\n"
            resultado_text.delete(1.0, tk.END)
            resultado_text.insert(tk.END, resultados_texto)

        def resetear_valores():
            entry_lambda.delete(0, tk.END)
            entry_mu.delete(0, tk.END)
            entry_clientes.delete(0, tk.END)
            ventana_MM1_a = tk.Tk()
            ventana_MM1_a.title("Modelo M/M/1")
        ventana_MM1_a = tk.Tk()
        ventana_MM1_a.title("M/M/1")
        ventana_MM1_a.geometry("550x550")

        label_Titulo = tk.Label(ventana_MM1_a, text="MODELO M/M/1")
        label_Titulo.pack()
        #PARAMETRO LAMBDA
        label_lambda = tk.Label(ventana_MM1_a, text="Parametro λ :")
        label_lambda.pack()
        entry_lambda = tk.Entry(ventana_MM1_a)
        entry_lambda.pack()
        #PARAMETRO MU
        label_mu = tk.Label(ventana_MM1_a, text="Parametro µ:")
        label_mu.pack()
        entry_mu = tk.Entry(ventana_MM1_a)
        entry_mu.pack()
        #PARAMETRO N clientes
        label_clientes = tk.Label(ventana_MM1_a, text="# Clientes:")
        label_clientes.pack()
        entry_clientes = tk.Entry(ventana_MM1_a)
        entry_clientes.pack()
        
        boton_calcular = tk.Button(ventana_MM1_a, text="Calcular", command=obtener_inputs)
        boton_calcular.pack()
        resultado_text = tk.Text(ventana_MM1_a, height=20, width=50)
        resultado_text.pack()
        boton_salir = tk.Button(ventana_MM1_a, text="Salir", command=ventana_MM1_a.destroy)
        boton_salir.pack()
        ventana_MM1_a.mainloop()

    def ventana_MG1():

        def Calcular(lambda_t,mu_t,desvt):
            lambda_r=round(lambda_t/60,2)
            mu_r=round(mu_t/60,2)
            pc=round(1-(lambda_r/mu_r),2)
            Lq=round((((lambda_r**2)*(desvt**2)+((lambda_r/mu_r)**2))/(2*(1-(lambda_r/mu_r)))),2)
            Ls=round(Lq+(lambda_r/mu_r),2)
            Wq=round(Lq/lambda_r,2)
            Ws=round(Wq+(1/mu_r),2)
            Pw=round(lambda_r/mu_r,2)
            resultados = {
                    "Parametro λ en minutos":lambda_r,
                    "Parametro ρ en minutos":mu_r,
                    "Lq con desviacion estandar de"+ str(desvt)+" ": Lq,
                    "Ls": Ls,
                    "Wq": Wq,
                    "Ws": Ws,
                    "Factor de uso del sistema (ρ)":"{:.2%}".format(Pw),
                    "Porcentaje de tiempo inactivo(ρ0)": "{:.2%}".format(pc),
            }
            return resultados
    
        def obtener_inputs():
            lambda_t = int(entry_lambda.get())
            mu_t = int(entry_mu.get())
            dest= float(entry_destandar.get())
            resultados_1 = Calcular(lambda_t,mu_t,dest)
            mostrar_resultados(resultados_1)

        def mostrar_resultados(resultados):
            resultados_texto = ""
            for key, value in resultados.items():
                resultados_texto += f"{key}: {value}\n"
            resultado_text.delete(1.0, tk.END)
            resultado_text.insert(tk.END, resultados_texto)

        def resetear_valores():
            entry_lambda.delete(0, tk.END)
            entry_mu.delete(0, tk.END)
            entry_destandar.delete(0, tk.END)
            ventana_MM1_a = tk.Tk()
            ventana_MM1_a.title("Modelo M/G/1")
            
        ventana_MG1_a = tk.Tk()
        ventana_MG1_a.title("M/G/1")
        ventana_MG1_a.geometry("550x550")

        label_Titulo = tk.Label(ventana_MG1_a, text="MODELO M/G/1")
        label_Titulo.pack()
        #PARAMETRO LAMBDA
        label_lambda = tk.Label(ventana_MG1_a, text="Parametro λ :")
        label_lambda.pack()
        entry_lambda = tk.Entry(ventana_MG1_a)
        entry_lambda.pack()
        #PARAMETRO MU
        label_mu = tk.Label(ventana_MG1_a, text="Parametro µ:")
        label_mu.pack()
        entry_mu = tk.Entry(ventana_MG1_a)
        entry_mu.pack()
        #DESVICION ESTANDAR
        label_destandar = tk.Label(ventana_MG1_a, text="Desviación estándar σ:")
        label_destandar.pack()
        entry_destandar = tk.Entry(ventana_MG1_a)
        entry_destandar.pack()
        #VENTANA MG1
        boton_calcular = tk.Button(ventana_MG1_a, text="Calcular", command=obtener_inputs)
        boton_calcular.pack()
        resultado_text = tk.Text(ventana_MG1_a, height=20, width=50)
        resultado_text.pack()
        boton_salir = tk.Button(ventana_MG1_a, text="Salir", command=ventana_MG1_a.destroy)
        boton_salir.pack()
        ventana_MG1_a.mainloop()

    #VENTANA PRINCIPAL TEORIA DE COLAS
    ventana_Elegir = tk.Tk()
    ventana_Elegir.title("Elegir Modelo de Teoria de Colas")
    ventana_Elegir.geometry("500x500")
    
    # Estilo para los botones
    estilo_boton = {"font": ("Arial", 14), "width": 20, "height": 2}

    label_Titulo = tk.Label(ventana_Elegir, text="Elige el tipo de modelo : ")
    label_Titulo.pack()
    # Botones para los modelos
    boton_MM1 = tk.Button(ventana_Elegir, text="M/M/1", command=abrir_ventana_MM1, **estilo_boton)
    boton_MM1.pack(pady=10)

    boton_MG1 = tk.Button(ventana_Elegir, text="M/G/1", command=abrir_ventana_MG1, **estilo_boton)
    boton_MG1.pack(pady=10)

    boton_salir = tk.Button(ventana_Elegir, text="Salir", command=ventana_Elegir.destroy)
    boton_salir.pack()

    ventana_Elegir.mainloop()
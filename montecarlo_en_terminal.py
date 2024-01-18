import pandas as pd
import random

# Número de filas
filas = int(input('Ingrese el número de consultas: '))

# Listas para almacenar los datos
consultas = []
frecuencia = []

# Solicitar datos de manera interactiva
for i in range(filas):
    dato = input(f'Ingrese la consulta {i}: ')
    try:
        dato = int(dato)
        if dato < 0:
            print("¡Error! Ingrese un valor entero no negativo para la frecuencia.")
        else:
            consultas.append(f'{i}')
            frecuencia.append(dato)
    except ValueError:
        print("¡Error! Ingrese un valor entero para la frecuencia.")

# Crear un DataFrame con las columnas especificadas
df = pd.DataFrame({'Consultas': consultas, 'Frecuencia': frecuencia})

# Calcular la Frecuencia acumulativa y Frecuencia relativa
df['Frecuencia Acumulativa'] = df['Frecuencia'].cumsum()
df['Probabilidad de Ocurrencia'] = df['Frecuencia'] / df['Frecuencia'].sum()
df['Probabilidad de Ocurrencia Acumulada'] = df['Probabilidad de Ocurrencia'].cumsum()

# Calcular límites (ajustados según tus necesidades)
df['Límite Inferior'] = [0] + list(df['Probabilidad de Ocurrencia Acumulada'][:-1])
df['Límite Superior'] = df['Probabilidad de Ocurrencia Acumulada']

# Mostrar el DataFrame resultante
print(df)


def generar_numeros_aleatorios(n):
    numeros_aleatorios = [random.random() for _ in range(n)]
    return numeros_aleatorios


def obtener_consulta(numero_aleatorio, df):
    for i, (limite_inferior, limite_superior) in enumerate(zip(df['Límite Inferior'], df['Límite Superior'])):
        if limite_inferior <= numero_aleatorio < limite_superior:
            return df['Consultas'].iloc[i]

# Solicitar al usuario que ingrese la cantidad de números aleatorios a generar
cantidad_numeros_aleatorios = int(input("Ingrese la cantidad de números aleatorios a generar: "))

# Generar números aleatorios y almacenarlos en una lista
lista_resultante = generar_numeros_aleatorios(cantidad_numeros_aleatorios)

# Verificar cada número aleatorio y obtener la consulta correspondiente
consultas_obtenidas = [obtener_consulta(aleatorio, df) for aleatorio in lista_resultante]

# Calcular el promedio de las consultas obtenidas
promedio_consultas = sum(map(int, consultas_obtenidas)) / len(consultas_obtenidas)

# Calcular la demanda esperada diaria
demanda_esperada_diaria = sum(df['Consultas'].astype(int) * df['Frecuencia']) / df['Frecuencia'].sum()

# Mostrar el resultado
print("Consulta obtenida para cada número aleatorio:", consultas_obtenidas)
print("Promedio de las consultas obtenidas:", promedio_consultas)
print("Demanda esperada diaria:", demanda_esperada_diaria)
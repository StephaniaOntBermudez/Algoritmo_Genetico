import numpy as np
import random

# Definir el número de hormigas
num_hormigas = 10

# Definir el número de ciudades
num_ciudades = 5

# Matriz de distancias entre ciudades (cambia esto según tu problema)
distancias = np.array([
    [0, 29, 20, 21, 16],
    [29, 0, 15, 17, 28],
    [20, 15, 0, 28, 18],
    [21, 17, 28, 0, 12],
    [16, 28, 18, 12, 0]
])

# Parámetros del algoritmo
alpha = 1.0  # Influencia de la feromona
beta = 2.0   # Influencia de la distancia
rho = 0.5   # Tasa de evaporación de feromonas

# Inicializar matriz de feromonas
feromonas = np.ones((num_ciudades, num_ciudades))

# Función para calcular la probabilidad de elegir una ciudad
def calcular_probabilidad(ciudad_actual, ciudades_no_visitadas):
    probabilidad = np.zeros(len(ciudades_no_visitadas))
    total = 0
    for i, ciudad in enumerate(ciudades_no_visitadas):
        probabilidad[i] = (feromonas[ciudad_actual][ciudad] ** alpha) / (distancias[ciudad_actual][ciudad] ** beta)
        total += probabilidad[i]
    probabilidad /= total
    return probabilidad

# Función para elegir la próxima ciudad
def elegir_ciudad(ciudad_actual, ciudades_no_visitadas):
    probabilidad = calcular_probabilidad(ciudad_actual, ciudades_no_visitadas)
    return np.random.choice(ciudades_no_visitadas, p=probabilidad)

# Función para calcular la longitud de un recorrido
def calcular_longitud(recorrido):
    longitud = 0
    for i in range(len(recorrido) - 1):
        longitud += distancias[recorrido[i]][recorrido[i + 1]]
    longitud += distancias[recorrido[-1]][recorrido[0]]  # Volver al inicio
    return longitud

# Algoritmo ACO
num_iteraciones = 100
for iteracion in range(num_iteraciones):
    recorridos = []
    for _ in range(num_hormigas):
        ciudad_inicial = random.randint(0, num_ciudades - 1)
        ciudades_no_visitadas = list(range(num_ciudades))
        ciudades_no_visitadas.remove(ciudad_inicial)
        recorrido = [ciudad_inicial]
        while ciudades_no_visitadas:
            ciudad_actual = recorrido[-1]
            siguiente_ciudad = elegir_ciudad(ciudad_actual, ciudades_no_visitadas)
            recorrido.append(siguiente_ciudad)
            ciudades_no_visitadas.remove(siguiente_ciudad)
        recorridos.append(recorrido)

    # Actualizar feromonas
    for i in range(num_ciudades):
        for j in range(i + 1, num_ciudades):
            delta_feromona = 0
            for recorrido in recorridos:
                if (i in recorrido and j in recorrido) or (i == j == recorrido[0]):
                    delta_feromona += 1 / calcular_longitud(recorrido)
            feromonas[i][j] = (1 - rho) * feromonas[i][j] + delta_feromona

# Encontrar el mejor recorrido
mejor_recorrido = min(recorridos, key=calcular_longitud)
print("Mejor recorrido:", mejor_recorrido)
print("Longitud del mejor recorrido:", calcular_longitud(mejor_recorrido))

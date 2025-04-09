# Importar el módulo random para generar números aleatorios
import random
# Importar el módulo time para medir el tiempo de ejecución
import time

# Definir función para crear una matriz de números aleatorios
def generar_matriz(filas, columnas):
    # Retornar una matriz usando comprensión de listas anidadas:
    # - La lista externa crea 'filas' elementos
    # - Cada fila es una lista de 'columnas' números aleatorios entre 0 y 100
    return [[random.randint(0, 100) for _ in range(columnas)] for _ in range(filas)]

# Definir función para contar números pares en una matriz
def contar_pares(matriz):
    # Inicializar contador de números pares en 0
    conteo = 0
    
    # Recorrer cada fila de la matriz
    for fila in matriz:
        # Recorrer cada elemento (valor) dentro de la fila
        for valor in fila:
            # Verificar si el valor es par (divisible por 2 sin residuo)
            if valor % 2 == 0:
                # Incrementar el contador si es par
                conteo += 1
    # Retornar el total de números pares encontrados
    return conteo

# Definir tamaño de la matriz (100 filas x 100 columnas)
filas, columnas = 100, 100

# Generar la matriz llamando a la función generar_matriz
matriz = generar_matriz(filas, columnas)

# Registrar el tiempo de inicio antes de contar los pares
inicio = time.time()

# Llamar a la función para contar los números pares en la matriz
resultado = contar_pares(matriz) 

# Registrar el tiempo de finalización después de contar los pares
fin = time.time()

# Mostrar el resultado del conteo de números pares
print(f"Números pares: {resultado}")

# Mostrar el tiempo transcurrido (diferencia entre fin e inicio)
# Formateado a 6 decimales para mayor precisión
print(f"Tiempo de ejecución: {fin - inicio:.6f} segundos")
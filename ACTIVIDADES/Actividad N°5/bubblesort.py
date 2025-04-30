import time  # Importa el módulo time para medir el tiempo de ejecución
import random  # Importa random para generar números aleatorios

# Algoritmo Bubble Sort
def bubble_sort(arr):
    n = len(arr)  # Obtiene el tamaño del arreglo (lista)
    for i in range(n - 1):  # Bucle externo: hace n-1 pasadas
         # Medir tiempo al inicio de la pasada
        pasada_inicio = time.time()
        for j in range(n - i - 1):  # Bucle interno: compara elementos no ordenados
            if arr[j] > arr[j + 1]:  # Si el actual es mayor que el siguiente
                arr[j], arr[j + 1] = arr[j + 1], arr[j]  # Intercambia los elementos
        # Medir tiempo al final de la pasada
        pasada_fin = time.time()

        # Mostrar estado y duración de la pasada
        print(f"Pasada {i + 1}: {arr} - Duración: {pasada_fin - pasada_inicio:.6f} segundos")

# Función para probar Bubble Sort con un arreglo y medir su tiempo
def probar_bubble_sort(nombre, arreglo):
    copia = arreglo.copy()  # Crea una copia para no modificar el arreglo original
    inicio = time.time()  # Marca el inicio de la ejecución
    bubble_sort(copia)  # Aplica el algoritmo de ordenamiento
    fin = time.time()  # Marca el final
    print(f"{nombre} - Tiempo: {fin - inicio:.6f} segundos")  # Muestra el tiempo tomado

# 1. Lista de 1000 números aleatorios entre 1 y 10000
aleatorio = [random.randint(1, 10000) for _ in range(1000)]

# 2. Lista ordenada de menor a mayor (mejor caso para algunos algoritmos)
ordenado = sorted(aleatorio)  # 'sorted()' es una función de Python que devuelve una nueva lista ordenada

# 3. Lista ordenada de mayor a menor (peor caso para Bubble Sort, por ejemplo)
inverso = sorted(aleatorio, reverse=True)  # Ordena al revés con reverse=True

# Ejecuta la prueba con los tres tipos de lista
probar_bubble_sort("Aleatorio", aleatorio)
probar_bubble_sort("Ordenado", ordenado)
probar_bubble_sort("Inverso", inverso)

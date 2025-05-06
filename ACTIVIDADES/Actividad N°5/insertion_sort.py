import random
import time

# Algoritmo Insertion Sort
def insertion_sort(arr):
    for i in range(1, len(arr)):  # Comenzar desde el segundo elemento
        key = arr[i]  # Valor actual a insertar
        j = i - 1  # Comparar con elementos anteriores
        while j >= 0 and arr[j] > key:  # Mientras haya elementos mayores
            arr[j + 1] = arr[j]  # Desplazar a la derecha
            j -= 1
        arr[j + 1] = key  # Insertar en su lugar correcto
        if i < 6:  # Mostrar primeras 5 iteraciones
            print(f"Iteración {i}: {arr[:10]}...")  # Muestra parcial

# Función para probar el algoritmo y medir tiempo
def probar_insertion_sort(nombre, arreglo):
    print(f"\n--- {nombre.upper()} ---")
    copia = arreglo.copy()
    inicio = time.time()
    insertion_sort(copia)
    fin = time.time()
    print(f"{nombre} - Tiempo: {fin - inicio:.6f} segundos")

# Generación de arreglos
n = 1000
aleatorio = random.sample(range(n), n)
ordenado = list(range(n))
inverso = list(range(n, 0, -1))

# Ejecución
print("Insertion Sort:")
probar_insertion_sort("Aleatorio", aleatorio)
probar_insertion_sort("Ordenado", ordenado)
probar_insertion_sort("Inverso", inverso)

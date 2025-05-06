import random
import time

# Algoritmo Quick Sort con pivote aleatorio
def quick_sort(arr, low, high, nivel=0):
    if low < high:
        pi = partition(arr, low, high)

        if nivel < 3:
            print(f"Partición nivel {nivel}: {arr[low:high+1][:10]}...")

        quick_sort(arr, low, pi - 1, nivel + 1)
        quick_sort(arr, pi + 1, high, nivel + 1)

# Partición con pivote aleatorio
def partition(arr, low, high):
    # Elegir índice aleatorio como pivote
    pivot_index = random.randint(low, high)
    arr[pivot_index], arr[high] = arr[high], arr[pivot_index]  # Mover pivote al final

    pivot = arr[high]
    i = low - 1

    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

# Medir tiempo y mostrar
def probar_quick_sort(nombre, arreglo):
    print(f"\n--- {nombre.upper()} ---")
    copia = arreglo.copy()
    inicio = time.time()
    quick_sort(copia, 0, len(copia) - 1)
    fin = time.time()
    print(f"{nombre} - Tiempo: {fin - inicio:.6f} segundos")

# Arreglos
n = 1000
aleatorio = random.sample(range(n), n)
ordenado = list(range(n))
inverso = list(range(n - 1, -1, -1))

# Ejecutar
print("Quick Sort:")
probar_quick_sort("Aleatorio", aleatorio)
probar_quick_sort("Ordenado", ordenado)
probar_quick_sort("Inverso", inverso)

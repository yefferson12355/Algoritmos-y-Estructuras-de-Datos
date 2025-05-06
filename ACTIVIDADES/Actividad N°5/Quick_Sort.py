import random
import time

# Algoritmo Merge Sort recursivo
def merge_sort(arr, nivel=0):
    if len(arr) > 1:
        mid = len(arr) // 2  # Punto medio
        L = arr[:mid]  # Subarreglo izquierdo
        R = arr[mid:]  # Subarreglo derecho

        merge_sort(L, nivel + 1)  # Ordenar mitad izquierda
        merge_sort(R, nivel + 1)  # Ordenar mitad derecha

        i = j = k = 0  # Índices para L, R y arr

        # Mezclar los elementos ordenados
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        # Copiar elementos restantes de L (si hay)
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        # Copiar elementos restantes de R (si hay)
        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1

        # Mostrar las fusiones de los primeros 3 ejemplos
        if nivel < 3:  # Mostrar hasta 3 niveles de fusión
            print(f"Fusión nivel {nivel}: {arr[:10]}...")

# Medir tiempo y mostrar
def probar_merge_sort(nombre, arreglo):
    print(f"\n--- {nombre.upper()} ---")
    copia = arreglo.copy()
    inicio = time.time()
    merge_sort(copia)
    fin = time.time()
    print(f"{nombre} - Tiempo: {fin - inicio:.6f} segundos")

# Arreglos
n = 1000
aleatorio = random.sample(range(n), n)
ordenado = list(range(n))
inverso = list(range(n, 0, -1))

# Ejecutar
print("Merge Sort:")
probar_merge_sort("Aleatorio", aleatorio)
probar_merge_sort("Ordenado", ordenado)
probar_merge_sort("Inverso", inverso)

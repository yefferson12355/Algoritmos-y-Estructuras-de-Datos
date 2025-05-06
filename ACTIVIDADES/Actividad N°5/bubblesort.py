import random  # Para generar arreglos aleatorios
import time    # Para medir el tiempo de ejecución

# Función de ordenamiento Bubble Sort
def bubble_sort(arr):
    n = len(arr)  # Longitud del arreglo
    for i in range(n):  # Recorrido de n veces
        for j in range(n - i - 1):  # Comparar elementos adyacentes
            if arr[j] > arr[j + 1]:  # Si están desordenados
                arr[j], arr[j + 1] = arr[j + 1], arr[j]  # Intercambiarlos
        if i < 5:  # Solo mostrar las primeras 5 iteraciones
            print(f"Iteración {i + 1}: {arr[:10]}...")  # Mostrar primeros 10 elementos

# Función para medir tiempo y mostrar resultados
def probar_bubble_sort(nombre, arreglo):
    print(f"\n--- {nombre.upper()} ---")  # Título
    copia = arreglo.copy()  # Copiar arreglo para no modificar el original
    inicio = time.time()  # Tiempo antes de ordenar
    bubble_sort(copia)  # Ejecutar el algoritmo
    fin = time.time()  # Tiempo después de ordenar
    print(f"{nombre} - Tiempo: {fin - inicio:.6f} segundos")  # Mostrar tiempo

# Crear tres tipos de arreglos
n = 1000
aleatorio = random.sample(range(n), n)  # Aleatorio sin repetición
ordenado = list(range(n))  # Arreglo ya ordenado
inverso = list(range(n, 0, -1))  # Arreglo en orden descendente

# Ejecutar pruebas
print("Bubble Sort:")
probar_bubble_sort("Aleatorio", aleatorio)
probar_bubble_sort("Ordenado", ordenado)
probar_bubble_sort("Inverso", inverso)

# Ordena una lista usando Bubble Sort
def bubble_sort(arr):
    n = len(arr)  # Obtener el tamaño de la lista
    for i in range(n - 1):  # Recorre la lista n-1 veces
        for j in range(n - i - 1):  # Hasta el último no ordenado
            if arr[j] > arr[j + 1]:  # Si el actual es mayor que el siguiente
                arr[j], arr[j + 1] = arr[j + 1], arr[j]  # Intercambio

# Ordena una lista usando Insertion Sort
def insertion_sort(arr):
    for i in range(1, len(arr)):  # Desde el segundo elemento
        key = arr[i]  # Elemento actual a insertar
        j = i - 1
        while j >= 0 and arr[j] > key:  # Mover elementos mayores a la derecha
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key  # Insertar el elemento

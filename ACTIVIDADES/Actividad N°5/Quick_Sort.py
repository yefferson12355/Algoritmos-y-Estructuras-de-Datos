# Ordena una lista usando Quick Sort (versión funcional)
def quick_sort(arr):
    if len(arr) <= 1:  # Caso base
        return arr
    pivot = arr[-1]  # Último elemento como pivote
    left = [x for x in arr[:-1] if x < pivot]  # Menores
    right = [x for x in arr[:-1] if x >= pivot]  # Mayores o iguales
    return quick_sort(left) + [pivot] + quick_sort(right)  # Concatenar resultado

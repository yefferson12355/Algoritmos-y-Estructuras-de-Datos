# Ordena una lista usando Merge Sort
def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2  # Punto medio
        L = arr[:mid]  # Mitad izquierda
        R = arr[mid:]  # Mitad derecha

        merge_sort(L)  # Ordenar izquierda
        merge_sort(R)  # Ordenar derecha

        i = j = k = 0
        # Mezclar los dos subarreglos
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        while i < len(L):  # Elementos restantes en L
            arr[k] = L[i]
            i += 1
            k += 1
        while j < len(R):  # Elementos restantes en R
            arr[k] = R[j]
            j += 1
            k += 1

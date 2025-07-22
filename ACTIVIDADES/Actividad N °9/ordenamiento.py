import tkinter as tk
import random
import time
import matplotlib.pyplot as plt

# ================== ALGORITMOS ================== #
def bubble_sort(arr):
    a = arr.copy()
    for i in range(len(a)):
        for j in range(len(a) - i - 1):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
    return a

def insertion_sort(arr):
    a = arr.copy()
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and key < a[j]:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a

def selection_sort(arr):
    a = arr.copy()
    for i in range(len(a)):
        min_idx = i
        for j in range(i+1, len(a)):
            if a[j] < a[min_idx]:
                min_idx = j
        a[i], a[min_idx] = a[min_idx], a[i]
    return a

def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr)//2
        L = merge_sort(arr[:mid])
        R = merge_sort(arr[mid:])
        return merge(L, R)
    else:
        return arr

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[0]
    menores = quick_sort([x for x in arr[1:] if x <= pivot])
    mayores = quick_sort([x for x in arr[1:] if x > pivot])
    return menores + [pivot] + mayores

# ================== FUNCIONES ================== #
def generar_lista(tam):
    return [random.randint(1, 1000) for _ in range(tam)]

def medir_tiempo(func, arr):
    inicio = time.time()
    func(arr)
    fin = time.time()
    return round(fin - inicio, 5)

def ejecutar_algoritmos():
    tam = int(entry_tamano.get())
    lista = generar_lista(tam)
    
    tiempos = {
        "Bubble Sort": medir_tiempo(bubble_sort, lista),
        "Insertion Sort": medir_tiempo(insertion_sort, lista),
        "Selection Sort": medir_tiempo(selection_sort, lista),
        "Merge Sort": medir_tiempo(merge_sort, lista),
        "Quick Sort": medir_tiempo(quick_sort, lista)
    }

    plt.figure(figsize=(8, 4))
    plt.bar(tiempos.keys(), tiempos.values())
    plt.ylabel("Tiempo (segundos)")
    plt.title("Comparación de Algoritmos de Ordenamiento")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# ================== INTERFAZ ================== #
ventana = tk.Tk()
ventana.title("Visualizador de Algoritmos de Ordenamiento")
ventana.geometry("400x200")

label_tamano = tk.Label(ventana, text="Tamaño de la lista:")
label_tamano.pack(pady=5)

entry_tamano = tk.Entry(ventana)
entry_tamano.insert(0, "100")
entry_tamano.pack(pady=5)

boton_ejecutar = tk.Button(ventana, text="Ejecutar y Comparar", command=ejecutar_algoritmos)
boton_ejecutar.pack(pady=10)

ventana.mainloop()

#include <iostream>     // Para imprimir en consola
#include <vector>       // Para usar std::vector
#include <algorithm>    // Para std::swap

#include <ctime>       // Para medir tiempo de ejecución

/* 
Descripción:
Bubble Sort: Algoritmo de ordenamiento simple que compara e intercambia elementos adyacentes,
burbujeando el mayor al final en cada pasada. Es ineficiente para listas grandes.
*/

// Función que ordena un vector usando Bubble Sort
void bubbleSort(std::vector<int>& arr) {
    clock_t inicio = clock();  // Marca el inicio del tiempo



    int n = arr.size();  // Obtener el tamaño del vector
    for (int i = 0; i < n - 1; ++i) {  // Repetir n-1 veces
        for (int j = 0; j < n - i - 1; ++j) {  // Recorrer hasta el último no ordenado
            if (arr[j] > arr[j + 1]) {  // Si están fuera de orden
                std::swap(arr[j], arr[j + 1]);  // Intercambiar
            }
        }

        // Mostrar el estado del vector después de cada pasada
        std::cout << "Pasada " << i + 1 << ": ";
        for (int val : arr)
            std::cout << val << " ";
        std::cout << std::endl;

        clock_t fin = clock();  // Marca el final del tiempo
        double tiempo = double(fin - inicio) / CLOCKS_PER_SEC;  // Calcular tiempo
        std::cout << "Tiempo de ejecucion: " << tiempo << " segundos" << std::endl;
    }
}

// Función principal
int main() {
    // Crear un vector con elementos desordenados
    std::vector<int> numeros = {64, 34, 25, 12, 22, 11, 90};

    std::cout << "Vector original: ";
    for (int n : numeros)
        std::cout << n << " ";
    std::cout << std::endl;

    // Aplicar Bubble Sort
    bubbleSort(numeros);

    // Mostrar el vector ordenado
    std::cout << "Vector ordenado: ";
    for (int n : numeros)
        std::cout << n << " ";
    std::cout << std::endl;

    return 0;
}
// Fin del código
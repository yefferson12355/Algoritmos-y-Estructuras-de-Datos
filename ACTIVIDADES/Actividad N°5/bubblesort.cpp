#include <iostream>     // Para imprimir en consola
#include <vector>       // Para usar std::vector
#include <algorithm>    // Para std::swap
#include <ctime>        // Para medir tiempo de ejecución
#include <cstdlib>      // Para usar rand()

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
        for (std::vector<int>::size_type j = 0; j < n - i - 1; ++j) {  // Usar el tipo correcto
            if (arr[j] > arr[j + 1]) {  // Si están fuera de orden
                std::swap(arr[j], arr[j + 1]);  // Intercambiar
            }
        }

        // Mostrar el estado del vector después de cada pasada, solo los primeros 10 elementos
        if (i < 5) {  // Solo mostrar las primeras 5 pasadas
            std::cout << "Pasada " << i + 1 << ": ";
            for (std::vector<int>::size_type j = 0; j < 10 && j < arr.size(); ++j) {
                std::cout << arr[j] << " ";  // Mostrar primeros 10 elementos
            }
            std::cout << "..." << std::endl;
        }
    }

    clock_t fin = clock();  // Marca el final del tiempo
    double tiempo = double(fin - inicio) / CLOCKS_PER_SEC;  // Calcular tiempo
    std::cout << "Tiempo total de ejecucion: " << tiempo << " segundos" << std::endl;
}

// Función para generar un arreglo aleatorio de tamaño n
std::vector<int> generarArregloAleatorio(int n) {
    std::vector<int> arr(n);
    for (int i = 0; i < n; ++i) {
        arr[i] = rand() % 1000;  // Llenar con números aleatorios entre 0 y 999
    }
    return arr;
}

// Función principal
int main() {
    srand(time(0));  // Inicializar la semilla aleatoria

    int n = 1000;  // Tamaño del arreglo

    // Crear tres vectores de ejemplo
    std::vector<int> aleatorio = generarArregloAleatorio(n);
    std::vector<int> ordenado(n);
    for (int i = 0; i < n; ++i) {
        ordenado[i] = i + 1;  // Arreglo ya ordenado
    }
    std::vector<int> inverso(n);
    for (int i = 0; i < n; ++i) {
        inverso[i] = n - i;  // Arreglo en orden descendente
    }

    // Ejecutar Bubble Sort para cada tipo de vector
    std::cout << "--- ALEATORIO ---" << std::endl;
    bubbleSort(aleatorio);

    std::cout << "\n--- ORDENADO ---" << std::endl;
    bubbleSort(ordenado);

    std::cout << "\n--- INVERSO ---" << std::endl;
    bubbleSort(inverso);

    return 0;
}

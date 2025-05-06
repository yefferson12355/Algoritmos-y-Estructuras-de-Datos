#include <iostream>
#include <vector>
#include <algorithm>
#include <chrono>
#include <random>

// Algoritmo Insertion Sort
void insertion_sort(std::vector<int>& arr) {
    for (size_t i = 1; i < arr.size(); ++i) {
        int key = arr[i];
        int j = i - 1;
        while (j >= 0 && arr[j] > key) {
            arr[j + 1] = arr[j];
            --j;
        }
        arr[j + 1] = key;

        if (i < 6) { // Mostrar primeras 5 iteraciones
            std::cout << "Iteracion " << i << ": ";
            for (size_t k = 0; k < std::min(arr.size(), size_t(10)); ++k) {
                std::cout << arr[k] << " ";
            }
            std::cout << "...\n";
        }
    }
}

// Función para probar el algoritmo y medir tiempo
void probar_insertion_sort(const std::string& nombre, const std::vector<int>& arreglo) {
    std::cout << "\n--- " << nombre << " ---\n";
    std::vector<int> copia = arreglo;
    auto inicio = std::chrono::high_resolution_clock::now();
    insertion_sort(copia);
    auto fin = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> duracion = fin - inicio;
    std::cout << nombre << " - Tiempo: " << duracion.count() << " segundos\n";
}

int main() {
    const int n = 1000;
    
    // Crear vector aleatorio
    std::vector<int> aleatorio(n);
    for (int i = 0; i < n; ++i) {
        aleatorio[i] = i;
    }
    std::random_device rd;
    std::mt19937 g(rd());
    std::shuffle(aleatorio.begin(), aleatorio.end(), g);

    // Crear vector ordenado
    std::vector<int> ordenado(n);
    for (int i = 0; i < n; ++i) {
        ordenado[i] = i;
    }

    // Crear vector inverso
    std::vector<int> inverso(n);
    for (int i = 0; i < n; ++i) {
        inverso[i] = n - i;
    }

    std::cout << "Insertion Sort:\n";
    probar_insertion_sort("Aleatorio", aleatorio);
    probar_insertion_sort("Ordenado", ordenado);
    probar_insertion_sort("Inverso", inverso);

    return 0;
}

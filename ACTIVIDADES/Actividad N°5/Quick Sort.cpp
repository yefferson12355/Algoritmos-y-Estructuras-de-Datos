#include <iostream>
#include <vector>
#include <algorithm>
#include <chrono>
#include <random>
#include <string>

// Merge Sort recursivo con impresión de los primeros niveles
void merge_sort(std::vector<int>& arr, int nivel = 0) {
    if (arr.size() > 1) {
        int mid = arr.size() / 2;
        std::vector<int> L(arr.begin(), arr.begin() + mid);
        std::vector<int> R(arr.begin() + mid, arr.end());

        merge_sort(L, nivel + 1);
        merge_sort(R, nivel + 1);

        int i = 0, j = 0, k = 0;

        // Mezclar subarreglos ordenados
        while (i < L.size() && j < R.size()) {
            if (L[i] < R[j]) {
                arr[k++] = L[i++];
            } else {
                arr[k++] = R[j++];
            }
        }

        // Copiar lo que queda de L (si hay)
        while (i < L.size()) {
            arr[k++] = L[i++];
        }

        // Copiar lo que queda de R (si hay)
        while (j < R.size()) {
            arr[k++] = R[j++];
        }

        // Mostrar las fusiones de los primeros 3 niveles
        if (nivel < 3) {
            std::cout << "Fusion nivel " << nivel << ": ";
            for (size_t m = 0; m < std::min(arr.size(), size_t(10)); ++m) {
                std::cout << arr[m] << " ";
            }
            std::cout << "...\n";
        }
    }
}

// Función para probar el algoritmo y medir tiempo
void probar_merge_sort(const std::string& nombre, const std::vector<int>& arreglo) {
    std::cout << "\n--- " << nombre << " ---\n";
    std::vector<int> copia = arreglo; // Copia del arreglo original
    auto inicio = std::chrono::high_resolution_clock::now();
    merge_sort(copia);
    auto fin = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> duracion = fin - inicio;
    std::cout << nombre << " - Tiempo: " << duracion.count() << " segundos\n";
}

int main() {
    const int n = 1000;

    // Generar arreglo aleatorio
    std::vector<int> aleatorio(n);
    for (int i = 0; i < n; ++i) aleatorio[i] = i;
    std::random_device rd;
    std::mt19937 g(rd());
    std::shuffle(aleatorio.begin(), aleatorio.end(), g);

    // Arreglo ordenado
    std::vector<int> ordenado(n);
    for (int i = 0; i < n; ++i) ordenado[i] = i;

    // Arreglo inverso
    std::vector<int> inverso(n);
    for (int i = 0; i < n; ++i) inverso[i] = n - i;

    std::cout << "Merge Sort:\n";
    probar_merge_sort("Aleatorio", aleatorio);
    probar_merge_sort("Ordenado", ordenado);
    probar_merge_sort("Inverso", inverso);

    return 0;
}

#include <iostream>
#include <vector>
#include <algorithm>
#include <cstdlib>
#include <ctime>
#include <chrono>
#include <random>

using namespace std;
using namespace std::chrono;

// Mostrar los primeros 10 elementos del segmento [low, high]
void mostrarParcial(const vector<int>& arr, int low, int high) {
    int limite = min(10, high - low + 1);
    cout << "[ ";
    for (int i = 0; i < limite; ++i) {
        cout << arr[low + i] << " ";
    }
    cout << (high - low + 1 > 10 ? "... " : "") << "]";
}

// Partición aleatoria
int partition(vector<int>& arr, int low, int high) {
    int pivotIndex = low + rand() % (high - low + 1);
    swap(arr[pivotIndex], arr[high]);
    int pivot = arr[high];
    int i = low - 1;

    for (int j = low; j < high; ++j) {
        if (arr[j] <= pivot) {
            ++i;
            swap(arr[i], arr[j]);
        }
    }
    swap(arr[i + 1], arr[high]);
    return i + 1;
}

// QuickSort con control de profundidad
void quickSort(vector<int>& arr, int low, int high, int nivel = 0) {
    if (low < high) {
        int pi = partition(arr, low, high);

        if (nivel < 3) {
            cout << "Particion nivel " << nivel << ": ";
            mostrarParcial(arr, low, high);
            cout << endl;
        }

        quickSort(arr, low, pi - 1, nivel + 1);
        quickSort(arr, pi + 1, high, nivel + 1);
    }
}

// Medir y mostrar tiempo de ejecución
void probarQuickSort(const string& nombre, const vector<int>& arreglo) {
    cout << "\n--- " << nombre << " ---" << endl;
    vector<int> copia = arreglo;

    auto inicio = high_resolution_clock::now();
    quickSort(copia, 0, copia.size() - 1);
    auto fin = high_resolution_clock::now();

    auto duracion = duration_cast<microseconds>(fin - inicio);
    cout << nombre << " - Tiempo: " << duracion.count() / 1e6 << " segundos" << endl;
}

int main() {
    srand(time(0));
    int n = 1000;

    // Generar vectores
    vector<int> aleatorio(n);
    for (int i = 0; i < n; ++i) aleatorio[i] = i;

    // Barajar aleatorio
    random_device rd;
    mt19937 g(rd());
    shuffle(aleatorio.begin(), aleatorio.end(), g);

    vector<int> ordenado(n);
    for (int i = 0; i < n; ++i) ordenado[i] = i;

    vector<int> inverso(n);
    for (int i = 0; i < n; ++i) inverso[i] = n - i - 1;

    cout << "Quick Sort:\n";
    probarQuickSort("Aleatorio", aleatorio);
    probarQuickSort("Ordenado", ordenado);
    probarQuickSort("Inverso", inverso);

    return 0;
}

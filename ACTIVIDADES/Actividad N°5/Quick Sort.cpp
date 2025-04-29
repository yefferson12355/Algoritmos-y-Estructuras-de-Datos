/*Quick Sort: Algoritmo eficiente basado en divide y vencerás.
 Elige un pivote, reordena elementos menores y mayores, y aplica recursión.

*/
#include <vector>  // Para std::vector
#include <algorithm> // Para std::swap

// Reorganiza el vector y devuelve la posición del pivote
int partition(std::vector<int>& arr, int low, int high) {
    int pivot = arr[high];  // Elegir último elemento como pivote
    int i = low - 1;  // Índice de menor elemento

    for (int j = low; j < high; ++j) {
        if (arr[j] < pivot) {
            std::swap(arr[++i], arr[j]);  // Intercambiar si es menor al pivote
        }
    }
    std::swap(arr[i + 1], arr[high]);  // Colocar pivote en su lugar
    return i + 1;
}

// Ordena el vector usando Quick Sort
void quickSort(std::vector<int>& arr, int low, int high) {
    if (low < high) {
        int pi = partition(arr, low, high);  // Partición
        quickSort(arr, low, pi - 1);  // Ordenar izquierda
        quickSort(arr, pi + 1, high);  // Ordenar derecha
    }
}

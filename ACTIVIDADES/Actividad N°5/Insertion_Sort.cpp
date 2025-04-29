/*Descripción:
Insertion Sort: Ordena los elementos construyendo la lista ordenada uno por uno,
 insertando cada elemento en su lugar adecuado.*/


#include <vector>  // Para usar std::vector

// Ordena un vector usando Insertion Sort
void insertionSort(std::vector<int>& arr) {
    for (int i = 1; i < arr.size(); ++i) {  // Desde el segundo elemento
        int key = arr[i];  // Elemento actual a insertar
        int j = i - 1;
        // Mueve elementos mayores que key una posición adelante
        while (j >= 0 && arr[j] > key) {
            arr[j + 1] = arr[j];  // Desplazar
            --j;
        }
        arr[j + 1] = key;  // Insertar en posición correcta
    }
}

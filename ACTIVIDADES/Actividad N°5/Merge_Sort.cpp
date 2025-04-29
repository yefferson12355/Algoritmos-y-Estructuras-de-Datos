/*Merge Sort: Algoritmo de ordenamiento eficiente de tipo divide y vencerás.
 Divide la lista en mitades, las ordena recursivamente y luego las combina.*/

 #include <vector>  // Para std::vector

// Combina dos mitades ordenadas del vector
void merge(std::vector<int>& arr, int left, int mid, int right) {
    std::vector<int> L(arr.begin() + left, arr.begin() + mid + 1);  // Subvector izquierdo
    std::vector<int> R(arr.begin() + mid + 1, arr.begin() + right + 1);  // Subvector derecho

    int i = 0, j = 0, k = left;
    while (i < L.size() && j < R.size()) {  // Mientras ambos tengan elementos
        if (L[i] <= R[j])
            arr[k++] = L[i++];  // Insertar el menor
        else
            arr[k++] = R[j++];
    }

    while (i < L.size()) arr[k++] = L[i++];  // Agregar los restantes de L
    while (j < R.size()) arr[k++] = R[j++];  // Agregar los restantes de R
}

// Ordena el vector recursivamente usando Merge Sort
void mergeSort(std::vector<int>& arr, int left, int right) {
    if (left < right) {
        int mid = (left + right) / 2;  // Punto medio
        mergeSort(arr, left, mid);  // Ordenar mitad izquierda
        mergeSort(arr, mid + 1, right);  // Ordenar mitad derecha
        merge(arr, left, mid, right);  // Combinar ambas mitades
    }
}

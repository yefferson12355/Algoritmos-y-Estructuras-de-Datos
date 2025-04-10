// Incluye la biblioteca para operaciones de entrada/salida
#include <iostream>
// Incluye la biblioteca para usar el contenedor vector
#include <vector>
// Incluye la biblioteca para funciones de tiempo
#include <ctime>
// Incluye la biblioteca para funciones generales (rand, srand)
#include <cstdlib>  

// Usa el espacio de nombres estándar para evitar std::
using namespace std;

// Función que genera una matriz de números aleatorios
vector<vector<int>> generarMatriz(int filas, int columnas) {
    // Crea una matriz bidimensional con las dimensiones especificadas
    vector<vector<int>> matriz(filas, vector<int>(columnas));
    
    // Recorre cada fila de la matriz
    for (int i = 0; i < filas; ++i)
        // Recorre cada columna de la fila actual
        for (int j = 0; j < columnas; ++j)
            // Asigna un número aleatorio entre 0 y 100 a cada posición
            matriz[i][j] = rand() % 101;
    
    // Devuelve la matriz generada
    return matriz;
}

// Función que cuenta los números pares en una matriz
int contarPares(const vector<vector<int>>& matriz) {
    // Inicializa el contador de números pares en 0
    int conteo = 0;
    
    // Recorre cada fila de la matriz (usando referencia constante)
    for (const auto& fila : matriz)
        // Recorre cada valor en la fila actual
        for (int val : fila)
            // Si el valor es par (divisible por 2 sin residuo)
            if (val % 2 == 0)
                // Incrementa el contador de pares
                ++conteo;
    
    // Devuelve el total de números pares encontrados
    return conteo;
}

// Función principal del programa
int main() {
    // Establece la semilla para números aleatorios usando el tiempo actual
    srand(time(0));
    
    // Define las dimensiones de la matriz (100x100)
    int filas = 100, columnas = 100;
    
    // Genera la matriz llamando a la función generarMatriz
    vector<vector<int>> matriz = generarMatriz(filas, columnas);
    
    // Registra el tiempo de inicio antes de contar los pares
    clock_t inicio = clock();
    
    // Cuenta los números pares en la matriz
    int resultado = contarPares(matriz);
    
    // Registra el tiempo de finalización después de contar
    clock_t fin = clock();
    
    // Imprime la cantidad de números pares encontrados
    cout << "Números pares: " << resultado << endl;
    
    // Calcula e imprime el tiempo de ejecución en segundos
    // Convierte la diferencia de ticks a segundos dividiendo por CLOCKS_PER_SEC
    cout << "Tiempo de ejecución: " << double(fin - inicio) / CLOCKS_PER_SEC << " segundos\n";
    
    // Retorna 0 indicando que el programa terminó correctamente
    return 0;
}
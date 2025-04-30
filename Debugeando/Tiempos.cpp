#include <iostream>
#include <cstdlib>   // Para rand(), srand()
#include <ctime>     // Para time(), clock()
using namespace std;

int main() {
    srand(time(0)); // Semilla aleatoria basada en el tiempo

    clock_t inicio = clock(); // Marca el inicio del bloque

    //  Bloque a medir: for con números aleatorios
    for (int i = 0; i < 100; ++i) {
        int a = rand() % 101; // Genera número aleatorio entre 0 y 100
        cout << a << " "; // Imprime el valor de 'a' para usarlo
    }

    clock_t fin = clock(); // Marca el final del bloque

    double tiempo = double(fin - inicio) / CLOCKS_PER_SEC;
    cout << "Tiempo de ejecución: " << tiempo << " segundos" << endl;

    return 0;
}


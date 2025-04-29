#include<iostream>
using namespace std;

/*2.Elaborar un algoritmo que recorra un arreglo de N elementos y determine el 
Segundo valor más alto sin ordenarlo*/

void encontrarSegundoMayor(int arr[], int N) {
    if (N < 2) {
        cout << "No hay suficientes elementos para encontrar el segundo mayor." << endl;
        return;
    }

    int max1 = arr[0], max2 = arr[0];

    for (int i = 1; i < N; i++) {
        if (arr[i] > max1) {
            max2 = max1;
            max1 = arr[i];
        } else if (arr[i] > max2 && arr[i] != max1) {
            max2 = arr[i];
        }
    }

    if (max1 == max2) {
        cout << "No hay un segundo mayor único en el arreglo." << std::endl;
    } else {
        cout << "El segundo valor más alto es: " << max2 << std::endl;
    }
}


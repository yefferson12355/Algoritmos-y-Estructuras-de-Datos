/*Cada nodo tiene un valor y una prioridad.

Se insertan ordenados por prioridad (no simplemente al final).*/

#include <iostream>
using namespace std;

// Nodo con prioridad
struct Nodo {
    int dato;
    int prioridad;
    Nodo* siguiente;
};

// Insertar ordenado por prioridad
void insertar(Nodo*& cabeza, int valor, int prioridad) {
    Nodo* nuevo = new Nodo{valor, prioridad, nullptr};

    if (!cabeza || prioridad < cabeza->prioridad) { 
        // Insertar al inicio si es más urgente
        nuevo->siguiente = cabeza;
        cabeza = nuevo;
    } else {
        Nodo* actual = cabeza;
        while (actual->siguiente && actual->siguiente->prioridad <= prioridad) {
            actual = actual->siguiente;
        }
        nuevo->siguiente = actual->siguiente;
        actual->siguiente = nuevo;
    }
}

// Mostrar lista
void mostrar(Nodo* cabeza) {
    while (cabeza) {
        cout << "[" << cabeza->dato << ", prioridad: " << cabeza->prioridad << "] -> ";
        cabeza = cabeza->siguiente;
    }
    cout << "NULL" << endl;
}

int main() {
    Nodo* lista = nullptr;

    insertar(lista, 10, 2);
    insertar(lista, 5, 1);
    insertar(lista, 20, 3);

    mostrar(lista);

    return 0;
}

/*Es como una lista normal, pero algunos nodos saltan más lejos.

Sirve para buscar más rápido.

Simulación básica (sin probabilidades reales todavía).
*/



#include <iostream>
using namespace std;

// Nodo con salto
struct Nodo {
    int dato;
    Nodo* siguiente;
    Nodo* salto; // salto extra (puede ser NULL)
};

// Insertar simple
void insertar(Nodo*& cabeza, int valor) {
    Nodo* nuevo = new Nodo{valor, nullptr, nullptr};

    if (!cabeza) {
        cabeza = nuevo;
    } else {
        Nodo* actual = cabeza;
        while (actual->siguiente) {
            actual = actual->siguiente;
        }
        actual->siguiente = nuevo;
    }
}

// Asignar saltos manualmente (ejemplo sencillo)
void asignarSaltos(Nodo* cabeza) {
    if (!cabeza || !cabeza->siguiente || !cabeza->siguiente->siguiente) return;
    
    cabeza->salto = cabeza->siguiente->siguiente; // primer salto
}

// Mostrar saltos
void mostrar(Nodo* cabeza) {
    Nodo* actual = cabeza;
    while (actual) {
        cout << actual->dato;
        if (actual->salto) {
            cout << " (salta a " << actual->salto->dato << ")";
        }
        cout << " -> ";
        actual = actual->siguiente;
    }
    cout << "NULL" << endl;
}

int main() {
    Nodo* lista = nullptr;

    insertar(lista, 1);
    insertar(lista, 2);
    insertar(lista, 3);
    insertar(lista, 4);

    asignarSaltos(lista);
    mostrar(lista);

    return 0;
}

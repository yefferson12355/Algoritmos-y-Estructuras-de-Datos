
/*Cada nodo tiene una lista dentro (o un puntero a otra lista).

Se usa en sistemas de carpetas (por ejemplo: carpetas dentro de carpetas).*/


#include <iostream>
using namespace std;

// Nodo multinivel
struct Nodo {
    int dato;
    Nodo* siguiente;
    Nodo* abajo; // apuntador a una sub-lista
};

// Insertar al final
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

// Mostrar lista multinivel
void mostrar(Nodo* cabeza) {
    while (cabeza) {
        cout << cabeza->dato;
        if (cabeza->abajo) {
            cout << " [sublista: ";
            mostrar(cabeza->abajo);
            cout << "]";
        }
        cout << " -> ";
        cabeza = cabeza->siguiente;
    }
    cout << "NULL ";
}

int main() {
    Nodo* lista = nullptr;

    insertar(lista, 1);
    insertar(lista, 2);

    // Sublista en 2
    lista->siguiente->abajo = nullptr;
    insertar(lista->siguiente->abajo, 21);
    insertar(lista->siguiente->abajo, 22);

    mostrar(lista);

    return 0;
}

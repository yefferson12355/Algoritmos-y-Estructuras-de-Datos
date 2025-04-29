#include <iostream>
using namespace std;

// Estructura de nodo
struct Nodo {
    int dato;
    Nodo* siguiente;
};

// Insertar al final
void insertar(Nodo*& cabeza, int valor) {
    Nodo* nuevo = new Nodo{valor, nullptr};

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

// Mostrar la lista
void mostrar(Nodo* cabeza) {
    Nodo* actual = cabeza;
    while (actual) {
        cout << actual->dato << " -> ";
        actual = actual->siguiente;
    }
    cout << "NULL" << endl;
}

// Buscar un valor
Nodo* buscar(Nodo* cabeza, int valor) {
    Nodo* actual = cabeza;
    while (actual) {
        if (actual->dato == valor) {
            return actual;
        }
        actual = actual->siguiente;
    }
    return nullptr; // No encontrado
}

// Eliminar un valor
void eliminar(Nodo*& cabeza, int valor) {
    if (!cabeza) return;

    if (cabeza->dato == valor) { // Si es el primero
        Nodo* temp = cabeza;
        cabeza = cabeza->siguiente;
        delete temp;
        return;
    }

    Nodo* actual = cabeza;
    while (actual->siguiente && actual->siguiente->dato != valor) {
        actual = actual->siguiente;
    }

    if (actual->siguiente) {
        Nodo* temp = actual->siguiente;
        actual->siguiente = temp->siguiente;
        delete temp;
    }
}

int main() {
    Nodo* lista = nullptr;

    insertar(lista, 1);
    insertar(lista, 2);
    insertar(lista, 3);

    mostrar(lista);

    Nodo* encontrado = buscar(lista, 2);
    if (encontrado) {
        cout << "Encontrado: " << encontrado->dato << endl;
    } else {
        cout << "No encontrado" << endl;
    }

    eliminar(lista, 3);
    mostrar(lista);

    return 0;
}

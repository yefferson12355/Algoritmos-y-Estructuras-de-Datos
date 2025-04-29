#include <iostream>
using namespace std;

// Estructura de nodo doble
struct Nodo {
    int dato;
    Nodo* siguiente;
    Nodo* anterior;
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
        nuevo->anterior = actual;
    }
}

// Mostrar hacia adelante
void mostrar(Nodo* cabeza) {
    Nodo* actual = cabeza;
    while (actual) {
        cout << actual->dato << " <-> ";
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
    return nullptr;
}

// Eliminar un valor
void eliminar(Nodo*& cabeza, int valor) {
    Nodo* actual = cabeza;
    
    while (actual && actual->dato != valor) {
        actual = actual->siguiente;
    }

    if (!actual) return; // No encontrado

    if (actual == cabeza) { // Es el primero
        cabeza = actual->siguiente;
        if (cabeza) cabeza->anterior = nullptr;
    } else {
        if (actual->anterior) actual->anterior->siguiente = actual->siguiente;
        if (actual->siguiente) actual->siguiente->anterior = actual->anterior;
    }

    delete actual;
}

int main() {
    Nodo* lista = nullptr;

    insertar(lista, 10);
    insertar(lista, 20);
    insertar(lista, 30);

    mostrar(lista);

    Nodo* encontrado = buscar(lista, 20);
    if (encontrado) {
        cout << "Encontrado: " << encontrado->dato << endl;
    }

    eliminar(lista, 20);
    mostrar(lista);

    return 0;
}

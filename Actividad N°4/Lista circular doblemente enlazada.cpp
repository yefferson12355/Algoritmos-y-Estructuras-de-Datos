#include <iostream>
using namespace std;

// Nodo circular doble
struct Nodo {
    int dato;
    Nodo* siguiente;
    Nodo* anterior;
};

// Insertar
void insertar(Nodo*& cabeza, int valor) {
    Nodo* nuevo = new Nodo{valor, nullptr, nullptr};

    if (!cabeza) {
        cabeza = nuevo;
        cabeza->siguiente = cabeza;
        cabeza->anterior = cabeza;
    } else {
        Nodo* ultimo = cabeza->anterior;

        ultimo->siguiente = nuevo;
        nuevo->anterior = ultimo;
        nuevo->siguiente = cabeza;
        cabeza->anterior = nuevo;
    }
}

// Mostrar
void mostrar(Nodo* cabeza) {
    if (!cabeza) return;
    Nodo* actual = cabeza;
    do {
        cout << actual->dato << " <-> ";
        actual = actual->siguiente;
    } while (actual != cabeza);
    cout << "(cierra circulo)" << endl;
}

int main() {
    Nodo* lista = nullptr;

    insertar(lista, 100);
    insertar(lista, 200);
    insertar(lista, 300);

    mostrar(lista);

    return 0;
}

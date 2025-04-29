#include <iostream>
using namespace std;

// Nodo circular simple
struct Nodo {
    int dato;
    Nodo* siguiente;
};

// Insertar
void insertar(Nodo*& cabeza, int valor) {
    Nodo* nuevo = new Nodo{valor, nullptr};

    if (!cabeza) {
        cabeza = nuevo;
        cabeza->siguiente = cabeza; // Apunta a sí mismo
    } else {
        Nodo* actual = cabeza;
        while (actual->siguiente != cabeza) {
            actual = actual->siguiente;
        }
        actual->siguiente = nuevo;
        nuevo->siguiente = cabeza;
    }
}

// Mostrar
void mostrar(Nodo* cabeza) {
    if (!cabeza) return;
    Nodo* actual = cabeza;
    do {
        cout << actual->dato << " -> ";
        actual = actual->siguiente;
    } while (actual != cabeza);
    cout << "(regresa inicio)" << endl;
}

int main() {
    Nodo* lista = nullptr;

    insertar(lista, 5);
    insertar(lista, 6);
    insertar(lista, 7);

    mostrar(lista);

    return 0;
}

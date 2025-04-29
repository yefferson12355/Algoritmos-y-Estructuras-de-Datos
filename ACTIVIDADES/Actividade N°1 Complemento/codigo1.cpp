#include <iostream>
using namespace std;

struct Nodo {
    int dato;
    Nodo* siguiente;
};

class Lista {
private:
    Nodo* cabeza;

public:
    Lista() {
        cabeza = nullptr;
    }

    void insertarInicio(int valor) {
        Nodo* nuevo = new Nodo();
        nuevo->dato = valor;
        nuevo->siguiente = cabeza;
        cabeza = nuevo;
    }

    void insertarFinal(int valor) {
        Nodo* nuevo = new Nodo();
        nuevo->dato = valor;
        nuevo->siguiente = nullptr;
        if (cabeza == nullptr) {
            cabeza = nuevo;
        } else {
            Nodo* actual = cabeza;
            while (actual->siguiente != nullptr)
                actual = actual->siguiente;
            actual->siguiente = nuevo;
        }
    }

    void eliminarInicio() {
        if (cabeza != nullptr) {
            Nodo* temp = cabeza;
            cabeza = cabeza->siguiente;
            delete temp;
        }
    }
    
    void insertarEnPosicion(int valor, int posicion) {
    Nodo* nuevo = new Nodo();
    nuevo->dato = valor;
    nuevo->siguiente = nullptr;

    if (posicion <= 0 || cabeza == nullptr) {
        nuevo->siguiente = cabeza;
        cabeza = nuevo;
    } else {
        Nodo* actual = cabeza;
        int contador = 0;

        while (actual->siguiente != nullptr && contador < posicion - 1) {
            actual = actual->siguiente;
            contador++;
        }

        nuevo->siguiente = actual->siguiente;
        actual->siguiente = nuevo;
    }
}

    void mostrar() {
        Nodo* actual = cabeza;
        while (actual != nullptr) {
            cout << actual->dato << " -> ";
            actual = actual->siguiente;
        }
        cout << "NULL" << endl;
    }
};

int main() {
    Lista lista;
    lista.insertarInicio(10);
    lista.insertarInicio(20);
    lista.insertarFinal(30);
    lista.mostrar(); 
    lista.eliminarInicio();
    lista.insertarEnPosicion(25, 2);  
    lista.mostrar(); 
    return 0;
}
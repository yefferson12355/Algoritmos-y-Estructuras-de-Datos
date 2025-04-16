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
            Nodo* nuevo = new Nodo{valor, cabeza};
            cabeza = nuevo;
        }

        void insertarFinal(int valor) {
            Nodo* nuevo = new Nodo{valor, nullptr};
            if (!cabeza) {
                cabeza = nuevo;
            } else {
                Nodo* actual = cabeza;
                while (actual->siguiente != nullptr)
                    actual = actual->siguiente;
                actual->siguiente = nuevo;
            }
        }   

    //  Insertar en una posición específica
    void insertarEnPosicion(int valor, int posicion) {
        if (posicion < 0) {
            cout << "Posicion invalida.\n";
            return;
        }

        Nodo* nuevo = new Nodo{valor, nullptr};

        if (posicion == 0) {
            nuevo->siguiente = cabeza;
            cabeza = nuevo;
            return;
        }

        Nodo* actual = cabeza;
        int contador = 0;

        for (contador = 0; contador <posicion -1 ; contador++)
        {   
            if (actual!=nullptr)
            {
                    actual=actual->siguiente;
                
                
            }
        }
        /*
        while (actual != nullptr && contador < posicion - 1) {
            actual = actual->siguiente;
            contador++;
        }
        */

        if (actual == nullptr) {
            cout << "La posicion excede el tamano de la lista.\n";
            delete nuevo;
            return;
        }

        nuevo->siguiente = actual->siguiente;
        actual->siguiente = nuevo;
    }

    void mostrar() {
        Nodo* actual = cabeza;
        while (actual != nullptr) {
            cout << actual->dato << " -> ";
            actual = actual->siguiente;
        }
        cout << "NULL" << endl;
    }

    ~Lista() {
        while (cabeza != nullptr) {
            Nodo* temp = cabeza;
            cabeza = cabeza->siguiente;
            delete temp;
        }
    }
};

int main() {
    Lista lista;
    lista.insertarFinal(10);
    lista.insertarFinal(20);
    lista.insertarFinal(30);
    lista.mostrar();  

    lista.insertarEnPosicion(15, 1); 
    lista.mostrar();  

    lista.insertarEnPosicion(5, 0); 
    lista.mostrar();      
    lista.insertarEnPosicion(50, 10); // Posición inválida
    return 0;
}

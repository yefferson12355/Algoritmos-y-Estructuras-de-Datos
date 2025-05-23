#include <iostream>
using namespace std;

// Definición del nodo
struct Nodo {
    int dato;
    Nodo* siguiente;
    
    Nodo(int valor) : dato(valor), siguiente(nullptr) {}
};

class ListaEnlazada {
private:
    Nodo* cabeza;
    
public:
    ListaEnlazada() : cabeza(nullptr) {}
    
    // Destructor para liberar memoria
    ~ListaEnlazada() {
        while (cabeza != nullptr) {
            Nodo* temp = cabeza;
            cabeza = cabeza->siguiente;
            delete temp;
        }
    }
    
    // Insertar al inicio
    void insertarAlInicio(int valor) {
        Nodo* nuevoNodo = new Nodo(valor);
        nuevoNodo->siguiente = cabeza;
        cabeza = nuevoNodo;
        cout << "Insertado al inicio: " << valor << endl;
    }
    
    // Insertar al final
    void insertarAlFinal(int valor) {
        Nodo* nuevoNodo = new Nodo(valor);
        
        if (cabeza == nullptr) {
            cabeza = nuevoNodo;
        } else {
            Nodo* actual = cabeza;
            while (actual->siguiente != nullptr) {
                actual = actual->siguiente;
            }
            actual->siguiente = nuevoNodo;
        }
        cout << "Insertado al final: " << valor << endl;
    }
    
    // Eliminar del inicio
    int eliminarDelInicio() {
        if (cabeza == nullptr) {
            cout << "Error: Lista vacia" << endl;
            return -1;
        }
        
        Nodo* temp = cabeza;
        int valor = temp->dato;
        cabeza = cabeza->siguiente;
        delete temp;
        cout << "Eliminado del inicio: " << valor << endl;
        return valor;
    }
    
    // Mostrar lista
    void mostrar() {
        if (cabeza == nullptr) {
            cout << "Lista vacia" << endl;
            return;
        }
        
        cout << "Recorrido completo: ";
        Nodo* actual = cabeza;
        while (actual != nullptr) {
            cout << actual->dato;
            if (actual->siguiente != nullptr) {
                cout << " -> ";
            }
            actual = actual->siguiente;
        }
        cout << " -> NULL" << endl;
    }
    
    bool estaVacia() {
        return cabeza == nullptr;
    }
};

// Función principal
int main() {
    ListaEnlazada lista;
    
    cout << "=== IMPLEMENTACION DE LISTA ENLAZADA EN C++ ===" << endl;
    
    // Insertar al inicio los valores: 8, 4
    cout << "\n1. Insertando al inicio:" << endl;
    lista.insertarAlInicio(8);
    lista.insertarAlInicio(4);
    
    cout << "\nEstado despues de insertar al inicio:" << endl;
    lista.mostrar();
    
    // Insertar al final el valor: 11
    cout << "\n2. Insertando al final:" << endl;
    lista.insertarAlFinal(11);
    
    cout << "\nEstado despues de insertar al final:" << endl;
    lista.mostrar();
    
    // Eliminar el primer nodo
    cout << "\n3. Eliminando el primer nodo:" << endl;
    lista.eliminarDelInicio();
    
    // Mostrar el recorrido completo
    cout << "\n4. Recorrido final:" << endl;
    lista.mostrar();
    
    return 0;
}

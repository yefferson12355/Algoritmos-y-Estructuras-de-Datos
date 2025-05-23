#include <iostream>
#include <vector>
using namespace std;

class Pila {
private:
    vector<int> elementos;
    
public:
    // Insertar elemento (push)
    void push(int valor) {
        elementos.push_back(valor);
        cout << "Insertado: " << valor << endl;
    }
    
    // Eliminar elemento (pop)
    int pop() {
        if (elementos.empty()) {
            cout << "Error: Pila vacía" << endl;
            return -1;
        }
        int valor = elementos.back();
        elementos.pop_back();
        cout << "Eliminado: " << valor << endl;
        return valor;
    }
    
    // Mostrar el tope
    int tope() {
        if (elementos.empty()) {
            cout << "Pila vacía" << endl;
            return -1;
        }
        return elementos.back();
    }
    
    // Recorrer pila
    void mostrar() {
        cout << "Estado de la pila (tope -> base): ";
        for (int i = elementos.size() - 1; i >= 0; i--) {
            cout << elementos[i] << " ";
        }
        cout << endl;
    }
    
    bool estaVacia() {
        return elementos.empty();
    }
};

// Función principal para ejecutar las operaciones
int main() {
    Pila pila;
    
    cout << "=== IMPLEMENTACION DE PILA EN C++ ===" << endl;
    
    // Insertar elementos: 5, 10, 15, 20, 25
    cout << "\n1. Insertando elementos:" << endl;
    pila.push(5);
    pila.push(10);
    pila.push(15);
    pila.push(20);
    pila.push(25);
    
    cout << "\nEstado despues de insertar:" << endl;
    pila.mostrar();
    cout << "Tope actual: " << pila.tope() << endl;
    
    // Eliminar dos elementos consecutivos
    cout << "\n2. Eliminando dos elementos:" << endl;
    pila.pop();
    pila.pop();
    
    // Mostrar estado final
    cout << "\n3. Estado final:" << endl;
    pila.mostrar();
    cout << "Tope final: " << pila.tope() << endl;
    
    return 0;
}
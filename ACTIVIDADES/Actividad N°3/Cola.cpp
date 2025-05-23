#include <iostream>
#include <queue>
using namespace std;

class Cola {
private:
    queue<int> elementos;
    
public:
    // Insertar elemento (enqueue)
    void enqueue(int valor) {
        elementos.push(valor);
        cout << "Insertado: " << valor << endl;
    }
    
    // Eliminar elemento (dequeue)
    int dequeue() {
        if (elementos.empty()) {
            cout << "Error: Cola vacía" << endl;
            return -1;
        }
        int valor = elementos.front();
        elementos.pop();
        cout << "Eliminado: " << valor << endl;
        return valor;
    }
    
    // Mostrar el frente
    int frente() {
        if (elementos.empty()) {
            cout << "Cola vacía" << endl;
            return -1;
        }
        return elementos.front();
    }
    
    // Recorrer cola (implementación auxiliar)
    void mostrar() {
        if (elementos.empty()) {
            cout << "Cola vacía" << endl;
            return;
        }
        
        queue<int> temp = elementos;
        cout << "Estado de la cola (frente -> final): ";
        while (!temp.empty()) {
            cout << temp.front() << " ";
            temp.pop();
        }
        cout << endl;
    }
    
    bool estaVacia() {
        return elementos.empty();
    }
    
    int tamaño() {
        return elementos.size();
    }
};

// Función principal
int main() {
    Cola cola;
    
    cout << "=== IMPLEMENTACION DE COLA EN C++ ===" << endl;
    
    // Insertar elementos: 3, 6, 9, 12
    cout << "\n1. Insertando elementos:" << endl;
    cola.enqueue(3);
    cola.enqueue(6);
    cola.enqueue(9);
    cola.enqueue(12);
    
    cout << "\nEstado despues de insertar:" << endl;
    cola.mostrar();
    cout << "Frente actual: " << cola.frente() << endl;
    
    // Eliminar un elemento
    cout << "\n2. Eliminando un elemento:" << endl;
    cola.dequeue();
    
    // Mostrar cola final
    cout << "\n3. Estado final:" << endl;
    cola.mostrar();
    cout << "Frente final: " << cola.frente() << endl;
    
    return 0;
}

//Grafos: Lista de Adyacencia - Versión Simple
#include <iostream>
#include <vector>

using namespace std;

//Definicion de Lista
vector<vector<int>> lista_Adyacencia;

//Inicializacion de listas
void crear_lista(int n){
    lista_Adyacencia.resize(n);
    cout << "Lista creada para " << n << " nodos" << endl;
} 

//Agregar arista
void agregar_arista(int origen, int destino){
    lista_Adyacencia[origen].push_back(destino);
    cout << "Arista agregada: " << origen << " -> " << destino << endl;
}

//Mostrar lista
void mostrar_lista(){
    cout << "\nLista de Adyacencia:" << endl;
    for(int i = 0; i < lista_Adyacencia.size(); i++){
        cout << "Nodo " << i << ": ";
        for(int j = 0; j < lista_Adyacencia[i].size(); j++){
            cout << lista_Adyacencia[i][j] << " ";
        }
        cout << endl;
    }
}

int main(){
    int n, origen, destino, opcion;
    
    cout << "=== LISTA DE ADYACENCIA ===" << endl;
    
    while(true){
        cout << "\n1. Crear lista" << endl;
        cout << "2. Agregar arista" << endl;
        cout << "3. Mostrar lista" << endl;
        cout << "4. Salir" << endl;
        cout << "Opcion: ";
        cin >> opcion;
        
        switch(opcion){
            case 1:
                cout << "Numero de nodos: ";
                cin >> n;
                crear_lista(n);
                break;
                
            case 2:
                cout << "Nodo origen: ";
                cin >> origen;
                cout << "Nodo destino: ";
                cin >> destino;
                agregar_arista(origen, destino);
                break;
                
            case 3:
                mostrar_lista();
                break;
                
            case 4:
                return 0;
                
            default:
                cout << "Opcion invalida" << endl;
        }
    }
    
    return 0;
}
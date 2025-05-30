#include <iostream>
#include <string>
#include <vector>
using namespace std;

// Estructura para representar el grafo no dirigido usando listas de adyacencia
class Grafo {
private:
    vector<string> nodos; // Lista de nombres de nodos
    vector<vector<int>> adyacencia; // Matriz de adyacencia
public:
    // Agrega un nodo al grafo si no existe
    void agregarNodo(const string& nombre) {
        for (const string& nodo : nodos) {
            if (nodo == nombre) return; // Ya existe
        }
        nodos.push_back(nombre);
        for (auto& fila : adyacencia) {
            fila.push_back(0); // Agrega una columna por cada nuevo nodo
        }
        adyacencia.push_back(vector<int>(nodos.size(), 0)); // Agrega una nueva fila
    }

    // Conecta dos nodos (grafo no dirigido)
    void agregarConexion(const string& origen, const string& destino) {
        int i = indice(origen);
        int j = indice(destino);
        if (i != -1 && j != -1) {
            adyacencia[i][j] = 1;
            adyacencia[j][i] = 1; // Conexión en ambos sentidos
        }
    }

    // Obtiene el índice de un nodo
    int indice(const string& nombre) {
        for (int i = 0; i < nodos.size(); i++) {
            if (nodos[i] == nombre) return i;
        }
        return -1;
    }

    // Verifica si hay una ruta usando DFS (Depth-First Search)
    bool hayRutaDFS(const string& inicio, const string& destino) {
        int i = indice(inicio);
        int j = indice(destino);
        if (i == -1 || j == -1) return false;
        vector<bool> visitado(nodos.size(), false);
        return dfs(i, j, visitado);
    }

    // Función recursiva DFS
    bool dfs(int actual, int destino, vector<bool>& visitado) {
        if (actual == destino) return true;
        visitado[actual] = true;
        for (int i = 0; i < nodos.size(); i++) {
            if (adyacencia[actual][i] == 1 && !visitado[i]) {
                if (dfs(i, destino, visitado)) return true;
            }
        }
        return false;
    }

    // Mostrar todas las rutas posibles entre dos nodos
    void mostrarTodasLasRutas(const string& inicio, const string& destino) {
        int i = indice(inicio);
        int j = indice(destino);
        if (i == -1 || j == -1) {
            cout << "Uno de los nodos no existe.\n";
            return;
        }
        vector<bool> visitado(nodos.size(), false);
        vector<string> camino;
        cout << "Rutas de " << inicio << " a " << destino << ":\n";
        dfsTodas(i, j, visitado, camino);
    }

    // DFS para encontrar todas las rutas posibles
    void dfsTodas(int actual, int destino, vector<bool>& visitado, vector<string>& camino) {
        visitado[actual] = true;
        camino.push_back(nodos[actual]);
        if (actual == destino) {
            for (int i = 0; i < camino.size(); i++) {
                cout << camino[i];
                if (i < camino.size() - 1) cout << " -> ";
            }
            cout << endl;
        } else {
            for (int i = 0; i < nodos.size(); i++) {
                if (adyacencia[actual][i] == 1 && !visitado[i]) {
                    dfsTodas(i, destino, visitado, camino);
                }
            }
        }
        // Retroceso
        camino.pop_back();
        visitado[actual] = false;
    }
};

// Función principal para interactuar con el sistema
int main() {
    Grafo g;
    int n;
    cout << "Cantidad de conexiones: ";
    cin >> n;
    cin.ignore();

    for (int i = 0; i < n; i++) {
        string a, b;
        cout << "Conexion " << i+1 << " (formato A B): ";
        cin >> a >> b;
        g.agregarNodo(a);
        g.agregarNodo(b);
        g.agregarConexion(a, b);
    }

    string origen, destino;
    cout << "Ingrese punto de partida: ";
    cin >> origen;
    cout << "Ingrese destino: ";
    cin >> destino;

    if (g.hayRutaDFS(origen, destino)) {
        cout << "Existe al menos una ruta.\n";
        g.mostrarTodasLasRutas(origen, destino);
    } else {
        cout << "No existe una ruta entre los puntos indicados.\n";
    }

    return 0;
}

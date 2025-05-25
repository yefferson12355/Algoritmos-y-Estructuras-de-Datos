#include <iostream>
#include <vector>   // Para usar vectores dinámicos
#include <queue>    // Para la cola de prioridad (priority_queue)
#include <limits>   // Para obtener valores límite (infinito)
#include <cstdlib>  // Para números aleatorios (rand, srand)
#include <ctime>
#include <chrono>
#include <unordered_set>    // Para conjuntos hash (evitar duplicados)

using namespace std;

// Función para generar un grafo dirigido con pesos aleatorios y una cantidad fija de conexiones por nodo
vector<vector<pair<int, int>>> generarGrafo(int n, int conexionesPorNodo = 3) {
    vector<vector<pair<int, int>>> grafo(n);
    srand(time(0)); // Semilla aleatoria para obtener diferentes grafos cada vez

    for (int u = 0; u < n; ++u) {
        unordered_set<int> conectados; // Para evitar múltiples conexiones al mismo nodo
        while (conectados.size() < conexionesPorNodo) {
            int v = rand() % n;
            int peso = 1 + rand() % 20; // Peso entre 1 y 20
            if (u != v && conectados.find(v) == conectados.end()) {
                grafo[u].emplace_back(v, peso); // Agrega conexión u -> v
                conectados.insert(v);
            }
        }
    }
    return grafo;
}

// Algoritmo de Dijkstra utilizando un min-heap (priority_queue con greater<>)
vector<int> dijkstra(int n, const vector<vector<pair<int, int>>>& grafo, int inicio) {
    vector<int> dist(n, numeric_limits<int>::max()); // Inicializa distancias a infinito
    priority_queue<pair<int, int>, vector<pair<int, int>>, greater<>> pq; // Min-heap

    dist[inicio] = 0;
    pq.push({0, inicio}); // (distancia, nodo)

    while (!pq.empty()) {
        auto [d, u] = pq.top(); pq.pop();

        if (d > dist[u]) continue; // Si ya hay una mejor distancia, ignorar

        for (const auto& [v, peso] : grafo[u]) {
            if (dist[u] + peso < dist[v]) {
                dist[v] = dist[u] + peso;
                pq.push({dist[v], v}); // Agrega el nuevo candidato al heap
            }
        }
    }

    return dist;
}

int main() {
    // Tamaños del grafo para modelar: 10, 100 y 1000 nodos
    vector<int> tamanos = {10, 100, 1000};

    for (int n : tamanos) {
        auto grafo = generarGrafo(n); // Genera el grafo

        auto inicio = chrono::high_resolution_clock::now(); // Inicia cronómetro

        auto distancias = dijkstra(n, grafo, 0); // Ejecuta Dijkstra desde nodo 0

        auto fin = chrono::high_resolution_clock::now(); // Detiene cronómetro

        auto duracion = chrono::duration_cast<chrono::milliseconds>(fin - inicio).count();

        cout << "Grafo de " << n << " nodos: Tiempo = " << duracion << " ms" << endl;

        // Mostrar un resumen de las distancias para verificar funcionamiento
        cout << "Distancias desde nodo 0 a los primeros 5 nodos: ";
        for (int i = 0; i < min(5, n); ++i) {
            cout << distancias[i] << " ";
        }
        cout << "...\n\n";
    }

    return 0;
}

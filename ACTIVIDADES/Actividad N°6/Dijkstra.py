import heapq
import random
import time
from memory_profiler import memory_usage

# Genera un grafo dirigido con pesos aleatorios y conexiones limitadas por nodo
def generar_grafo(n, conexiones_por_nodo=3):
    grafo = {i: [] for i in range(n)}
    for u in range(n):
        conectados = set()
        while len(conectados) < conexiones_por_nodo:
            v = random.randint(0, n - 1)
            if v != u and v not in conectados:
                peso = random.randint(1, 20)
                grafo[u].append((v, peso))
                conectados.add(v)
    return grafo

# Algoritmo de Dijkstra usando min-heap
def dijkstra(graph, start):
    dist = {node: float('inf') for node in graph}
    dist[start] = 0
    priority_queue = [(0, start)]  # (distancia, nodo)

    while priority_queue:
        d, u = heapq.heappop(priority_queue)
        if d > dist[u]:
            continue
        for v, weight in graph.get(u, []):
            if dist[u] + weight < dist[v]:
                dist[v] = dist[u] + weight
                heapq.heappush(priority_queue, (dist[v], v))
    return dist

# Evalúa tiempo y memoria para distintos tamaños
def evaluar_dijkstra():
    tamanos = [10, 100, 1000]
    tiempos = []
    memorias = []

    for n in tamanos:
        grafo = generar_grafo(n)

        # Medición de tiempo
        inicio = time.time()
        distancias = dijkstra(grafo, 0)
        fin = time.time()
        duracion = (fin - inicio) * 1000  # ms
        tiempos.append(duracion)

        # Medición de memoria
        uso_memoria = memory_usage((dijkstra, (grafo, 0)), max_iterations=1)
        memoria_max = max(uso_memoria) - min(uso_memoria)
        memorias.append(memoria_max)

        print(f"Grafo de {n} nodos: Tiempo = {duracion:.2f} ms, Memoria ≈ {memoria_max:.2f} MiB")
        print(f"Distancias desde nodo 0 a los primeros 5 nodos: {[distancias[i] for i in range(min(5, n))]}\n")

    return tamanos, tiempos, memorias

# Ejecutar evaluación
if __name__ == "__main__":
    evaluar_dijkstra()

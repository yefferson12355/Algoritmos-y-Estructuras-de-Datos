    import networkx as nx
import matplotlib.pyplot as plt

class GrafoVisual:
    def _init_(self):
        self.grafo = nx.Graph()
        self.adyacencia = {}

    def agregar_conexion(self, a, b):
        self.grafo.add_edge(a, b)
        self.adyacencia.setdefault(a, []).append(b)
        self.adyacencia.setdefault(b, []).append(a)

    def mostrar_grafo(self):
        pos = nx.spring_layout(self.grafo)
        nx.draw(self.grafo, pos, with_labels=True, node_color='skyblue', node_size=2000, font_weight='bold')
        plt.title("Grafo de la ciudad altiplánica")
        plt.show()

    def mostrar_todas_las_rutas(self, origen, destino):
        rutas = []
        self._dfs_rutas(origen, destino, set(), [], rutas)
        print(f"Rutas desde {origen} a {destino}:")
        for ruta in rutas:
            print(" -> ".join(ruta))
        return rutas

    def _dfs_rutas(self, actual, destino, visitados, camino, rutas):
        visitados.add(actual)
        camino.append(actual)

        if actual == destino:
            rutas.append(list(camino))
        else:
            for vecino in self.adyacencia.get(actual, []):
                if vecino not in visitados:
                    self._dfs_rutas(vecino, destino, visitados, camino, rutas)

        camino.pop()
        visitados.remove(actual)

    def dibujar_rutas(self, rutas):
        for ruta in rutas:
            plt.figure()
            pos = nx.spring_layout(self.grafo)
            nx.draw(self.grafo, pos, with_labels=True, node_color='lightgray', node_size=2000)
            edges_ruta = [(ruta[i], ruta[i+1]) for i in range(len(ruta)-1)]
            nx.draw_networkx_edges(self.grafo, pos, edgelist=edges_ruta, width=4, edge_color='red')
            nx.draw_networkx_nodes(self.grafo, pos, nodelist=ruta, node_color='orange')
            plt.title("Ruta resaltada: " + " -> ".join(ruta))
            plt.show()



grafo = GrafoVisual()
n = int(input("Ingrese número de conexiones: "))

print("Ingrese las conexiones (puntoA puntoB):")
for _ in range(n):
    a, b = input().split()
    grafo.agregar_conexion(a, b)

grafo.mostrar_grafo()

origen = input("Ingrese el punto de origen: ")
destino = input("Ingrese el punto de destino: ")

rutas = grafo.mostrar_todas_las_rutas(origen, destino)

if rutas:
    grafo.dibujar_rutas(rutas)
else:
    print(f"No existe una ruta entre {origen} y {destino}.")


Ese es el 2 
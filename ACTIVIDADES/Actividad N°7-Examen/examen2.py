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


import tkinter as tk
from tkinter import messagebox

# ==================== CLASE GRAFO ====================
# Esta clase representa la estructura de datos del grafo
# Un grafo es una colección de nodos (puntos) conectados por aristas (conexiones)

class Grafo:
    def __init__(self):
        """
        Constructor de la clase Grafo
        Inicializa un diccionario vacío para almacenar las conexiones
        """
        # Diccionario donde cada clave es un nodo y su valor es una lista de nodos conectados
        # Ejemplo: {'A': ['B', 'C'], 'B': ['A'], 'C': ['A']}
        self.adyacencia = {}

    def agregar_conexion(self, a, b):
        """
        Agrega una conexión bidireccional entre dos puntos
        
        Args:
            a: Primer punto/nodo
            b: Segundo punto/nodo
        """
        # setdefault: Si 'a' no existe en el diccionario, crea una lista vacía
        # luego agrega 'b' a la lista de conexiones de 'a'
        self.adyacencia.setdefault(a, []).append(b) 
        
        # Hace lo mismo para 'b', creando una conexión bidireccional
        # Si A está conectado a B, entonces B también está conectado a A
        self.adyacencia.setdefault(b, []).append(a)

    def existe_ruta(self, origen, destino):
        """
        Verifica si existe AL MENOS UNA ruta entre origen y destino
        
        Args:
            origen: Punto de inicio
            destino: Punto de llegada
            
        Returns:
            bool: True si existe una ruta, False si no existe
        """
        # Set para llevar control de los nodos ya visitados
        # Evita ciclos infinitos en el recorrido
        visitados = set()# para no duplicados.
        
        # Llama al método privado que hace la búsqueda recursiva
        return self._dfs_existe(origen, destino, visitados)

    def _dfs_existe(self, actual, destino, visitados):
        """
        Búsqueda en profundidad (DFS - Depth First Search) para verificar existencia de ruta
        Este es un método privado (por eso empieza con _)
        
        Args:
            actual: Nodo actual en el que estamos
            destino: Nodo al que queremos llegar
            visitados: Set de nodos ya visitados
            
        Returns:
            bool: True si encontramos el destino, False si no
        """
        # CASO BASE: Si llegamos al destino, encontramos la ruta
        if actual == destino:
            return True
        
        # Marcamos el nodo actual como visitado
        visitados.add(actual)
        
        # Exploramos todos los vecinos del nodo actual
        for vecino in self.adyacencia.get(actual, []):
            # Solo visitamos vecinos que no hayamos visitado antes
            if vecino not in visitados:
                # RECURSIÓN: Buscamos desde el vecino hacia el destino
                if self._dfs_existe(vecino, destino, visitados):
                    return True
        
        # Si ningún vecino llevó al destino, no hay ruta
        return False

    def mostrar_todas_las_rutas(self, origen, destino):
        """
        Encuentra TODAS las rutas posibles entre origen y destino
        
        Args:
            origen: Punto de inicio
            destino: Punto de llegada
            
        Returns:
            list: Lista de listas, donde cada sublista es una ruta completa
        """
        rutas = []  # Lista para almacenar todas las rutas encontradas
        
        # Llama al método privado que hace la búsqueda recursiva
        self._dfs_rutas(origen, destino, set(), [], rutas)
        
        return rutas

    def _dfs_rutas(self, actual, destino, visitados, camino, rutas):
        """
        Búsqueda en profundidad para encontrar TODAS las rutas posibles
        
        Args:
            actual: Nodo actual
            destino: Nodo destino
            visitados: Set de nodos visitados en el camino actual
            camino: Lista con el camino actual que estamos construyendo
            rutas: Lista donde se almacenan todas las rutas encontradas
        """
        # Marcamos el nodo actual como visitado
        visitados.add(actual)
        # Agregamos el nodo actual al camino que estamos construyendo
        camino.append(actual)

        # CASO BASE: Si llegamos al destino
        if actual == destino:
            # Agregamos una COPIA del camino actual a la lista de rutas
            # Usamos list(camino) para crear una copia, no una referencia
            rutas.append(list(camino))
        else:
            # Si no llegamos al destino, exploramos todos los vecinos
            for vecino in self.adyacencia.get(actual, []):
                if vecino not in visitados:
                    # RECURSIÓN: Continuamos la búsqueda desde el vecino
                    self._dfs_rutas(vecino, destino, visitados, camino, rutas)

        # BACKTRACKING: Deshacemos los cambios para explorar otros caminos
        camino.pop()           # Removemos el nodo actual del camino
        visitados.remove(actual)  # Marcamos el nodo como no visitado

# ==================== INTERFAZ GRÁFICA ====================

class InterfazGrafo:
    def __init__(self, root):
        """
        Constructor de la interfaz gráfica
        
        Args:
            root: Ventana principal de tkinter
        """
        # Creamos una instancia del grafo que vamos a manejar
        self.grafo = Grafo()

        # Configuración de la ventana principal
        root.title("Análisis de rutas - Ciudad Altiplánica")
        root.geometry("500x500")

        # ========== SECCIÓN: AGREGAR CONEXIONES ==========
        
        # Etiqueta y campo de entrada para el punto A
        tk.Label(root, text="Punto A:").pack()
        self.entry_a = tk.Entry(root)
        self.entry_a.pack()

        # Etiqueta y campo de entrada para el punto B
        tk.Label(root, text="Punto B:").pack()
        self.entry_b = tk.Entry(root)
        self.entry_b.pack()

        # Botón para agregar la conexión entre A y B
        tk.Button(root, text="Agregar conexión", command=self.agregar_conexion).pack(pady=5)

        # ========== SECCIÓN: ANÁLISIS DE RUTAS ==========
        
        # Etiqueta y campo de entrada para el origen
        tk.Label(root, text="Origen:").pack()
        self.entry_origen = tk.Entry(root)
        self.entry_origen.pack()

        # Etiqueta y campo de entrada para el destino
        tk.Label(root, text="Destino:").pack()
        self.entry_destino = tk.Entry(root)
        self.entry_destino.pack()

        # Botón para verificar si existe una ruta
        tk.Button(root, text="¿Existe una ruta?", command=self.verificar_ruta).pack(pady=5)
        
        # Botón para mostrar todas las rutas posibles
        tk.Button(root, text="Mostrar todas las rutas", command=self.mostrar_rutas).pack(pady=5)

        # ========== ÁREA DE RESULTADOS ==========
        
        # Área de texto donde se muestran los resultados
        self.resultado = tk.Text(root, height=15, width=60)
        self.resultado.pack(pady=10)

    def agregar_conexion(self):
        """
        Método que se ejecuta cuando se presiona el botón "Agregar conexión"
        """
        # Obtiene los valores de los campos de entrada y elimina espacios en blanco
        a = self.entry_a.get().strip()
        b = self.entry_b.get().strip()
        
        # Verifica que ambos campos tengan contenido
        if a and b:
            # Agrega la conexión al grafo
            self.grafo.agregar_conexion(a, b)
            
            # Muestra un mensaje en el área de resultados
            self.resultado.insert(tk.END, f"Conexión agregada: {a} <-> {b}\n")
            
            # Limpia los campos de entrada para la siguiente conexión
            self.entry_a.delete(0, tk.END)
            self.entry_b.delete(0, tk.END)
        else:
            # Muestra un mensaje de error si falta información
            messagebox.showwarning("Error", "Ingrese ambos puntos.")

    def verificar_ruta(self):
        """
        Método que verifica si existe una ruta entre origen y destino
        """
        # Obtiene los valores de origen y destino
        origen = self.entry_origen.get().strip()
        destino = self.entry_destino.get().strip()
        
        # Verifica que ambos campos tengan contenido
        if not origen or not destino:
            messagebox.showwarning("Error", "Ingrese origen y destino.")
            return
        
        # Usa el método del grafo para verificar si existe ruta
        existe = self.grafo.existe_ruta(origen, destino)
        
        # Muestra el resultado en el área de texto
        if existe:
            self.resultado.insert(tk.END, f"Existe una ruta entre {origen} y {destino}\n")
        else:
            self.resultado.insert(tk.END, f"No hay ruta entre {origen} y {destino}\n")

    def mostrar_rutas(self):
        """
        Método que muestra todas las rutas posibles entre origen y destino
        """
        # Obtiene los valores de origen y destino
        origen = self.entry_origen.get().strip()
        destino = self.entry_destino.get().strip()
        
        # Verifica que ambos campos tengan contenido
        if not origen or not destino:
            messagebox.showwarning("Error", "Ingrese origen y destino.")
            return
        
        # Obtiene todas las rutas posibles del grafo
        rutas = self.grafo.mostrar_todas_las_rutas(origen, destino)
        
        # Muestra los resultados
        if rutas:
            self.resultado.insert(tk.END, f"Rutas entre {origen} y {destino}:\n")
            # Itera sobre cada ruta encontrada
            for ruta in rutas:
                # Une los elementos de la ruta con " -> " y los muestra
                self.resultado.insert(tk.END, " -> ".join(ruta) + "\n")
        else:
            self.resultado.insert(tk.END, f"No hay rutas posibles entre {origen} y {destino}\n")

# ==================== EJECUCIÓN DEL PROGRAMA ====================

if __name__ == "__main__":
    """
    Punto de entrada del programa
    Solo se ejecuta si este archivo se ejecuta directamente (no si se importa)
    """
    # Crea la ventana principal de tkinter
    root = tk.Tk()
    
    # Crea una instancia de la interfaz gráfica
    app = InterfazGrafo(root)
    
    # Inicia el bucle principal de la interfaz gráfica
    # Esto mantiene la ventana abierta y responde a eventos del usuario
    root.mainloop()
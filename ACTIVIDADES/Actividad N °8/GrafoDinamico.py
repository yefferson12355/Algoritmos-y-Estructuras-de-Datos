import tkinter as tk
from tkinter import scrolledtext, messagebox
import random
import heapq

# Clase para representar un nodo con su nombre y coordenadas para el dibujo
class Nodo:
    def __init__(self, nombre, x, y):
        self.nombre = nombre
        self.x = x
        self.y = y

# Clase para representar una arista con nodos de origen, destino y su peso
class Arista:
    def __init__(self, desde, hasta, peso):
        self.desde = desde
        self.hasta = hasta
        self.peso = peso

class GrafoDinamico(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Grafo de Transporte - Python/Tkinter")
        self.geometry("800x650")

        self.nodos = {}
        self.aristas = []
        self.ruta_corta_nodos = []

        # -- Paneles de la Interfaz --
        # Panel superior para la entrada del grafo
        top_frame = tk.Frame(self, padx=10, pady=10)
        top_frame.pack(side=tk.TOP, fill=tk.X)

        tk.Label(top_frame, text="Ingrese aristas (formato: Nodo1 Nodo2 Peso):").pack(anchor='w')
        self.entrada_text_area = scrolledtext.ScrolledText(top_frame, height=5, width=70)
        self.entrada_text_area.insert(tk.END, "A B 4\nA C 2\nB D 10\nC D 3\nC E 8\nD E 6")
        self.entrada_text_area.pack(side=tk.LEFT, expand=True, fill=tk.X)
        
        tk.Button(top_frame, text="Crear Grafo", command=self.cargar_grafo_desde_texto).pack(side=tk.RIGHT, padx=5)

        # Canvas para dibujar el grafo
        self.canvas = tk.Canvas(self, bg="white", height=400)
        self.canvas.pack(expand=True, fill=tk.BOTH, padx=10, pady=5)

        # Panel inferior para buscar la ruta
        bottom_frame = tk.Frame(self, padx=10, pady=10)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

        tk.Label(bottom_frame, text="Inicio:").pack(side=tk.LEFT)
        self.inicio_field = tk.Entry(bottom_frame, width=8)
        self.inicio_field.pack(side=tk.LEFT, padx=5)
        
        tk.Label(bottom_frame, text="Fin:").pack(side=tk.LEFT)
        self.fin_field = tk.Entry(bottom_frame, width=8)
        self.fin_field.pack(side=tk.LEFT, padx=5)

        tk.Button(bottom_frame, text="Buscar Ruta", command=self.buscar_ruta).pack(side=tk.LEFT, padx=10)
        
        self.resultado_area = tk.Text(bottom_frame, height=2, width=40, state='disabled')
        self.resultado_area.pack(side=tk.LEFT, expand=True, fill=tk.X)

        # Cargar el grafo inicial al arrancar
        self.cargar_grafo_desde_texto()

    def cargar_grafo_desde_texto(self):
        """Lee la entrada de texto, crea los nodos y aristas, y redibuja el grafo."""
        self.nodos.clear()
        self.aristas.clear()
        self.ruta_corta_nodos.clear()
        
        texto = self.entrada_text_area.get("1.0", tk.END)
        lineas = texto.strip().split("\n")
        
        canvas_width = self.canvas.winfo_width() or 780
        canvas_height = self.canvas.winfo_height() or 400

        for linea in lineas:
            partes = linea.strip().split()
            if len(partes) == 3:
                n1_nombre, n2_nombre, peso_str = partes
                try:
                    peso = int(peso_str)
                    
                    # Crea los nodos si no existen, asignando posiciones aleatorias
                    if n1_nombre not in self.nodos:
                        x, y = random.randint(50, canvas_width - 50), random.randint(50, canvas_height - 50)
                        self.nodos[n1_nombre] = Nodo(n1_nombre, x, y)
                    if n2_nombre not in self.nodos:
                        x, y = random.randint(50, canvas_width - 50), random.randint(50, canvas_height - 50)
                        self.nodos[n2_nombre] = Nodo(n2_nombre, x, y)
                        
                    nodo1 = self.nodos[n1_nombre]
                    nodo2 = self.nodos[n2_nombre]
                    
                    # El grafo es no dirigido, se añaden aristas en ambos sentidos
                    self.aristas.append(Arista(nodo1, nodo2, peso))
                    self.aristas.append(Arista(nodo2, nodo1, peso))
                    
                except ValueError:
                    print(f"Línea ignorada (formato incorrecto): {linea}")

        self.pintar_componente()

    def dijkstra(self, inicio_nombre):
        """Implementación del algoritmo de Dijkstra para encontrar la ruta más corta."""
        distancias = {nombre: float('inf') for nombre in self.nodos}
        padres = {nombre: None for nombre in self.nodos}
        distancias[inicio_nombre] = 0
        
        cola_prioridad = [(0, inicio_nombre)] # (distancia, nombre_nodo)
        
        while cola_prioridad:
            dist_actual, v_actual_nombre = heapq.heappop(cola_prioridad)

            if dist_actual > distancias[v_actual_nombre]:
                continue
            
            v_actual = self.nodos[v_actual_nombre]
            
            # Revisa las aristas que salen del nodo actual
            for arista in self.aristas:
                if arista.desde == v_actual:
                    vecino = arista.hasta
                    nueva_dist = dist_actual + arista.peso
                    if nueva_dist < distancias[vecino.nombre]:
                        distancias[vecino.nombre] = nueva_dist
                        padres[vecino.nombre] = v_actual_nombre
                        heapq.heappush(cola_prioridad, (nueva_dist, vecino.nombre))
                        
        return distancias, padres

    def buscar_ruta(self):
        """Manejador del botón 'Buscar Ruta'."""
        inicio_texto = self.inicio_field.get().upper()
        fin_texto = self.fin_field.get().upper()

        if not inicio_texto or not fin_texto:
            messagebox.showwarning("Entrada inválida", "Debe ingresar un nodo de inicio y fin.")
            return
            
        if inicio_texto not in self.nodos or fin_texto not in self.nodos:
            messagebox.showerror("Error", "Nodos inválidos. Asegúrese de que existen en el grafo.")
            return
            
        distancias, padres = self.dijkstra(inicio_texto)
        
        # Actualizar el área de resultado
        self.resultado_area.config(state='normal')
        self.resultado_area.delete("1.0", tk.END)

        if distancias[fin_texto] == float('inf'):
            self.resultado_area.insert(tk.END, "No hay camino entre los nodos.")
            self.ruta_corta_nodos = []
        else:
            # Reconstruir la ruta
            ruta = []
            paso_actual = fin_texto
            while paso_actual is not None:
                ruta.append(paso_actual)
                paso_actual = padres[paso_actual]
            ruta.reverse()
            
            self.ruta_corta_nodos = [self.nodos[nombre] for nombre in ruta]
            
            # Mostrar resultado
            texto_resultado = f"Ruta más corta: {' -> '.join(ruta)}\n"
            texto_resultado += f"Distancia total: {distancias[fin_texto]}"
            self.resultado_area.insert(tk.END, texto_resultado)

        self.resultado_area.config(state='disabled')
        self.pintar_componente()

    def pintar_componente(self):
        """Dibuja todos los elementos del grafo en el canvas."""
        self.canvas.delete("all")
        
        # Dibujar aristas
        for arista in self.aristas:
            self.canvas.create_line(
                arista.desde.x, arista.desde.y,
                arista.hasta.x, arista.hasta.y,
                fill="gray", width=1
            )
            # Dibujar peso de la arista
            xm, ym = (arista.desde.x + arista.hasta.x) / 2, (arista.desde.y + arista.hasta.y) / 2
            self.canvas.create_text(xm, ym, text=str(arista.peso), fill="black")

        # Dibujar la ruta más corta (si existe)
        if len(self.ruta_corta_nodos) > 1:
            for i in range(len(self.ruta_corta_nodos) - 1):
                n1 = self.ruta_corta_nodos[i]
                n2 = self.ruta_corta_nodos[i+1]
                self.canvas.create_line(n1.x, n1.y, n2.x, n2.y, fill="red", width=3)

        # Dibujar nodos
        for nodo in self.nodos.values():
            x, y = nodo.x, nodo.y
            self.canvas.create_oval(x - 15, y - 15, x + 15, y + 15, fill="#66CCFF", outline="black")
            self.canvas.create_text(x, y, text=nodo.nombre, fill="black", font=("Arial", 10, "bold"))

if __name__ == "__main__":
    app = GrafoDinamico()
    app.mainloop()
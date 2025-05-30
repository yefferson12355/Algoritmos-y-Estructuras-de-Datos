import tkinter as tk
from tkinter import messagebox

class Grafo:
    def __init__(self):
        self.adyacencia = {}

    def agregar_conexion(self, a, b):
        self.adyacencia.setdefault(a, []).append(b)
        self.adyacencia.setdefault(b, []).append(a)

    def existe_ruta(self, origen, destino):
        visitados = set()
        return self._dfs_existe(origen, destino, visitados)

    def _dfs_existe(self, actual, destino, visitados):
        if actual == destino:
            return True
        visitados.add(actual)
        for vecino in self.adyacencia.get(actual, []):
            if vecino not in visitados:
                if self._dfs_existe(vecino, destino, visitados):
                    return True
        return False

    def mostrar_todas_las_rutas(self, origen, destino):
        rutas = []
        self._dfs_rutas(origen, destino, set(), [], rutas)
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

# ------------------ INTERFAZ ------------------

class InterfazGrafo:
    def __init__(self, root):
        self.grafo = Grafo()

        root.title("Análisis de rutas - Ciudad Altiplánica")
        root.geometry("500x500")

        # Entrada de conexiones
        tk.Label(root, text="Punto A:").pack()
        self.entry_a = tk.Entry(root)
        self.entry_a.pack()

        tk.Label(root, text="Punto B:").pack()
        self.entry_b = tk.Entry(root)
        self.entry_b.pack()

        tk.Button(root, text="Agregar conexión", command=self.agregar_conexion).pack(pady=5)

        # Entrada origen y destino
        tk.Label(root, text="Origen:").pack()
        self.entry_origen = tk.Entry(root)
        self.entry_origen.pack()

        tk.Label(root, text="Destino:").pack()
        self.entry_destino = tk.Entry(root)
        self.entry_destino.pack()

        tk.Button(root, text="¿Existe una ruta?", command=self.verificar_ruta).pack(pady=5)
        tk.Button(root, text="Mostrar todas las rutas", command=self.mostrar_rutas).pack(pady=5)

        # Área de salida
        self.resultado = tk.Text(root, height=15, width=60)
        self.resultado.pack(pady=10)

    def agregar_conexion(self):
        a = self.entry_a.get().strip()
        b = self.entry_b.get().strip()
        if a and b:
            self.grafo.agregar_conexion(a, b)
            self.resultado.insert(tk.END, f"Conexión agregada: {a} <-> {b}\n")
            self.entry_a.delete(0, tk.END)
            self.entry_b.delete(0, tk.END)
        else:
            messagebox.showwarning("Error", "Ingrese ambos puntos.")

    def verificar_ruta(self):
        origen = self.entry_origen.get().strip()
        destino = self.entry_destino.get().strip()
        if not origen or not destino:
            messagebox.showwarning("Error", "Ingrese origen y destino.")
            return
        existe = self.grafo.existe_ruta(origen, destino)
        if existe:
            self.resultado.insert(tk.END, f"Existe una ruta entre {origen} y {destino}\n")
        else:
            self.resultado.insert(tk.END, f" No hay ruta entre {origen} y {destino}\n")

    def mostrar_rutas(self):
        origen = self.entry_origen.get().strip()
        destino = self.entry_destino.get().strip()
        if not origen or not destino:
            messagebox.showwarning("Error", "Ingrese origen y destino.")
            return
        rutas = self.grafo.mostrar_todas_las_rutas(origen, destino)
        if rutas:
            self.resultado.insert(tk.END, f"Rutas entre {origen} y {destino}:\n")
            for ruta in rutas:
                self.resultado.insert(tk.END, " -> ".join(ruta) + "\n")
        else:
            self.resultado.insert(tk.END, f"No hay rutas posibles entre {origen} y {destino}\n")

# ------------------ Ejecutar ------------------

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazGrafo(root)
    root.mainloop()

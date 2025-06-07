import tkinter as tk

# Clase que gestiona el historial de acciones
class HistorialComandos:
    def __init__(self, limite=10):
        self.deshacer = []  # Pila para deshacer
        self.rehacer = []   # Pila para rehacer
        self.limite = limite

    def ejecutar_accion(self, accion):
        if len(self.deshacer) >= self.limite:
            self.deshacer.pop(0)  # Eliminar la accion mas antigua si se supera el limite//es necesario el cero , borrar por indice
        self.deshacer.append(accion)  # Añadir nueva accion
        self.rehacer.clear()  # Al hacer una nueva accion, se limpia rehacer

    def deshacer_accion(self):
        if not self.deshacer:
            return "Nada que deshacer."
        accion = self.deshacer.pop()
        self.rehacer.append(accion)#Agregar al ultimo ,reaccer
        return f"Deshacer accion: {accion}"

    def rehacer_accion(self):
        if not self.rehacer:
            return "Nada que rehacer."
        accion = self.rehacer.pop()
        self.deshacer.append(accion)
        return f"Rehacer accion: {accion}"

    def obtener_historial(self):
        return self.deshacer, self.rehacer


# Clase de interfaz grafica
class Interfaz:
    def __init__(self, root):
        self.historial = HistorialComandos()
        self.root = root
        root.title("Historial de Comandos")

        # Etiquetas para mostrar el estado de las pilas
        self.label_deshacer = tk.Label(root, text="Deshacer: []")
        self.label_deshacer.pack()

        self.label_rehacer = tk.Label(root, text="Rehacer: []")
        self.label_rehacer.pack()

        # Mostrar la accion realizada o mensaje de estado
        self.label_estado = tk.Label(root, text="")
        self.label_estado.pack(pady=5)

        # Botones de accion
        tk.Button(root, text="Dibujar", command=lambda: self.realizar_accion("Dibujar")).pack(pady=5)
        tk.Button(root, text="Mover", command=lambda: self.realizar_accion("Mover")).pack(pady=5)
        tk.Button(root, text="Eliminar", command=lambda: self.realizar_accion("Eliminar")).pack(pady=5)
        tk.Button(root, text="Deshacer", command=self.deshacer).pack(pady=5)
        tk.Button(root, text="Rehacer", command=self.rehacer).pack(pady=5)

    # Ejecuta una accion y actualiza la interfaz
    def realizar_accion(self, accion):
        self.historial.ejecutar_accion(accion)
        self.label_estado.config(text=f"Accion realizada: {accion}")
        self.actualizar_historial()

    # Realiza deshacer
    def deshacer(self):
        mensaje = self.historial.deshacer_accion()
        self.label_estado.config(text=mensaje)
        self.actualizar_historial()

    # Realiza rehacer
    def rehacer(self):
        mensaje = self.historial.rehacer_accion()
        self.label_estado.config(text=mensaje)
        self.actualizar_historial()

    # Actualiza las etiquetas visuales
    def actualizar_historial(self):
        deshacer, rehacer = self.historial.obtener_historial()
        self.label_deshacer.config(text=f"Deshacer: {deshacer}")
        self.label_rehacer.config(text=f"Rehacer: {rehacer}")


# Crear la ventana e iniciar la interfaz (esto se debe ejecutar localmente con entorno gráfico)
if __name__ == "__main__":
    ventana = tk.Tk()
    app = Interfaz(ventana)
    ventana.mainloop()


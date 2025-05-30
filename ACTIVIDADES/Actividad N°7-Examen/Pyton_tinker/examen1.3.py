import tkinter as tk
from tkinter import messagebox, simpledialog

class Paciente:
    def __init__(self, nombre, dni, nivel, tiempo):
        self.nombre = nombre
        self.dni = dni
        self.nivelEmergencia = nivel
        self.tiempoAtencion = tiempo

class SistemaEmergencia:
    def __init__(self):
        self.heap = []
        self.totalAtendidos = 0
        self.tiempoTotal = 0

    def agregarPaciente(self, p):
        self.heap.append(p)
        self._subir(len(self.heap) - 1)

    def atenderPaciente(self):
        if not self.heap:
            return None
        paciente = self.heap[0]
        self.totalAtendidos += 1
        self.tiempoTotal += paciente.tiempoAtencion
        self.heap[0] = self.heap[-1]
        self.heap.pop()
        self._bajar(0)
        return paciente

    def pacientesPendientes(self):
        return self.heap

    def resumen(self):
        return self.totalAtendidos, self.tiempoTotal

    def _subir(self, i):
        while i > 0:
            padre = (i - 1) // 2
            if self.heap[i].nivelEmergencia < self.heap[padre].nivelEmergencia:
                self.heap[i], self.heap[padre] = self.heap[padre], self.heap[i]
                i = padre
            else:
                break

    def _bajar(self, i):
        n = len(self.heap)
        while True:
            izq = 2 * i + 1
            der = 2 * i + 2
            menor = i
            if izq < n and self.heap[izq].nivelEmergencia < self.heap[menor].nivelEmergencia:
                menor = izq
            if der < n and self.heap[der].nivelEmergencia < self.heap[menor].nivelEmergencia:
                menor = der
            if menor != i:
                self.heap[i], self.heap[menor] = self.heap[menor], self.heap[i]
                i = menor
            else:
                break

# Interfaz gráfica
sistema = SistemaEmergencia()

def agregar_paciente():
    nombre = simpledialog.askstring("Nombre", "Ingrese nombre del paciente:")
    if not nombre: return
    dni = simpledialog.askstring("DNI", "Ingrese DNI:")
    if not dni: return
    try:
        nivel = int(simpledialog.askstring("Nivel", "Nivel de emergencia (1-5):"))
        tiempo = int(simpledialog.askstring("Tiempo", "Tiempo estimado de atención (min):"))
    except:
        messagebox.showerror("Error", "Nivel o tiempo inválido.")
        return

    paciente = Paciente(nombre, dni, nivel, tiempo)
    sistema.agregarPaciente(paciente)
    messagebox.showinfo("Éxito", "Paciente agregado correctamente.")

def atender_paciente():
    paciente = sistema.atenderPaciente()
    if paciente:
        messagebox.showinfo("Atendido", f"Nombre: {paciente.nombre}\nDNI: {paciente.dni}\nEmergencia: {paciente.nivelEmergencia}\nTiempo: {paciente.tiempoAtencion} min")
    else:
        messagebox.showwarning("Atención", "No hay pacientes por atender.")

def ver_pendientes():
    pendientes = sistema.pacientesPendientes()
    if not pendientes:
        messagebox.showinfo("Pendientes", "No hay pacientes pendientes.")
    else:
        texto = "\n".join([f"{p.nombre} - DNI: {p.dni} - Nivel: {p.nivelEmergencia}, Tiempo: {p.tiempoAtencion} min" for p in pendientes])
        messagebox.showinfo("Pacientes Pendientes", texto)

def ver_resumen():
    total, tiempo = sistema.resumen()
    messagebox.showinfo("Resumen", f"Total atendidos: {total}\nTiempo total: {tiempo} minutos")

# Ventana principal
root = tk.Tk()
root.title("Sistema de Emergencia Hospitalaria")

tk.Label(root, text="Sistema de Emergencia", font=("Arial", 16)).pack(pady=10)

tk.Button(root, text="Agregar Paciente", command=agregar_paciente, width=30, height=2).pack(pady=5)
tk.Button(root, text="Atender Paciente", command=atender_paciente, width=30, height=2).pack(pady=5)
tk.Button(root, text="Ver Pacientes Pendientes", command=ver_pendientes, width=30, height=2).pack(pady=5)
tk.Button(root, text="Ver Resumen de Atención", command=ver_resumen, width=30, height=2).pack(pady=5)
tk.Button(root, text="Salir", command=root.destroy, width=30, height=2, bg="red", fg="white").pack(pady=10)

root.mainloop()

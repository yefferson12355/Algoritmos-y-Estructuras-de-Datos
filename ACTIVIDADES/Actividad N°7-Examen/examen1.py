class Paciente:
    def __init__(self, nombre, dni, nivel_emergencia, tiempo_atencion):
        self.nombre = nombre
        self.dni = dni
        self.nivel_emergencia = nivel_emergencia  # 1-5 (5 más grave)
        self.tiempo_atencion = tiempo_atencion
    
    def __str__(self):
        return f"{self.nombre} - Nivel: {self.nivel_emergencia}"

class ColaPrioridad:
    def __init__(self):
        self.heap = []
    
    def _padre(self, i): return (i - 1) // 2
    def _hijo_izq(self, i): return 2 * i + 1
    def _hijo_der(self, i): return 2 * i + 2
    
    def _tiene_mayor_prioridad(self, i, j):
        return self.heap[i].nivel_emergencia > self.heap[j].nivel_emergencia
    
    def _subir(self, i):
        while i > 0:
            padre = self._padre(i)
            if self._tiene_mayor_prioridad(i, padre):
                self.heap[i], self.heap[padre] = self.heap[padre], self.heap[i]
                i = padre
            else:
                break
    
    def _bajar(self, i):
        while True:
            mayor = i
            izq = self._hijo_izq(i)
            der = self._hijo_der(i)
            
            if izq < len(self.heap) and self._tiene_mayor_prioridad(izq, mayor):
                mayor = izq
            if der < len(self.heap) and self._tiene_mayor_prioridad(der, mayor):
                mayor = der
            
            if mayor != i:
                self.heap[i], self.heap[mayor] = self.heap[mayor], self.heap[i]
                i = mayor
            else:
                break
    
    def insertar(self, paciente):
        self.heap.append(paciente)
        self._subir(len(self.heap) - 1)
    
    def extraer_max(self):
        if not self.heap:
            return None
        
        if len(self.heap) == 1:
            return self.heap.pop()
        
        maximo = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._bajar(0)
        return maximo
    
    def esta_vacia(self):
        return len(self.heap) == 0

class SistemaEmergencia:
    def __init__(self):
        self.cola = ColaPrioridad()
    
    def agregar_paciente(self, nombre, dni, nivel, tiempo):
        paciente = Paciente(nombre, dni, nivel, tiempo)
        self.cola.insertar(paciente)
        print(f"Agregado: {paciente}")
    
    def atender_siguiente(self):
        paciente = self.cola.extraer_max()
        if paciente:
            print(f"Atendiendo: {paciente}")
            return paciente
        else:
            print("No hay pacientes")
            return None
    
    def mostrar_pendientes(self):
        if self.cola.esta_vacia():
            print("No hay pacientes pendientes")
        else:
            print("Pacientes pendientes:")
            for i, p in enumerate(self.cola.heap, 1):
                print(f"{i}. {p}")

# Ejemplo de uso
sistema = SistemaEmergencia()

# Agregar pacientes
sistema.agregar_paciente("Ana", "12345", 2, 15)
sistema.agregar_paciente("Carlos", "54321", 5, 30)
sistema.agregar_paciente("María", "11111", 3, 20)

# Ver pendientes
sistema.mostrar_pendientes()

# Atender pacientes por prioridad
sistema.atender_siguiente()
sistema.atender_siguiente()
sistema.mostrar_pendientes()
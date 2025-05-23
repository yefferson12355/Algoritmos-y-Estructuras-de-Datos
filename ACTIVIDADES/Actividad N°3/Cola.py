from collections import deque

class Cola:
    def __init__(self):
        self.elementos = deque()
    
    def enqueue(self, valor):
        """Insertar elemento (enqueue)"""
        self.elementos.append(valor)
        print(f"Insertado: {valor}")
    
    def dequeue(self):
        """Eliminar elemento (dequeue)"""
        if not self.elementos:
            print("Error: Cola vacía")
            return None
        valor = self.elementos.popleft()
        print(f"Eliminado: {valor}")
        return valor
    
    def frente(self):
        """Mostrar el frente"""
        if not self.elementos:
            print("Cola vacía")
            return None
        return self.elementos[0]
    
    def mostrar(self):
        """Recorrer cola"""
        if not self.elementos:
            print("Cola vacía")
            return
        print("Estado de la cola (frente -> final):", end=" ")
        for elemento in self.elementos:
            print(elemento, end=" ")
        print()
    
    def esta_vacia(self):
        return len(self.elementos) == 0
    
    def tamaño(self):
        return len(self.elementos)

# Función principal
def main():
    cola = Cola()
    
    print("=== IMPLEMENTACIÓN DE COLA EN PYTHON ===")
    
    # Insertar elementos: 3, 6, 9, 12
    print("\n1. Insertando elementos:")
    cola.enqueue(3)
    cola.enqueue(6)
    cola.enqueue(9)
    cola.enqueue(12)
    
    print("\nEstado después de insertar:")
    cola.mostrar()
    print(f"Frente actual: {cola.frente()}")
    
    # Eliminar un elemento
    print("\n2. Eliminando un elemento:")
    cola.dequeue()
    
    # Mostrar cola final
    print("\n3. Estado final:")
    cola.mostrar()
    print(f"Frente final: {cola.frente()}")

if __name__ == "__main__":
    main()

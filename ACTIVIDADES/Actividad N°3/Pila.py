class Pila:
    def __init__(self):
        self.elementos = []
    
    def push(self, valor):
        """Insertar elemento (push)"""
        self.elementos.append(valor)
        print(f"Insertado: {valor}")
    
    def pop(self):
        """Eliminar elemento (pop)"""
        if not self.elementos:
            print("Error: Pila vacía")
            return None
        valor = self.elementos.pop()
        print(f"Eliminado: {valor}")
        return valor
    
    def tope(self):
        """Mostrar el tope"""
        if not self.elementos:
            print("Pila vacía")
            return None
        return self.elementos[-1]
    
    def mostrar(self):
        """Recorrer pila"""
        if not self.elementos:
            print("Pila vacía")
            return
        print("Estado de la pila (tope -> base):", end=" ")
        for i in range(len(self.elementos) - 1, -1, -1):
            print(self.elementos[i], end=" ")
        print()
    
    def esta_vacia(self):
        return len(self.elementos) == 0

# Función principal para ejecutar las operaciones
def main():
    pila = Pila()
    
    print("=== IMPLEMENTACIÓN DE PILA EN PYTHON ===")
    
    # Insertar elementos: 5, 10, 15, 20, 25
    print("\n1. Insertando elementos:")
    pila.push(5)
    pila.push(10)
    pila.push(15)
    pila.push(20)
    pila.push(25)
    
    print("\nEstado después de insertar:")
    pila.mostrar()
    print(f"Tope actual: {pila.tope()}")
    
    # Eliminar dos elementos consecutivos
    print("\n2. Eliminando dos elementos:")
    pila.pop()
    pila.pop()
    
    # Mostrar estado final
    print("\n3. Estado final:")
    pila.mostrar()
    print(f"Tope final: {pila.tope()}")

if __name__ == "__main__":
    main()

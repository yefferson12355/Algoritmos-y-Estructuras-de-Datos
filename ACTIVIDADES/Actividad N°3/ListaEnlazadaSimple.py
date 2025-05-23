class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None

class ListaEnlazada:
    def __init__(self):
        self.cabeza = None
    
    def insertar_al_inicio(self, valor):
        """Insertar al inicio"""
        nuevo_nodo = Nodo(valor)
        nuevo_nodo.siguiente = self.cabeza
        self.cabeza = nuevo_nodo
        print(f"Insertado al inicio: {valor}")
    
    def insertar_al_final(self, valor):
        """Insertar al final"""
        nuevo_nodo = Nodo(valor)
        
        if self.cabeza is None:
            self.cabeza = nuevo_nodo
        else:
            actual = self.cabeza
            while actual.siguiente is not None:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo
        print(f"Insertado al final: {valor}")
    
    def eliminar_del_inicio(self):
        """Eliminar del inicio"""
        if self.cabeza is None:
            print("Error: Lista vacía")
            return None
        
        valor = self.cabeza.dato
        self.cabeza = self.cabeza.siguiente
        print(f"Eliminado del inicio: {valor}")
        return valor
    
    def mostrar(self):
        """Mostrar lista"""
        if self.cabeza is None:
            print("Lista vacía")
            return
        
        print("Recorrido completo: ", end="")
        actual = self.cabeza
        while actual is not None:
            print(actual.dato, end="")
            if actual.siguiente is not None:
                print(" -> ", end="")
            actual = actual.siguiente
        print(" -> NULL")
    
    def esta_vacia(self):
        return self.cabeza is None

# Función principal
def main():
    lista = ListaEnlazada()
    
    print("=== IMPLEMENTACIÓN DE LISTA ENLAZADA EN PYTHON ===")
    
    # Insertar al inicio los valores: 8, 4
    print("\n1. Insertando al inicio:")
    lista.insertar_al_inicio(8)
    lista.insertar_al_inicio(4)
    
    print("\nEstado después de insertar al inicio:")
    lista.mostrar()
    
    # Insertar al final el valor: 11
    print("\n2. Insertando al final:")
    lista.insertar_al_final(11)
    
    print("\nEstado después de insertar al final:")
    lista.mostrar()
    
    # Eliminar el primer nodo
    print("\n3. Eliminando el primer nodo:")
    lista.eliminar_del_inicio()
    
    # Mostrar el recorrido completo
    print("\n4. Recorrido final:")
    lista.mostrar()

if __name__ == "__main__":
    main()

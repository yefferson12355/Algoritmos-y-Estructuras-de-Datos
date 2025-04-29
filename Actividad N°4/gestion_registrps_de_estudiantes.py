class Nodo:
    def __init__(self, id, nombre, correo, escuela, anio):
        self.id = id
        self.nombre = nombre
        self.correo = correo
        self.escuela = escuela
        self.anio = anio
        self.siguiente = None
        self.anterior = None

class ListaDoble:
    def __init__(self):
        self.cabeza = None
        self.contador_id = 1

    def agregar(self, nombre, correo, escuela, anio):
        nuevo = Nodo(self.contador_id, nombre, correo, escuela, anio)
        self.contador_id += 1
        if not self.cabeza:
            self.cabeza = nuevo
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo
            nuevo.anterior = actual

    def mostrar(self):
        actual = self.cabeza
        while actual:
            print(f"{actual.id} - {actual.nombre} - {actual.correo} - {actual.escuela} - {actual.anio}")
            actual = actual.siguiente

    def buscar(self, criterio):
        actual = self.cabeza
        while actual:
            if str(actual.id) == str(criterio) or actual.nombre.lower() == str(criterio).lower():
                print(f"Encontrado: {actual.id} - {actual.nombre}")
                return actual
            actual = actual.siguiente
        print("No encontrado.")
        return None

    def modificar(self, id, nuevo_nombre, nuevo_correo, nueva_escuela, nuevo_anio):
        nodo = self.buscar(id)
        if nodo:
            nodo.nombre = nuevo_nombre
            nodo.correo = nuevo_correo
            nodo.escuela = nueva_escuela
            nodo.anio = nuevo_anio
            print("Registro modificado.")

    def eliminar(self, id):
        actual = self.cabeza
        while actual:
            if actual.id == id:
                if actual.anterior:
                    actual.anterior.siguiente = actual.siguiente
                else:
                    self.cabeza = actual.siguiente
                if actual.siguiente:
                    actual.siguiente.anterior = actual.anterior
                print("Registro eliminado.")
                return
            actual = actual.siguiente
        print("No encontrado.")

    def guardar(self, archivo='estudiantes.txt'):
        with open(archivo, 'w') as f:
            actual = self.cabeza
            while actual:
                f.write(f"{actual.id},{actual.nombre},{actual.correo},{actual.escuela},{actual.anio}\n")
                actual = actual.siguiente
        print("Datos guardados.")

    def cargar(self, archivo='estudiantes.txt'):
        try:
            with open(archivo, 'r') as f:
                for linea in f:
                    partes = linea.strip().split(',')
                    if len(partes) == 5:
                        self.agregar(partes[1], partes[2], partes[3], int(partes[4]))
        except FileNotFoundError:
            print("Archivo no encontrado, iniciando lista vacía.")

def menu():
    lista = ListaDoble()
    lista.cargar()

    while True:
        print("\n--- MENÚ ---")
        print("1. Agregar estudiante")
        print("2. Mostrar estudiantes")
        print("3. Buscar estudiante por ID o nombre")
        print("4. Modificar estudiante")
        print("5. Eliminar estudiante")
        print("6. Guardar en archivo")
        print("0. Salir")
        opcion = input("Opción: ")

        if opcion == '1':
            nombre = input("Nombre: ")
            correo = input("Correo: ")
            escuela = input("Escuela: ")
            anio = int(input("Año: "))
            lista.agregar(nombre, correo, escuela, anio)

        elif opcion == '2':
            lista.mostrar()

        elif opcion == '3':
            criterio = input("ID o nombre a buscar: ")
            lista.buscar(criterio)

        elif opcion == '4':
            id_mod = int(input("ID a modificar: "))
            nombre = input("Nuevo nombre: ")
            correo = input("Nuevo correo: ")
            escuela = input("Nueva escuela: ")
            anio = int(input("Nuevo año: "))
            lista.modificar(id_mod, nombre, correo, escuela, anio)

        elif opcion == '5':
            id_elim = int(input("ID a eliminar: "))
            lista.eliminar(id_elim)

        elif opcion == '6':
            lista.guardar()

        elif opcion == '0':
            lista.guardar()
            break

        else:
            print("Opción inválida.")

menu()

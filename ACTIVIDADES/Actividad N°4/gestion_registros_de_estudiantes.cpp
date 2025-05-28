#include <iostream>
#include <string>
#include <fstream>

using namespace std;
class Nodo {
    public:
     Nodo* siguiente;
     Nodo* anterior;
     int id;
     string nombre;
     string correo;
     string escuela;
     int anio;
     

     Nodo(int id, string nombre, string correo, string escuela, int anio) {
        this->id = id;
        this->nombre = nombre;
        this->correo = correo;
        this->escuela = escuela;
        this->anio = anio;
        siguiente = nullptr;
        anterior = nullptr;
     }
};


class ListaDoble {
    private:
        Nodo* cabeza;
        int contadorId;
    
    public:
        ListaDoble() {
            cabeza = nullptr;
            contadorId = 1;
        }
    
        Nodo* getCabeza() { return cabeza; }
    
        void setCabeza(Nodo* nuevoCabeza) { cabeza = nuevoCabeza; }
    
     void agregar(string nombre, string correo, string escuela, int anio) 
     {
        Nodo* nuevo = new Nodo(contadorId++, nombre, correo, escuela, anio);
            //1
        if (cabeza == nullptr) {
        cabeza = nuevo;
        } else {//2
        Nodo* actual = cabeza;

        while (actual->siguiente != nullptr) {
            actual = actual->siguiente;
        }
        actual->siguiente = nuevo;
        nuevo->anterior = actual;

        }
     }
     void mostrar() {
        Nodo* actual = cabeza;

        while (actual != nullptr) {
            cout << actual->id << " - " << actual->nombre << " - " << 
            actual->correo << endl;
            actual = actual->siguiente;
        }
     }
     void buscar(int id) {
        Nodo* actual = cabeza;

        while (actual != nullptr) {
            if (actual->id == id) {
                cout << "Encontrado: " << actual->nombre << endl;
                return;
            }
            actual = actual->siguiente;
        }
        cout << "No encontrado." << endl;
     }
     void modificar(int id, string nuevoNombre, string nuevoCorreo, string nuevaEscuela, int nuevoAnio) {
        Nodo* actual = cabeza;

        while (actual != nullptr) {
            if (actual->id == id) {
                actual->nombre = nuevoNombre;
                actual->correo = nuevoCorreo;
                actual->escuela = nuevaEscuela;
                actual->anio = nuevoAnio;
                cout << "Registro modificado." << endl;
                return;
            }
            actual = actual->siguiente;
        }
        cout << "No encontrado." << endl;
     }
     void eliminar(int id) {
        Nodo* actual = cabeza;

        while (actual != nullptr) {
            if (actual->id == id) {
                if (actual->anterior != nullptr) {
                    actual->anterior->siguiente = actual->siguiente;
                } else {
                    cabeza = actual->siguiente; // Si es el primero
                }
                if (actual->siguiente != nullptr) {
                    actual->siguiente->anterior = actual->anterior;
                }
                delete actual;
                cout << "Registro eliminado." << endl;
                return;
            }
            actual = actual->siguiente;
        }
        cout << "No encontrado." << endl;
     }
     void guardar() {
        ofstream archivo("datos.txt");
        if (!archivo) {
            cout << "Error al abrir el archivo para guardar." << endl;
            return;
        }
        Nodo* actual = cabeza;
        while (actual != nullptr) {
            archivo << actual->id << ";" << actual->nombre << ";" << actual->correo << ";"
                    << actual->escuela << ";" << actual->anio << endl;
            actual = actual->siguiente;
        }
        archivo.close();
        cout << "Datos guardados correctamente." << endl;
    }
    void cargar() {
        ifstream archivo("datos.txt");
        if (!archivo) {
            cout << "Archivo no encontrado. No se cargaron datos." << endl;
            return;
        }
        string linea;
        while (getline(archivo, linea)) {
            int id, anio;
            string nombre, correo, escuela;
            size_t pos = 0;

            // Parsear ID
            pos = linea.find(";");
            id = stoi(linea.substr(0, pos));
            linea.erase(0, pos + 1);

            // Parsear nombre
            pos = linea.find(";");
            nombre = linea.substr(0, pos);
            linea.erase(0, pos + 1);

            // Parsear correo
            pos = linea.find(";");
            correo = linea.substr(0, pos);
            linea.erase(0, pos + 1);

            // Parsear escuela
            pos = linea.find(";");
            escuela = linea.substr(0, pos);
            linea.erase(0, pos + 1);

            // Parsear año
            anio = stoi(linea);

            Nodo* nuevo = new Nodo(id, nombre, correo, escuela, anio);
            if (cabeza == nullptr) {
                cabeza = nuevo;
            } else {
                Nodo* actual = cabeza;
                while (actual->siguiente != nullptr) {
                    actual = actual->siguiente;
                }
                actual->siguiente = nuevo;
                nuevo->anterior = actual;
            }

            if (id >= contadorId) {
                contadorId = id + 1;
            }
        }
        archivo.close();
        cout << "Datos cargados correctamente." << endl;
    }
};

int main() {
    ListaDoble lista;
    lista.cargar(); // Cargar datos al iniciar

    int opcion;
    do {
        cout << "\n----- MENU PRINCIPAL -----\n";
        cout << "1. Agregar nuevo estudiante\n";
        cout << "2. Mostrar todos los estudiantes\n";
        cout << "3. Buscar estudiante por ID o nombre\n";
        cout << "4. Modificar estudiante\n";
        cout << "5. Eliminar estudiante por ID\n";
        cout << "6. Guardar datos en archivo\n";
        cout << "0. Salir\n";
        cout << "Seleccione una opcion: ";
        cin >> opcion;
        cin.ignore(); // Limpiar buffer

        if (opcion == 1) {
            string nombre, correo, escuela;
            int anio;
            cout << "Nombre: ";
            getline(cin, nombre);
            cout << "Correo: ";
            getline(cin, correo);
            cout << "Escuela: ";
            getline(cin, escuela);
            cout << "Anio de ingreso: ";
            cin >> anio;
            cin.ignore();
            lista.agregar(nombre, correo, escuela, anio);
            cout << "Estudiante agregado.\n";
        } else if (opcion == 2) {
            lista.mostrar();
        } else if (opcion == 3) {
            int subop;
            cout << "Buscar por: 1. ID  2. Nombre\n";
            cin >> subop;
            cin.ignore();
            if (subop == 1) {
                int id;
                cout << "Ingrese ID: ";
                cin >> id;
                cin.ignore();
                lista.buscar(id);
            } else if (subop == 2) {
                string nombre;
                cout << "Ingrese nombre: ";
                getline(cin, nombre);
                Nodo* actual = lista.getCabeza(); // Accedemos al nodo cabeza
                bool encontrado = false;
                while (actual != nullptr) {
                    if (actual->nombre == nombre) {
                        cout << actual->id << " - " << actual->nombre << " - "
                             << actual->correo << " - " << actual->escuela << " - " << actual->anio << endl;
                        encontrado = true;
                    }
                    actual = actual->siguiente;
                }
                if (!encontrado)
                    cout << "No encontrado." << endl;
            }
        } else if (opcion == 4) {
            int id, anio;
            string nombre, correo, escuela;
            cout << "ID del estudiante a modificar: ";
            cin >> id;
            cin.ignore();
            cout << "Nuevo nombre: ";
            getline(cin, nombre);
            cout << "Nuevo correo: ";
            getline(cin, correo);
            cout << "Nueva escuela: ";
            getline(cin, escuela);
            cout << "Nuevo anio de ingreso: ";
            cin >> anio;
            cin.ignore();
            lista.modificar(id, nombre, correo, escuela, anio);
        } else if (opcion == 5) {
            int id;
            cout << "ID del estudiante a eliminar: ";
            cin >> id;
            cin.ignore();
            lista.eliminar(id);
        } else if (opcion == 6) {
            lista.guardar();
        } else if (opcion == 0) {
            lista.guardar(); // Guardar al salir
            cout << "Saliendo y guardando datos...\n";
        } else {
            cout << "Opcion invalida.\n";
        }

    } while (opcion != 0);

    return 0;
}
// Actividad N°4 - Listas Doblemente Enlazadas
// Integrantes: yo y chat gpt
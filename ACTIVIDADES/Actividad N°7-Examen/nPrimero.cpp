#include <iostream>   
#include <vector>     
#include <string>     I

using namespace std;


struct Paciente {
    string nombre;
    string dni;
    int nivelEmergencia;      
    int tiempoAtencion;       

    
    Paciente(string n, string d, int nivel, int tiempo) {
        nombre = n;
        dni = d;
        nivelEmergencia = nivel;
        tiempoAtencion = tiempo;
    }
};


class SistemaEmergencia {
private:
    vector<Paciente> heap; 

    
    void subir(int i) {
        while (i > 0) {
            int padre = (i - 1) / 2;
            // Comparar por nivel de emergencia: menor valor = mayor prioridad
            if (heap[i].nivelEmergencia < heap[padre].nivelEmergencia) {
                swap(heap[i], heap[padre]); // Intercambiar con el padre si tiene mayor prioridad
                i = padre;
            } else break;
        }
    }

    // Función para mantener el heap al eliminar (heapify-down)
    void bajar(int i) {
        int n = heap.size();
        while (true) {
            int izq = 2 * i + 1;
            int der = 2 * i + 2;
            int menor = i;

            if (izq < n && heap[izq].nivelEmergencia < heap[menor].nivelEmergencia)
                menor = izq;
            if (der < n && heap[der].nivelEmergencia < heap[menor].nivelEmergencia)
                menor = der;

            if (menor != i) {
                swap(heap[i], heap[menor]); // Intercambiar con el hijo menor
                i = menor;
            } else break;
        }
    }

    int totalAtendidos = 0;    // Contador de pacientes atendidos
    int tiempoTotal = 0;       // Acumulador de tiempo total de atención

public:
    // Insertar un nuevo paciente al sistema
    void agregarPaciente(Paciente p) {
        heap.push_back(p);    // Insertar al final del vector
        subir(heap.size() - 1); // Ajustar heap hacia arriba
    }

    // Atender al paciente con mayor prioridad
    void atenderPaciente() {
        if (heap.empty()) {
            cout << "No hay pacientes para atender.\n";
            return;
        }
        Paciente atendido = heap[0];              // El paciente más grave está al inicio
        cout << "Atendiendo a: " << atendido.nombre << " (DNI: " << atendido.dni << ")\n";
        cout << "Nivel de emergencia: " << atendido.nivelEmergencia << ", Tiempo: " << atendido.tiempoAtencion << " minutos\n";

        totalAtendidos++;                         // Incrementar contador
        tiempoTotal += atendido.tiempoAtencion;   // Acumular tiempo

        heap[0] = heap.back();     // Reemplazar raíz con el último
        heap.pop_back();           // Eliminar el último
        bajar(0);                  // Ajustar heap hacia abajo
    }

    // Mostrar pacientes pendientes en tiempo real
    void mostrarPendientes() {
        if (heap.empty()) {
            cout << "No hay pacientes pendientes.\n";
            return;
        }
        cout << "\nLista de pacientes pendientes:\n";
        for (auto& p : heap) {
            cout << "- " << p.nombre << " (DNI: " << p.dni << ") - Emergencia: " << p.nivelEmergencia << ", Tiempo: " << p.tiempoAtencion << " min\n";
        }
    }

    // Mostrar resumen de atención
    void mostrarResumen() {
        cout << "\nTotal de pacientes atendidos: " << totalAtendidos << endl;
        cout << "Tiempo total de atencion: " << tiempoTotal << " minutos\n";
    }
};

// Función principal para simular la atención
int main() {
    SistemaEmergencia sistema;
    int opcion;

    do {
        cout << "\n--- MENU ---\n";
        cout << "1. Agregar paciente\n";
        cout << "2. Atender paciente\n";
        cout << "3. Ver pacientes pendientes\n";
        cout << "4. Ver resumen de atencion\n";
        cout << "5. Salir\n";
        cout << "Seleccione una opcion: ";
        cin >> opcion;

        if (opcion == 1) {
            string nombre, dni;
            int nivel, tiempo;
            cout << "Nombre: "; cin.ignore(); getline(cin, nombre);
            cout << "DNI: "; getline(cin, dni);
            cout << "Nivel de emergencia (1-5): "; cin >> nivel;
            cout << "Tiempo estimado de atencion (min): "; cin >> tiempo;

            sistema.agregarPaciente(Paciente(nombre, dni, nivel, tiempo));
        }
        else if (opcion == 2) {
            sistema.atenderPaciente();
        }
        else if (opcion == 3) {
            sistema.mostrarPendientes();
        }
        else if (opcion == 4) {
            sistema.mostrarResumen();
        }

    } while (opcion != 5);

    return 0;
}

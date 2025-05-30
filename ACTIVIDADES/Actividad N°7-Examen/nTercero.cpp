#include <iostream>
#include <string>
#include <vector>
using namespace std;

// Función para mostrar el historial actual de acciones
void mostrarHistorial(const vector<string>& historial) {
    cout << "Historial actual (más reciente al final):\n";
    for (int i = 0; i < historial.size(); i++) {
        cout << i + 1 << ". " << historial[i] << endl;
    }
    cout << "-----------------------------\n";
}

int main() {
    vector<string> historial; // Pila de acciones realizadas (máx 10)
    vector<string> rehacer;   // Pila de acciones deshechas

    int opcion;
    string accion;

    do {
        cout << "\n--- MENÚ DE COMANDOS ---\n";
        cout << "[1] Dibujar\n";
        cout << "[2] Mover\n";
        cout << "[3] Eliminar\n";
        cout << "[4] Deshacer\n";
        cout << "[5] Rehacer\n";
        cout << "[0] Salir\n";
        cout << "Seleccione una opción: ";
        cin >> opcion;

        switch (opcion) {
            case 1:
                accion = "Dibujar";
                break;
            case 2:
                accion = "Mover";
                break;
            case 3:
                accion = "Eliminar";
                break;
            case 4: // DESHACER
                if (!historial.empty()) {
                    rehacer.push_back(historial.back()); // Última acción va a pila rehacer
                    historial.pop_back(); // Se elimina del historial
                    cout << "Deshecho.\n";
                } else {
                    cout << "No hay acciones para deshacer.\n";
                }
                mostrarHistorial(historial);
                continue;
            case 5: // REHACER
                if (!rehacer.empty()) {
                    historial.push_back(rehacer.back()); // Se vuelve a hacer la acción
                    rehacer.pop_back(); // Se elimina de la pila rehacer
                    cout << "Rehecho.\n";
                } else {
                    cout << "No hay acciones para rehacer.\n";
                }
                mostrarHistorial(historial);
                continue;
            case 0:
                cout << "Saliendo...\n";
                break;
            default:
                cout << "Opción inválida.\n";
                continue;
        }

        // Si fue una acción nueva (1 a 3)
        if (opcion >= 1 && opcion <= 3) {
            if (historial.size() == 10) {
                historial.erase(historial.begin()); // Se elimina la más antigua
            }
            historial.push_back(accion); // Se agrega la nueva acción
            rehacer.clear(); // Al hacer una nueva acción se pierde la posibilidad de rehacer
            cout << "Acción realizada: " << accion << endl;
            mostrarHistorial(historial);
        }

    } while (opcion != 0);

    return 0;
}

#include <windows.h>
#include <string>
#include <vector> //array dinamico.
#include <sstream>
using namespace std;
//AVl  , metodo izqueirdista, uphigtj, dowhijw, Tipos de prioridad.
struct Paciente {
    string nombre;
    string dni;
    int nivelEmergencia;//prioridad
    int tiempoAtencion;

    Paciente(string n, string d, int nivel, int tiempo)
        : nombre(n), dni(d), nivelEmergencia(nivel), tiempoAtencion(tiempo) {}
};

class SistemaEmergencia {
private:
    vector<Paciente> heap;
    int totalAtendidos = 0;
    int tiempoTotal = 0;

    void subir(int i) {
        while (i > 0) {
            int padre = (i - 1) / 2;
            if (heap[i].nivelEmergencia < heap[padre].nivelEmergencia) {
                swap(heap[i], heap[padre]);
                i = padre;
            } else break;
        }
    }

    void bajar(int i) {
        int n = heap.size();
        while (true) {
            int izq = 2 * i + 1;
            int der = 2 * i + 2;
            int menor = i;
            if (izq < n && heap[izq].nivelEmergencia < heap[menor].nivelEmergencia) menor = izq;
            if (der < n && heap[der].nivelEmergencia < heap[menor].nivelEmergencia) menor = der;
            if (menor != i) {
                swap(heap[i], heap[menor]);
                i = menor;
            } else break;
        }
    }

public:
    void agregarPaciente(Paciente p) {
        heap.push_back(p);
        subir(heap.size() - 1);
    }

    void atenderPaciente(HWND hEstado) {
        if (heap.empty()) {
            SetWindowText(hEstado, "No hay pacientes para atender.");
            return;
        }
        Paciente atendido = heap[0];
        stringstream ss;
        ss << "Atendiendo a: " << atendido.nombre << " (DNI: " << atendido.dni << ") - Nivel: "
           << atendido.nivelEmergencia << ", Tiempo: " << atendido.tiempoAtencion << " min";

        totalAtendidos++;
        tiempoTotal += atendido.tiempoAtencion;

        heap[0] = heap.back();
        heap.pop_back();
        bajar(0);

        SetWindowText(hEstado, ss.str().c_str());
    }

    void mostrarPendientes(HWND lista) {
        SendMessage(lista, LB_RESETCONTENT, 0, 0);
        for (auto& p : heap) {
            stringstream ss;
            ss << p.nombre << " (" << p.dni << ") - Nivel: " << p.nivelEmergencia
               << ", " << p.tiempoAtencion << " min";
            SendMessage(lista, LB_ADDSTRING, 0, (LPARAM)ss.str().c_str());
        }
    }

    void mostrarResumen(HWND hEstado) {
        stringstream ss;
        ss << "Total atendidos: " << totalAtendidos << ", Tiempo total: " << tiempoTotal << " min";
        SetWindowText(hEstado, ss.str().c_str());
    }
};

SistemaEmergencia sistema;
HWND hNombre, hDNI, hNivel, hTiempo, hLista, hEstado;

void CrearControles(HWND hwnd) {
    CreateWindow("STATIC", "SISTEMA DE EMERGENCIA", WS_VISIBLE | WS_CHILD, 20, 10, 200, 20, hwnd, NULL, NULL, NULL);
    CreateWindow("STATIC", "Nombre:", WS_VISIBLE | WS_CHILD, 20, 40, 50, 20, hwnd, NULL, NULL, NULL);
    hNombre = CreateWindow("EDIT", "", WS_VISIBLE | WS_CHILD | WS_BORDER, 80, 40, 120, 20, hwnd, NULL, NULL, NULL);

    CreateWindow("STATIC", "DNI:", WS_VISIBLE | WS_CHILD, 220, 40, 40, 20, hwnd, NULL, NULL, NULL);
    hDNI = CreateWindow("EDIT", "", WS_VISIBLE | WS_CHILD | WS_BORDER, 260, 40, 100, 20, hwnd, NULL, NULL, NULL);

    CreateWindow("STATIC", "Nivel (1-5):", WS_VISIBLE | WS_CHILD, 20, 70, 80, 20, hwnd, NULL, NULL, NULL);
    hNivel = CreateWindow("EDIT", "", WS_VISIBLE | WS_CHILD | WS_BORDER, 100, 70, 40, 20, hwnd, NULL, NULL, NULL);

    CreateWindow("STATIC", "Tiempo (min):", WS_VISIBLE | WS_CHILD, 160, 70, 80, 20, hwnd, NULL, NULL, NULL);
    hTiempo = CreateWindow("EDIT", "", WS_VISIBLE | WS_CHILD | WS_BORDER, 240, 70, 50, 20, hwnd, NULL, NULL, NULL);

    CreateWindow("BUTTON", "Agregar", WS_VISIBLE | WS_CHILD, 20, 100, 80, 25, hwnd, (HMENU)1, NULL, NULL);
    CreateWindow("BUTTON", "Atender", WS_VISIBLE | WS_CHILD, 110, 100, 80, 25, hwnd, (HMENU)2, NULL, NULL);
    CreateWindow("BUTTON", "Pendientes", WS_VISIBLE | WS_CHILD, 200, 100, 80, 25, hwnd, (HMENU)3, NULL, NULL);
    CreateWindow("BUTTON", "Resumen", WS_VISIBLE | WS_CHILD, 290, 100, 80, 25, hwnd, (HMENU)4, NULL, NULL);

    hLista = CreateWindow("LISTBOX", NULL, WS_VISIBLE | WS_CHILD | WS_BORDER | WS_VSCROLL, 20, 140, 350, 120, hwnd, NULL, NULL, NULL);
    hEstado = CreateWindow("STATIC", "Estado:", WS_VISIBLE | WS_CHILD, 20, 270, 350, 20, hwnd, NULL, NULL, NULL);
}

LRESULT CALLBACK WndProc(HWND hwnd, UINT msg, WPARAM wParam, LPARAM lParam) {
    char b1[100], b2[100], b3[10], b4[10];
    switch (msg) {
    case WM_CREATE:
        CrearControles(hwnd);
        break;
    case WM_COMMAND:
        switch (LOWORD(wParam)) {
        case 1:
            GetWindowText(hNombre, b1, 100);
            GetWindowText(hDNI, b2, 100);
            GetWindowText(hNivel, b3, 10);
            GetWindowText(hTiempo, b4, 10);
            sistema.agregarPaciente(Paciente(b1, b2, atoi(b3), atoi(b4)));
            SetWindowText(hEstado, "Paciente agregado");
            break;
        case 2:
            sistema.atenderPaciente(hEstado);
            break;
        case 3:
            sistema.mostrarPendientes(hLista);
            break;
        case 4:
            sistema.mostrarResumen(hEstado);
            break;
        }
        break;
    case WM_DESTROY:
        PostQuitMessage(0);
        break;
    default:
        return DefWindowProc(hwnd, msg, wParam, lParam);
    }
    return 0;
}

int WINAPI WinMain(HINSTANCE hInst, HINSTANCE hPrev, LPSTR args, int nCmdShow) {
    WNDCLASSW wc = {0};
    wc.hbrBackground = (HBRUSH)COLOR_WINDOW;
    wc.hCursor = LoadCursor(NULL, IDC_ARROW);
    wc.hInstance = hInst;
    wc.lpszClassName = L"EmergenciaClase";
    wc.lpfnWndProc = WndProc;

    if (!RegisterClassW(&wc)) return -1;
    CreateWindowW(L"EmergenciaClase", L"Sistema de Emergencia", WS_OVERLAPPEDWINDOW | WS_VISIBLE,
                  100, 100, 420, 350, NULL, NULL, NULL, NULL);

    MSG msg = {0};
    while (GetMessage(&msg, NULL, 0, 0)) {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }
    return 0;
}

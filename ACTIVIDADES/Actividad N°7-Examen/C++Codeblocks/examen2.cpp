#include <windows.h>
#include <map>
#include <vector>
#include <string>
#include <queue> // Para BFS
#include <set>

using namespace std;

// Estructura base del grafo
map<string, vector<string>> grafo;

// Handles
HWND hNodoA, hNodoB, hInicio, hFin, hListbox, hEstado;

void AgregarConexion(const string& a, const string& b) {
    grafo[a].push_back(b);
    grafo[b].push_back(a);
}

bool ExisteCamino(const string& inicio, const string& fin) {
    set<string> visitado;
    queue<string> q;
    q.push(inicio);
    visitado.insert(inicio);
    while (!q.empty()) {
        string actual = q.front(); q.pop();
        if (actual == fin) return true;
        for (const auto& vecino : grafo[actual]) {
            if (!visitado.count(vecino)) {
                q.push(vecino);
                visitado.insert(vecino);
            }
        }
    }
    return false;
}

void DFS(string actual, string destino, vector<string>& ruta, set<string>& visitado, vector<vector<string>>& rutas) {
    ruta.push_back(actual);
    visitado.insert(actual);
    if (actual == destino) {
        rutas.push_back(ruta);
    } else {
        for (const auto& vecino : grafo[actual]) {
            if (!visitado.count(vecino)) {
                DFS(vecino, destino, ruta, visitado, rutas);
            }
        }
    }
    ruta.pop_back();
    visitado.erase(actual);
}

void MostrarTodasLasRutas(HWND hListbox, const string& inicio, const string& fin) {
    vector<vector<string>> rutas;
    vector<string> ruta;
    set<string> visitado;
    DFS(inicio, fin, ruta, visitado, rutas);

    SendMessage(hListbox, LB_RESETCONTENT, 0, 0);
    int i = 1;
    for (const auto& r : rutas) {
        string s = "Ruta " + to_string(i++) + ": ";
        for (const string& nodo : r) s += nodo + " ";
        SendMessage(hListbox, LB_ADDSTRING, 0, (LPARAM)s.c_str());
    }
}

void ActualizarEstado(const string& mensaje) {
    SetWindowText(hEstado, mensaje.c_str());
}

void CrearControles(HWND hwnd) {
    CreateWindow("STATIC", "Nodo A:", WS_VISIBLE | WS_CHILD, 20, 20, 50, 20, hwnd, NULL, NULL, NULL);
    hNodoA = CreateWindow("EDIT", "", WS_VISIBLE | WS_CHILD | WS_BORDER, 70, 20, 80, 20, hwnd, NULL, NULL, NULL);

    CreateWindow("STATIC", "Nodo B:", WS_VISIBLE | WS_CHILD, 160, 20, 50, 20, hwnd, NULL, NULL, NULL);
    hNodoB = CreateWindow("EDIT", "", WS_VISIBLE | WS_CHILD | WS_BORDER, 210, 20, 80, 20, hwnd, NULL, NULL, NULL);

    CreateWindow("BUTTON", "Agregar Conexion", WS_VISIBLE | WS_CHILD, 300, 20, 130, 25, hwnd, (HMENU)1, NULL, NULL);

    CreateWindow("STATIC", "Inicio:", WS_VISIBLE | WS_CHILD, 20, 60, 50, 20, hwnd, NULL, NULL, NULL);
    hInicio = CreateWindow("EDIT", "", WS_VISIBLE | WS_CHILD | WS_BORDER, 70, 60, 80, 20, hwnd, NULL, NULL, NULL);

    CreateWindow("STATIC", "Fin:", WS_VISIBLE | WS_CHILD, 160, 60, 40, 20, hwnd, NULL, NULL, NULL);
    hFin = CreateWindow("EDIT", "", WS_VISIBLE | WS_CHILD | WS_BORDER, 210, 60, 80, 20, hwnd, NULL, NULL, NULL);

    CreateWindow("BUTTON", "Verificar Camino", WS_VISIBLE | WS_CHILD, 300, 60, 130, 25, hwnd, (HMENU)2, NULL, NULL);
    CreateWindow("BUTTON", "Mostrar Rutas", WS_VISIBLE | WS_CHILD, 300, 90, 130, 25, hwnd, (HMENU)3, NULL, NULL);

    hListbox = CreateWindow("LISTBOX", NULL, WS_VISIBLE | WS_CHILD | WS_BORDER | WS_VSCROLL, 20, 100, 270, 150, hwnd, NULL, NULL, NULL);

    hEstado = CreateWindow("STATIC", "Estado: ", WS_VISIBLE | WS_CHILD, 20, 260, 410, 20, hwnd, NULL, NULL, NULL);
}

LRESULT CALLBACK WindowProc(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam) {
    switch (uMsg) {
    case WM_CREATE:
        CrearControles(hwnd);
        break;
    case WM_COMMAND:
        if (LOWORD(wParam) == 1) { // Agregar conexion
            char a[50], b[50];
            GetWindowText(hNodoA, a, 50);
            GetWindowText(hNodoB, b, 50);
            if (strlen(a) > 0 && strlen(b) > 0) {
                AgregarConexion(a, b);
                ActualizarEstado("Conexion agregada correctamente.");
            }
        } else if (LOWORD(wParam) == 2) { // Verificar camino
            char s[50], t[50];
            GetWindowText(hInicio, s, 50);
            GetWindowText(hFin, t, 50);
            if (ExisteCamino(s, t)) {
                ActualizarEstado("Existe un camino entre los nodos.");
            } else {
                ActualizarEstado("No existe camino entre los nodos.");
            }
        } else if (LOWORD(wParam) == 3) { // Mostrar rutas
            char s[50], t[50];
            GetWindowText(hInicio, s, 50);
            GetWindowText(hFin, t, 50);
            MostrarTodasLasRutas(hListbox, s, t);
            ActualizarEstado("Rutas mostradas en la lista.");
        }
        break;
    case WM_DESTROY:
        PostQuitMessage(0);
        return 0;
    }
    return DefWindowProc(hwnd, uMsg, wParam, lParam);
}

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE, LPSTR, int nCmdShow) {
    const char CLASS_NAME[] = "AnalizadorRutas";

    WNDCLASS wc = {};
    wc.lpfnWndProc = WindowProc;
    wc.hInstance = hInstance;
    wc.lpszClassName = CLASS_NAME;

    RegisterClass(&wc);

    HWND hwnd = CreateWindowEx(0, CLASS_NAME, "Analizador de Rutas", WS_OVERLAPPEDWINDOW,
        CW_USEDEFAULT, CW_USEDEFAULT, 480, 340, NULL, NULL, hInstance, NULL);

    if (hwnd == NULL) return 0;

    ShowWindow(hwnd, nCmdShow);
    UpdateWindow(hwnd);

    MSG msg = {};
    while (GetMessage(&msg, NULL, 0, 0)) {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }
    return 0;
}

#include <windows.h> // Librería principal para la API de Windows
#include <string>    // Para manejar texto (std::string)
#include <vector>    // Para usar listas dinámicas
#include <algorithm> // Para usar std::max
#include <chrono>    // Para medir el tiempo con alta precisión
#include <random>    // Para generar números aleatorios



//Asegurarse que este agregado en el proyecto gdi32, Project -> Build options,Linker settings,add, gdi32.
// Usamos el espacio de nombres estándar para mayor comodidad
using namespace std;

// === DECLARACIÓN DE CLASES (Para que el compilador las conozca) ===
class ArbolAVL;
struct NodoAVL;

// =================================================================
// 1. ESTRUCTURA PARA UN NODO DEL ÁRBOL AVL
// =================================================================
struct NodoAVL {
    int id;           // El ID del expediente
    string nombre;    // El nombre asociado al expediente
    int altura;       // La altura del subárbol que nace en este nodo
    NodoAVL* izquierda; // Puntero al hijo izquierdo
    NodoAVL* derecha;   // Puntero al hijo derecho

    // Constructor para crear un nuevo nodo
    NodoAVL(int _id, const string& _nombre) {
        id = _id;
        nombre = _nombre;
        altura = 1; // Un nuevo nodo siempre tiene altura 1
        izquierda = nullptr; // Nace sin hijos
        derecha = nullptr;
    }
};

// =================================================================
// 2. CLASE PARA GESTIONAR EL ÁRBOL AVL COMPLETO
// =================================================================
class ArbolAVL {
private:
    NodoAVL* raiz; // Puntero a la raíz del árbol

    // --- FUNCIONES PRIVADAS RECURSIVAS ---

    // Obtiene la altura de un nodo (0 si es nulo)
    int getAltura(NodoAVL* nodo) {
        return (nodo == nullptr) ? 0 : nodo->altura;
    }

    // Actualiza la altura de un nodo basándose en la de sus hijos
    void actualizarAltura(NodoAVL* nodo) {
        if (nodo != nullptr) {
            nodo->altura = 1 + max(getAltura(nodo->izquierda), getAltura(nodo->derecha));
        }
    }

    // Calcula el factor de balance de un nodo
    int getFactorBalance(NodoAVL* nodo) {
        return (nodo == nullptr) ? 0 : getAltura(nodo->izquierda) - getAltura(nodo->derecha);
    }

    // Rotación simple a la derecha
    NodoAVL* rotarDerecha(NodoAVL* y) {
        NodoAVL* x = y->izquierda;
        NodoAVL* T2 = x->derecha;
        x->derecha = y;
        y->izquierda = T2;
        actualizarAltura(y);
        actualizarAltura(x);
        return x;
    }

    // Rotación simple a la izquierda
    NodoAVL* rotarIzquierda(NodoAVL* x) {
        NodoAVL* y = x->derecha;
        NodoAVL* T2 = y->izquierda;
        y->izquierda = x;
        x->derecha = T2;
        actualizarAltura(x);
        actualizarAltura(y);
        return y;
    }

    // Inserta un nodo y devuelve la nueva raíz del subárbol
    NodoAVL* insertarRec(NodoAVL* nodo, int id, const string& nombre) {
        if (nodo == nullptr) return new NodoAVL(id, nombre);

        if (id < nodo->id) nodo->izquierda = insertarRec(nodo->izquierda, id, nombre);
        else if (id > nodo->id) nodo->derecha = insertarRec(nodo->derecha, id, nombre);
        else return nodo; // No se permiten duplicados

        actualizarAltura(nodo);

        // --- Lógica de Balanceo ---
        int balance = getFactorBalance(nodo);
        // Caso Izquierda-Izquierda
        if (balance > 1 && id < nodo->izquierda->id) return rotarDerecha(nodo);
        // Caso Derecha-Derecha
        if (balance < -1 && id > nodo->derecha->id) return rotarIzquierda(nodo);
        // Caso Izquierda-Derecha
        if (balance > 1 && id > nodo->izquierda->id) {
            nodo->izquierda = rotarIzquierda(nodo->izquierda);
            return rotarDerecha(nodo);
        }
        // Caso Derecha-Izquierda
        if (balance < -1 && id < nodo->derecha->id) {
            nodo->derecha = rotarDerecha(nodo->derecha);
            return rotarIzquierda(nodo);
        }

        return nodo;
    }

    // Función para liberar la memoria de todo el árbol (CRÍTICO en C++)
    void destruirArbol(NodoAVL* nodo) {
        if (nodo != nullptr) {
            destruirArbol(nodo->izquierda);
            destruirArbol(nodo->derecha);
            delete nodo;
        }
    }

public:
    // Constructor
    ArbolAVL() {
        raiz = nullptr;
    }

    // Destructor: se llama automáticamente al final del programa
    ~ArbolAVL() {
        destruirArbol(raiz);
    }

    // --- FUNCIONES PÚBLICAS ---
    void insertar(int id, const string& nombre) {
        raiz = insertarRec(raiz, id, nombre);
    }

    string buscar(int id) {
        NodoAVL* actual = raiz;
        while (actual != nullptr) {
            if (id == actual->id) return actual->nombre;
            actual = (id < actual->id) ? actual->izquierda : actual->derecha;
        }
        return "NO ENCONTRADO";
    }

    NodoAVL* getRaiz() { return raiz; }
};

// =================================================================
// 3. PARTE GRÁFICA (API DE WINDOWS)
// =================================================================

// --- Variables Globales para los Controles y el Árbol ---
HWND hInputId, hInputNombre, hBotonInsertar, hBotonBuscar, hBotonMasivo, hTextoSalida;
ArbolAVL* arbolExpedientes;

// --- Prototipos ---
LRESULT CALLBACK WndProc(HWND, UINT, WPARAM, LPARAM);
void CrearControles(HWND);
void DibujarArbol(HDC hdc, NodoAVL* nodo, int x, int y, int separacion);

// --- Punto de Entrada ---
int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow) {
    arbolExpedientes = new ArbolAVL(); // Creamos la instancia del árbol

    WNDCLASSEX wc = {0};
    wc.cbSize = sizeof(WNDCLASSEX);
    wc.lpfnWndProc = WndProc;
    wc.hInstance = hInstance;
    wc.hbrBackground = (HBRUSH)(COLOR_WINDOW + 1);
    wc.lpszClassName = "VentanaAVL";
    RegisterClassEx(&wc);

    HWND hwnd = CreateWindowEx(0, "VentanaAVL", "Gestor de Expedientes con Arbol AVL en C++",
        WS_OVERLAPPEDWINDOW, CW_USEDEFAULT, CW_USEDEFAULT, 900, 650,
        NULL, NULL, hInstance, NULL);

    ShowWindow(hwnd, nCmdShow);
    UpdateWindow(hwnd);

    MSG msg;
    while (GetMessage(&msg, NULL, 0, 0)) {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }

    delete arbolExpedientes; // Liberamos la memoria del árbol al salir
    return (int)msg.wParam;
}

// --- Procedimiento de Ventana ---
LRESULT CALLBACK WndProc(HWND hwnd, UINT msg, WPARAM wParam, LPARAM lParam) {
    switch (msg) {
        case WM_CREATE:
            CrearControles(hwnd);
            break;

        case WM_PAINT: {
            PAINTSTRUCT ps;
            HDC hdc = BeginPaint(hwnd, &ps);
            // Dibujamos el árbol en el área cliente de la ventana
            DibujarArbol(hdc, arbolExpedientes->getRaiz(), 450, 50, 200);
            EndPaint(hwnd, &ps);
            break;
        }

        case WM_COMMAND: {
            // Convertir el buffer de texto a std::string y luego a int
            char bufferId[20], bufferNombre[100];
            GetWindowText(hInputId, bufferId, 20);
            GetWindowText(hInputNombre, bufferNombre, 100);

            if (LOWORD(wParam) == 1) { // Insertar
                try {
                    arbolExpedientes->insertar(stoi(bufferId), string(bufferNombre));
                    SetWindowText(hTextoSalida, "Expediente insertado.");
                    InvalidateRect(hwnd, NULL, TRUE); // Forza el redibujado (WM_PAINT)
                } catch (...) { SetWindowText(hTextoSalida, "Error: Datos inválidos."); }
            }
            if (LOWORD(wParam) == 2) { // Buscar
                try {
                    auto inicio = chrono::high_resolution_clock::now();
                    string resultado = arbolExpedientes->buscar(stoi(bufferId));
                    auto fin = chrono::high_resolution_clock::now();
                    auto duracion = chrono::duration_cast<chrono::nanoseconds>(fin - inicio).count();

                    string texto = "Resultado: " + resultado + ". \nTiempo: " + to_string(duracion) + " ns.";
                    SetWindowText(hTextoSalida, texto.c_str());
                } catch (...) { SetWindowText(hTextoSalida, "Error: ID inválido para buscar."); }
            }
            if (LOWORD(wParam) == 3) { // Insertar Masivo
                SetWindowText(hTextoSalida, "Insertando 100,000 expedientes... por favor espere.");
                random_device rd;
                mt19937 gen(rd());
                uniform_int_distribution<> distrib(1, 1000000);

                for(int i=0; i<100000; ++i){
                    int id = distrib(gen);
                    arbolExpedientes->insertar(id, "Estudiante" + to_string(id));
                }
                SetWindowText(hTextoSalida, "Carga masiva completada.");
                InvalidateRect(hwnd, NULL, TRUE);
            }
            break;
        }

        case WM_CLOSE:
            DestroyWindow(hwnd);
            break;

        case WM_DESTROY:
            PostQuitMessage(0);
            break;

        default:
            return DefWindowProc(hwnd, msg, wParam, lParam);
    }
    return 0;
}

// --- Funciones Auxiliares de la GUI ---
void CrearControles(HWND hwnd) {
    CreateWindow("STATIC", "ID:", WS_VISIBLE | WS_CHILD, 20, 20, 25, 20, hwnd, NULL, NULL, NULL);
    hInputId = CreateWindow("EDIT", "", WS_VISIBLE | WS_CHILD | WS_BORDER, 50, 20, 80, 20, hwnd, NULL, NULL, NULL);

    CreateWindow("STATIC", "Nombre:", WS_VISIBLE | WS_CHILD, 140, 20, 55, 20, hwnd, NULL, NULL, NULL);
    hInputNombre = CreateWindow("EDIT", "", WS_VISIBLE | WS_CHILD | WS_BORDER, 200, 20, 120, 20, hwnd, NULL, NULL, NULL);

    hBotonInsertar = CreateWindow("BUTTON", "Insertar", WS_VISIBLE | WS_CHILD, 330, 20, 80, 25, hwnd, (HMENU)1, NULL, NULL);
    hBotonBuscar = CreateWindow("BUTTON", "Buscar", WS_VISIBLE | WS_CHILD, 420, 20, 80, 25, hwnd, (HMENU)2, NULL, NULL);
    hBotonMasivo = CreateWindow("BUTTON", "Insertar 100k", WS_VISIBLE | WS_CHILD, 510, 20, 120, 25, hwnd, (HMENU)3, NULL, NULL);

    hTextoSalida = CreateWindow("EDIT", "", WS_VISIBLE | WS_CHILD | WS_BORDER | ES_MULTILINE | ES_READONLY,
        20, 520, 840, 80, hwnd, NULL, NULL, NULL);
}

void DibujarArbol(HDC hdc, NodoAVL* nodo, int x, int y, int separacion) {
    if (nodo == nullptr) return;

    // Dibuja el círculo y el texto del nodo
    Ellipse(hdc, x - 15, y - 15, x + 15, y + 15);
    TextOut(hdc, x - 10, y - 8, to_string(nodo->id).c_str(), to_string(nodo->id).length());

    // Dibuja la conexión y llama recursivamente para los hijos
    if (nodo->izquierda != nullptr) {
        int hijoX = x - separacion;
        int hijoY = y + 60;
        MoveToEx(hdc, x, y, NULL);
        LineTo(hdc, hijoX, hijoY);
        DibujarArbol(hdc, nodo->izquierda, hijoX, hijoY, separacion / 2);
    }
    if (nodo->derecha != nullptr) {
        int hijoX = x + separacion;
        int hijoY = y + 60;
        MoveToEx(hdc, x, y, NULL);
        LineTo(hdc, hijoX, hijoY);
        DibujarArbol(hdc, nodo->derecha, hijoX, hijoY, separacion / 2);
    }
}

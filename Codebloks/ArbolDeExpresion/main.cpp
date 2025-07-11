#include <windows.h>
#include <string>
#include <vector>
#include <stack>
#include <sstream>
#include <stdexcept>

//Importante agregar gdi32, para funciones de dibujo

// Usamos el espacio de nombres estándar para mayor comodidad
using namespace std;

// --- ESTRUCTURAS Y CLASES PARA EL ÁRBOL ---

// Estructura que representa un nodo en el árbol de expresión.
struct NodoDelArbol {
    string valor; // Puede ser un número o un operador (+, -, *, /)
    NodoDelArbol* hijoIzquierdo;
    NodoDelArbol* hijoDerecho;

    // Constructor para crear un nodo fácilmente
    NodoDelArbol(const string& val) {
        valor = val;
        hijoIzquierdo = nullptr;
        hijoDerecho = nullptr;
    }
};

// Clase que gestiona el árbol (principalmente para la memoria)
class ArbolDeExpresion {
private:
    NodoDelArbol* raiz;

    // Función recursiva para borrar todos los nodos
    void destruirRecursivamente(NodoDelArbol* nodo) {
        if (nodo) {
            destruirRecursivamente(nodo->hijoIzquierdo);
            destruirRecursivamente(nodo->hijoDerecho);
            delete nodo;
        }
    }

public:
    // Constructor
    ArbolDeExpresion() {
        raiz = nullptr;
    }

    // Destructor (¡CRUCIAL en C++!)
    ~ArbolDeExpresion() {
        destruirRecursivamente(raiz);
    }

    // Método para cambiar la raíz del árbol
    void setRaiz(NodoDelArbol* nuevaRaiz) {
        // Borramos el árbol anterior para evitar fugas de memoria
        destruirRecursivamente(raiz);
        raiz = nuevaRaiz;
    }

    NodoDelArbol* getRaiz() {
        return raiz;
    }
};


// --- FUNCIONES DE LÓGICA DEL ÁRBOL ---

// Prototipos de las funciones que usaremos
bool esNumero(const string& cadena);
int obtenerPrioridad(const string& op);
string convertirInfijaAPostfija(string infija);
NodoDelArbol* construirArbolDesdePostfija(string postfija);
double evaluarArbol(NodoDelArbol* nodo);

// --- VARIABLES GLOBALES PARA LA INTERFAZ GRÁFICA ---
HWND hCampoExpresion, hBotonEvaluar, hAreaSalida;
ArbolDeExpresion* arbol; // Puntero global a nuestro árbol

// --- PROTOTIPOS DE FUNCIONES DE LA GUI ---
LRESULT CALLBACK WndProc(HWND, UINT, WPARAM, LPARAM);
void CrearControles(HWND);
void DibujarNodo(HDC hdc, NodoDelArbol* nodo, int x, int y, int separacion);

// --- PUNTO DE ENTRADA DE LA APLICACIÓN ---
int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow) {
    arbol = new ArbolDeExpresion();

    WNDCLASSEX wc = {0};
    wc.cbSize = sizeof(WNDCLASSEX);
    wc.lpfnWndProc = WndProc;
    wc.hInstance = hInstance;
    wc.hbrBackground = (HBRUSH)(COLOR_WINDOW + 1);
    wc.lpszClassName = "VentanaArbolExpresion";
    RegisterClassEx(&wc);

    HWND hwnd = CreateWindowEx(0, "VentanaArbolExpresion", "Evaluador de Árbol de Expresión en C++",
        WS_OVERLAPPEDWINDOW, CW_USEDEFAULT, CW_USEDEFAULT, 800, 600,
        NULL, NULL, hInstance, NULL);

    ShowWindow(hwnd, nCmdShow);
    UpdateWindow(hwnd);

    MSG msg;
    while (GetMessage(&msg, NULL, 0, 0)) {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }

    delete arbol; // Liberamos la memoria del árbol al salir
    return (int)msg.wParam;
}

// --- LÓGICA DE LA VENTANA ---
LRESULT CALLBACK WndProc(HWND hwnd, UINT msg, WPARAM wParam, LPARAM lParam) {
    switch (msg) {
        case WM_CREATE:
            CrearControles(hwnd);
            break;

        case WM_PAINT: {
            PAINTSTRUCT ps;
            HDC hdc = BeginPaint(hwnd, &ps);
            // El área de dibujo principal es el fondo de la ventana
            if (arbol && arbol->getRaiz()) {
                DibujarNodo(hdc, arbol->getRaiz(), 400, 50, 180);
            }
            EndPaint(hwnd, &ps);
            break;
        }

        case WM_COMMAND:
            if (LOWORD(wParam) == 1) { // Botón "Evaluar"
                char buffer[512];
                GetWindowText(hCampoExpresion, buffer, 512);
                string expresionInfija(buffer);

                try {
                    string postfija = convertirInfijaAPostfija(expresionInfija);
                    NodoDelArbol* nuevaRaiz = construirArbolDesdePostfija(postfija);
                    arbol->setRaiz(nuevaRaiz);

                    double resultado = evaluarArbol(arbol->getRaiz());

                    // Construir el texto de salida
                    stringstream ss;
                    ss << "Resultado: " << resultado << "\r\n";
                    // Aquí podrías añadir los recorridos si lo deseas

                    SetWindowText(hAreaSalida, ss.str().c_str());
                    InvalidateRect(hwnd, NULL, TRUE); // Forza a redibujar el árbol
                } catch (const exception& e) {
                    SetWindowText(hAreaSalida, "Error: Expresión inválida o mal formateada.");
                    arbol->setRaiz(nullptr); // Limpia el árbol si hay error
                    InvalidateRect(hwnd, NULL, TRUE);
                }
            }
            break;

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

// --- IMPLEMENTACIÓN DE FUNCIONES DE LÓGICA ---

bool esNumero(const string& s) {
    try {
        stod(s);
        return true;
    } catch (...) {
        return false;
    }
}

int obtenerPrioridad(const string& op) {
    if (op == "+" || op == "-") return 1;
    if (op == "*" || op == "/") return 2;
    return 0; // Para paréntesis
}

string convertirInfijaAPostfija(string infija) {
    stringstream ss(infija);
    string token;
    vector<string> tokens;
    // Tokenización manual simple
    for (char c : infija) {
        if (string("()+-*/").find(c) != string::npos) {
            tokens.push_back(string(1, c));
        } else if (c != ' ') {
             if (!tokens.empty() && esNumero(tokens.back())) {
                tokens.back() += c;
            } else {
                tokens.push_back(string(1, c));
            }
        }
    }

    stringstream salida;
    stack<string> pila;

    for (const string& tok : tokens) {
        if (esNumero(tok)) {
            salida << tok << " ";
        } else if (tok == "(") {
            pila.push(tok);
        } else if (tok == ")") {
            while (!pila.empty() && pila.top() != "(") {
                salida << pila.top() << " ";
                pila.pop();
            }
            if(!pila.empty()) pila.pop(); // Saca el "("
        } else { // Es operador
            while (!pila.empty() && obtenerPrioridad(pila.top()) >= obtenerPrioridad(tok)) {
                salida << pila.top() << " ";
                pila.pop();
            }
            pila.push(tok);
        }
    }
    while (!pila.empty()) {
        salida << pila.top() << " ";
        pila.pop();
    }
    return salida.str();
}

NodoDelArbol* construirArbolDesdePostfija(string postfija) {
    stringstream ss(postfija);
    string token;
    stack<NodoDelArbol*> pila;

    while (ss >> token) {
        if (esNumero(token)) {
            pila.push(new NodoDelArbol(token));
        } else {
            if (pila.size() < 2) throw runtime_error("Expresión inválida");
            NodoDelArbol* hijoDer = pila.top(); pila.pop();
            NodoDelArbol* hijoIzq = pila.top(); pila.pop();

            NodoDelArbol* operador = new NodoDelArbol(token);
            operador->hijoIzquierdo = hijoIzq;
            operador->hijoDerecho = hijoDer;
            pila.push(operador);
        }
    }
    if (pila.size() != 1) throw runtime_error("Expresión inválida");
    return pila.top();
}

double evaluarArbol(NodoDelArbol* nodo) {
    if (!nodo) return 0;
    if (esNumero(nodo->valor)) return stod(nodo->valor);

    double izq = evaluarArbol(nodo->hijoIzquierdo);
    double der = evaluarArbol(nodo->hijoDerecho);

    if (nodo->valor == "+") return izq + der;
    if (nodo->valor == "-") return izq - der;
    if (nodo->valor == "*") return izq * der;
    if (nodo->valor == "/") return izq / der;
    return 0;
}


// --- IMPLEMENTACIÓN DE FUNCIONES DE LA GUI ---

void CrearControles(HWND hwnd) {
    CreateWindow("STATIC", "Expresión Infija:", WS_VISIBLE | WS_CHILD, 20, 20, 120, 20, hwnd, NULL, NULL, NULL);
    hCampoExpresion = CreateWindow("EDIT", "3 + ( 2 * 5 )", WS_VISIBLE | WS_CHILD | WS_BORDER, 150, 20, 300, 20, hwnd, NULL, NULL, NULL);
    hBotonEvaluar = CreateWindow("BUTTON", "Evaluar", WS_VISIBLE | WS_CHILD, 460, 20, 100, 25, hwnd, (HMENU)1, NULL, NULL);

    hAreaSalida = CreateWindow("EDIT", "", WS_VISIBLE | WS_CHILD | WS_BORDER | ES_MULTILINE | ES_READONLY | WS_VSCROLL,
        20, 480, 740, 60, hwnd, NULL, NULL, NULL);
}

void DibujarNodo(HDC hdc, NodoDelArbol* nodo, int x, int y, int separacion) {
    if (!nodo) return;

    Ellipse(hdc, x - 20, y - 15, x + 20, y + 15);
    TextOut(hdc, x - 5, y - 8, nodo->valor.c_str(), nodo->valor.length());

    if (nodo->hijoIzquierdo) {
        int hijoX = x - separacion;
        int hijoY = y + 60;
        MoveToEx(hdc, x, y, NULL);
        LineTo(hdc, hijoX, hijoY);
        DibujarNodo(hdc, nodo->hijoIzquierdo, hijoX, hijoY, separacion / 2);
    }
    if (nodo->hijoDerecho) {
        int hijoX = x + separacion;
        int hijoY = y + 60;
        MoveToEx(hdc, x, y, NULL);
        LineTo(hdc, hijoX, hijoY);
        DibujarNodo(hdc, nodo->hijoDerecho, hijoX, hijoY, separacion / 2);
    }
}

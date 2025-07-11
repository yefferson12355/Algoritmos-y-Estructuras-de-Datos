#include <windows.h> // Librería principal para la API de Windows
#include <vector>    // Para usar listas dinámicas (como el ArrayList de Java)
#include <string>    // Para manejar texto
#include <sstream>   // Para conversiones entre texto y números
#include <iostream>  // Para la consola (opcional, útil para depurar)

// Usamos el espacio de nombres estándar para no tener que escribir std:: a cada rato
using namespace std;

// === DECLARACIÓN DE CLASES (Para que se conozcan entre ellas) ===
class ArbolB;
class NodoArbolB;

// =================================================================
// 1. CLASE PARA UN NODO DEL ÁRBOL B
// =================================================================
class NodoArbolB {
private:
    int ordenMinimo;        // Orden mínimo (t). Determina la capacidad del nodo.
    bool esHoja;            // Verdadero si el nodo es una hoja (no tiene hijos).
    vector<int> llaves;     // Lista de llaves (los números que guardamos).
    vector<NodoArbolB*> hijos; // Lista de punteros a los nodos hijos.

public:
    // Constructor del nodo
    NodoArbolB(int _ordenMinimo, bool _esHoja) {
        this->ordenMinimo = _ordenMinimo;
        this->esHoja = _esHoja;
    }

    // Destructor para liberar memoria (muy importante en C++)
    ~NodoArbolB() {
        for (NodoArbolB* hijo : hijos) {
            delete hijo; // Llama al destructor de cada hijo recursivamente
        }
    }

    // --- MÉTODOS PRINCIPALES DEL NODO ---

    // Método para buscar una llave en el subárbol de este nodo
    bool buscar(int llaveBuscada) {
        int i = 0;
        // Encontrar la primera llave mayor o igual a la llave buscada
        while (i < llaves.size() && llaveBuscada > llaves[i]) {
            i++;
        }

        // Si encontramos la llave exacta, retornamos verdadero
        if (i < llaves.size() && llaves[i] == llaveBuscada) {
            return true;
        }

        // Si el nodo es una hoja, y no la encontramos, ya no está
        if (esHoja) {
            return false;
        }

        // Si no, descendemos al hijo correspondiente
        return hijos[i]->buscar(llaveBuscada);
    }

    // Método para insertar una llave en un nodo que NO está lleno
    void insertarEnNodoNoLleno(int nuevaLlave) {
        int i = llaves.size() - 1; // Empezamos desde la última llave

        if (esHoja) {
            // Si es una hoja, hacemos espacio y la insertamos en orden
            llaves.push_back(0); // Añadimos un espacio temporal
            while (i >= 0 && llaves[i] > nuevaLlave) {
                llaves[i + 1] = llaves[i]; // Movemos las llaves a la derecha
                i--;
            }
            llaves[i + 1] = nuevaLlave; // Insertamos la nueva llave
        } else {
            // Si no es hoja, encontramos el hijo donde debe ir la nueva llave
            while (i >= 0 && llaves[i] > nuevaLlave) {
                i--;
            }

            // Revisamos si el hijo encontrado está lleno
            if (hijos[i + 1]->llaves.size() == 2 * ordenMinimo - 1) {
                dividirHijo(i + 1, hijos[i + 1]); // Si está lleno, lo dividimos

                // Después de dividir, decidimos a qué hijo ir
                if (llaves[i + 1] < nuevaLlave) {
                    i++;
                }
            }
            hijos[i + 1]->insertarEnNodoNoLleno(nuevaLlave);
        }
    }

    // Método para dividir un hijo 'y' de este nodo. 'y' debe estar lleno.
    void dividirHijo(int indice, NodoArbolB* hijoLleno) {
        // 1. Crear un nuevo nodo que guardará la mitad de las llaves del hijo lleno
        NodoArbolB* nuevoNodo = new NodoArbolB(hijoLleno->ordenMinimo, hijoLleno->esHoja);

        // 2. Mover la mitad de las llaves del hijo lleno al nuevo nodo
        for (int j = 0; j < ordenMinimo - 1; j++) {
            nuevoNodo->llaves.push_back(hijoLleno->llaves[j + ordenMinimo]);
        }

        // 3. Si el hijo no era hoja, mover también la mitad de sus hijos
        if (!hijoLleno->esHoja) {
            for (int j = 0; j < ordenMinimo; j++) {
                nuevoNodo->hijos.push_back(hijoLleno->hijos[j + ordenMinimo]);
            }
        }

        // 4. Reducir el número de llaves en el hijo original
        hijoLleno->llaves.resize(ordenMinimo - 1);
        if(!hijoLleno->esHoja){
             hijoLleno->hijos.resize(ordenMinimo);
        }

        // 5. Insertar el puntero al nuevo nodo en la lista de hijos del nodo actual
        hijos.insert(hijos.begin() + indice + 1, nuevoNodo);

        // 6. Subir la llave del medio del hijo lleno al nodo actual
        llaves.insert(llaves.begin() + indice, hijoLleno->llaves[ordenMinimo - 1]);
    }

    // Para que la clase ArbolB pueda acceder a los miembros privados de NodoArbolB
    friend class ArbolB;
};

// =================================================================
// 2. CLASE PARA EL ÁRBOL B COMPLETO
// =================================================================
class ArbolB {
private:
    NodoArbolB* raiz;     // Puntero a la raíz del árbol
    int ordenMinimo;      // Orden (grado) del árbol

public:
    // Constructor del árbol
    ArbolB(int _ordenMinimo) {
        this->raiz = new NodoArbolB(_ordenMinimo, true);
        this->ordenMinimo = _ordenMinimo;
    }

    // Destructor para liberar toda la memoria del árbol
    ~ArbolB() {
        delete raiz;
    }

    // --- MÉTODOS PRINCIPALES DEL ÁRBOL ---

    // Método público para buscar una llave
    bool buscar(int llaveBuscada) {
        return (raiz == nullptr) ? false : raiz->buscar(llaveBuscada);
    }

    // Método público para insertar una llave
    void insertar(int nuevaLlave) {
        NodoArbolB* r = raiz;

        // Si la raíz está llena, el árbol crece en altura
        if (r->llaves.size() == 2 * ordenMinimo - 1) {
            // Creamos una nueva raíz
            NodoArbolB* nuevaRaiz = new NodoArbolB(ordenMinimo, false);
            nuevaRaiz->hijos.push_back(raiz); // La antigua raíz se convierte en hijo

            // Dividimos la antigua raíz (que ahora es un hijo)
            nuevaRaiz->dividirHijo(0, r);

            // Decidimos cuál de los dos hijos tendrá la nueva llave
            int i = 0;
            if (nuevaRaiz->llaves[0] < nuevaLlave) {
                i++;
            }
            nuevaRaiz->hijos[i]->insertarEnNodoNoLleno(nuevaLlave);

            // La nueva raíz ahora es la raíz del árbol
            raiz = nuevaRaiz;
        } else {
            // Si la raíz no está llena, llamamos a insertar en la raíz
            r->insertarEnNodoNoLleno(nuevaLlave);
        }
    }
};


// =================================================================
// 3. PARTE GRÁFICA (API DE WINDOWS)
// =================================================================

// --- Variables Globales para los Controles de la Ventana ---
HWND hInputId;         // Caja de texto para el ID
HWND hBotonInsertar;   // Botón de Insertar
HWND hBotonBuscar;     // Botón de Buscar
HWND hListaDatos;      // Lista para mostrar los IDs insertados
HWND hTextoSalida;     // Etiqueta para mostrar mensajes de resultado

// Puntero global a nuestro árbol
ArbolB* arbolB;

// --- Prototipos de Funciones ---
LRESULT CALLBACK WndProc(HWND, UINT, WPARAM, LPARAM);
void CrearControles(HWND);

// --- Punto de Entrada de la Aplicación de Windows ---
int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow) {
    // Definimos el orden del árbol. Para un ejemplo simple, lo fijamos en 3.
    // En una app real, se podría pedir al usuario con un cuadro de diálogo.
    const int ORDEN_ARBOL = 3;
    arbolB = new ArbolB(ORDEN_ARBOL);

    // --- Proceso estándar para crear una ventana en Windows ---
    WNDCLASSEX wc = {0};
    wc.cbSize = sizeof(WNDCLASSEX);
    wc.style = 0;
    wc.lpfnWndProc = WndProc; // La función que manejará los eventos
    wc.hInstance = hInstance;
    wc.hbrBackground = (HBRUSH)(COLOR_WINDOW + 1);
    wc.lpszClassName = "VentanaArbolB";
    RegisterClassEx(&wc);

    HWND hwnd = CreateWindowEx(0, "VentanaArbolB", "Simulador de Arbol B en C++",
        WS_OVERLAPPEDWINDOW, CW_USEDEFAULT, CW_USEDEFAULT, 600, 400,
        NULL, NULL, hInstance, NULL);

    ShowWindow(hwnd, nCmdShow);
    UpdateWindow(hwnd);

    // Bucle de mensajes: mantiene la ventana abierta y reactiva
    MSG msg;
    while (GetMessage(&msg, NULL, 0, 0)) {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }

    // Limpieza de memoria al cerrar
    delete arbolB;
    return (int)msg.wParam;
}

// --- Cerebro de la Ventana: Procesa todos los eventos ---
LRESULT CALLBACK WndProc(HWND hwnd, UINT msg, WPARAM wParam, LPARAM lParam) {
    switch (msg) {
        case WM_CREATE:
            // Este mensaje se recibe una sola vez, al crear la ventana.
            // Es el lugar perfecto para crear nuestros botones y cajas de texto.
            CrearControles(hwnd);
            break;

        case WM_COMMAND:
            // Este mensaje se recibe cada vez que se hace clic en un botón.
            // LOWORD(wParam) nos dice QUÉ botón fue presionado.
            if (LOWORD(wParam) == 1) { // Botón Insertar (ID=1)
                char buffer[256];
                GetWindowText(hInputId, buffer, 256); // Obtenemos el texto del input
                try {
                    int id = stoi(string(buffer)); // Convertimos texto a número
                    arbolB->insertar(id);          // Insertamos en el árbol

                    // Añadimos el ID a la lista visual y mostramos mensaje
                    SendMessage(hListaDatos, LB_ADDSTRING, 0, (LPARAM)buffer);
                    SetWindowText(hTextoSalida, "ID insertado con éxito.");
                } catch (...) {
                    SetWindowText(hTextoSalida, "Error: Ingrese un ID numérico válido.");
                }
            }
            if (LOWORD(wParam) == 2) { // Botón Buscar (ID=2)
                char buffer[256];
                GetWindowText(hInputId, buffer, 256);
                try {
                    int id = stoi(string(buffer));
                    bool encontrado = arbolB->buscar(id); // Buscamos en el árbol

                    if (encontrado) {
                        SetWindowText(hTextoSalida, "Resultado: ID encontrado.");
                    } else {
                        SetWindowText(hTextoSalida, "Resultado: ID NO encontrado.");
                    }
                } catch (...) {
                    SetWindowText(hTextoSalida, "Error: Ingrese un ID numérico válido.");
                }
            }
            break;

        case WM_CLOSE:
            // Se recibe cuando el usuario cierra la ventana.
            DestroyWindow(hwnd);
            break;

        case WM_DESTROY:
            // Se recibe después de destruir la ventana.
            // Le decimos a la aplicación que termine.
            PostQuitMessage(0);
            break;

        default:
            // Para cualquier otro mensaje, usamos el manejador por defecto.
            return DefWindowProc(hwnd, msg, wParam, lParam);
    }
    return 0;
}


// --- Función para crear y posicionar los controles en la ventana ---
void CrearControles(HWND hwnd) {
    CreateWindow("STATIC", "ID:", WS_VISIBLE | WS_CHILD, 20, 20, 25, 20, hwnd, NULL, NULL, NULL);
    hInputId = CreateWindow("EDIT", "", WS_VISIBLE | WS_CHILD | WS_BORDER, 50, 20, 100, 20, hwnd, NULL, NULL, NULL);

    hBotonInsertar = CreateWindow("BUTTON", "Insertar", WS_VISIBLE | WS_CHILD, 160, 20, 80, 25, hwnd, (HMENU)1, NULL, NULL);
    hBotonBuscar = CreateWindow("BUTTON", "Buscar", WS_VISIBLE | WS_CHILD, 250, 20, 80, 25, hwnd, (HMENU)2, NULL, NULL);

    CreateWindow("STATIC", "Datos Insertados:", WS_VISIBLE | WS_CHILD, 20, 60, 120, 20, hwnd, NULL, NULL, NULL);
    hListaDatos = CreateWindow("LISTBOX", NULL, WS_VISIBLE | WS_CHILD | WS_BORDER | LBS_NOTIFY, 20, 80, 540, 200, hwnd, NULL, NULL, NULL);

    hTextoSalida = CreateWindow("STATIC", "Bienvenido. Ingrese un ID para comenzar.", WS_VISIBLE | WS_CHILD, 20, 300, 540, 20, hwnd, NULL, NULL, NULL);
}

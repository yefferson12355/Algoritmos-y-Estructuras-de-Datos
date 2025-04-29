// Inclusión de bibliotecas necesarias
#include <windows.h>     // Biblioteca principal de WinAPI
#include <fstream>       // Para archivos (guardar y cargar)
#include <sstream>       // Para leer datos con separadores
#include <string>        // Para trabajar con strings C++
#include <vector>        // Para almacenar lista de estudiantes

using namespace std;     // Uso del espacio de nombres estándar

// Estructura para representar un estudiante
struct Estudiante {
    string nombre;
    string correo;
    string carrera;
    int anio;
};

// Lista global de estudiantes
vector<Estudiante> lista;

// Controles de interfaz globales
HWND hNombre, hCorreo, hCarrera, hAnio, hLista;

// Función para agregar un nuevo estudiante
void AgregarEstudiante(HWND hwnd) {
    char nombre[100], correo[100], carrera[100], anioStr[10];

    // Obtener texto ingresado por el usuario desde los controles
    GetWindowText(hNombre, nombre, 100);
    GetWindowText(hCorreo, correo, 100);
    GetWindowText(hCarrera, carrera, 100);
    GetWindowText(hAnio, anioStr, 10);

    // Convertir año de string a entero
    int anio = atoi(anioStr);

    // Crear estructura y agregar a la lista
    Estudiante e = { nombre, correo, carrera, anio };
    lista.push_back(e);

    // Agregar al ListBox (visualización)
    string textoLista = string(nombre) + " - " + correo;
    SendMessage(hLista, LB_ADDSTRING, 0, (LPARAM)textoLista.c_str());

    // Limpiar los campos
    SetWindowText(hNombre, "");
    SetWindowText(hCorreo, "");
    SetWindowText(hCarrera, "");
    SetWindowText(hAnio, "");
}

// Función para guardar la lista en un archivo de texto
void GuardarArchivo() {
    ofstream file("registros.txt");  // Crear archivo
    for (auto& e : lista) {
        // Escribir datos separados por punto y coma
        file << e.nombre << ";" << e.correo << ";" << e.carrera << ";" << e.anio << "\n";
    }
    file.close(); // Cerrar archivo
}

// Función para cargar registros desde archivo
void CargarArchivo(HWND hwnd) {
    lista.clear();  // Limpiar lista en memoria
    SendMessage(hLista, LB_RESETCONTENT, 0, 0);  // Limpiar lista en pantalla

    ifstream file("registros.txt");  // Abrir archivo
    string linea;
    while (getline(file, linea)) {
        stringstream ss(linea);
        string nombre, correo, carrera, anioStr;

        // Extraer campos por separado
        getline(ss, nombre, ';');
        getline(ss, correo, ';');
        getline(ss, carrera, ';');
        getline(ss, anioStr, ';');

        int anio = stoi(anioStr);  // Convertir año a entero

        // Crear estructura y agregar a lista
        Estudiante e = { nombre, correo, carrera, anio };
        lista.push_back(e);

        // Mostrar en el ListBox
        string textoLista = nombre + " - " + correo;
        SendMessage(hLista, LB_ADDSTRING, 0, (LPARAM)textoLista.c_str());
    }
    file.close(); // Cerrar archivo
}

// Procesamiento de mensajes (ventana principal)
LRESULT CALLBACK WindowProcedure(HWND hwnd, UINT msg, WPARAM wp, LPARAM lp) {
    switch (msg) {
    case WM_COMMAND:  // Evento de botones
        switch (wp) {
        case 1: AgregarEstudiante(hwnd); break;   // Botón Agregar
        case 2: GuardarArchivo(); break;          // Botón Guardar
        case 3: CargarArchivo(hwnd); break;       // Botón Cargar
        }
        break;
    case WM_DESTROY:  // Al cerrar ventana
        PostQuitMessage(0); break;
    default:
        return DefWindowProc(hwnd, msg, wp, lp);  // Procesamiento por defecto
    }
    return 0;
}

// Función para crear los controles visuales en la ventana
void CrearControles(HWND hwnd) {
    // Etiquetas y cajas de texto
    CreateWindow("STATIC", "Nombre:", WS_VISIBLE | WS_CHILD, 20, 20, 80, 20, hwnd, NULL, NULL, NULL);
    hNombre = CreateWindow("EDIT", "", WS_VISIBLE | WS_CHILD | WS_BORDER, 100, 20, 200, 20, hwnd, NULL, NULL, NULL);

    CreateWindow("STATIC", "Correo:", WS_VISIBLE | WS_CHILD, 20, 50, 80, 20, hwnd, NULL, NULL, NULL);
    hCorreo = CreateWindow("EDIT", "", WS_VISIBLE | WS_CHILD | WS_BORDER, 100, 50, 200, 20, hwnd, NULL, NULL, NULL);

    CreateWindow("STATIC", "Carrera:", WS_VISIBLE | WS_CHILD, 20, 80, 80, 20, hwnd, NULL, NULL, NULL);
    hCarrera = CreateWindow("EDIT", "", WS_VISIBLE | WS_CHILD | WS_BORDER, 100, 80, 200, 20, hwnd, NULL, NULL, NULL);

    CreateWindow("STATIC", "Año:", WS_VISIBLE | WS_CHILD, 20, 110, 80, 20, hwnd, NULL, NULL, NULL);
    hAnio = CreateWindow("EDIT", "", WS_VISIBLE | WS_CHILD | WS_BORDER, 100, 110, 100, 20, hwnd, NULL, NULL, NULL);

    // Botones
    CreateWindow("BUTTON", "Agregar", WS_VISIBLE | WS_CHILD, 320, 20, 100, 30, hwnd, (HMENU)1, NULL, NULL);
    CreateWindow("BUTTON", "Guardar", WS_VISIBLE | WS_CHILD, 320, 60, 100, 30, hwnd, (HMENU)2, NULL, NULL);
    CreateWindow("BUTTON", "Cargar", WS_VISIBLE | WS_CHILD, 320, 100, 100, 30, hwnd, (HMENU)3, NULL, NULL);

    // Lista donde se muestra a los estudiantes
    hLista = CreateWindow("LISTBOX", NULL, WS_VISIBLE | WS_CHILD | WS_BORDER | LBS_NOTIFY,
        20, 150, 400, 200, hwnd, NULL, NULL, NULL);
}

// Función principal del programa WinAPI
int WINAPI WinMain(HINSTANCE hInst, HINSTANCE hPrev, LPSTR args, int nCmdShow) {
    // Definición de la clase de ventana
    WNDCLASS wc = { 0 };
    wc.hbrBackground = (HBRUSH)COLOR_WINDOW;         // Color de fondo blanco
    wc.hCursor = LoadCursor(NULL, IDC_ARROW);        // Cursor por defecto
    wc.hInstance = hInst;                            // Instancia del programa
    wc.lpszClassName = "RegistroWin";                // Nombre único de clase
    wc.lpfnWndProc = WindowProcedure;                // Función que maneja eventos

    // Registro de la clase de ventana
    if (!RegisterClass(&wc)) return -1;

    // Crear la ventana principal
    HWND hwnd = CreateWindow("RegistroWin", "Sistema de Registro Académico",
        WS_OVERLAPPEDWINDOW | WS_VISIBLE, 100, 100, 470, 420,
        NULL, NULL, NULL, NULL);

    // Crear los controles dentro de la ventana
    CrearControles(hwnd);

    // Loop principal de mensajes (ventana activa)
    MSG msg = { 0 };
    while (GetMessage(&msg, NULL, 0, 0)) {
        TranslateMessage(&msg);    // Traducir entrada (teclado)    
        DispatchMessage(&msg);     // Enviar mensaje a WindowProcedure
    }

    return 0; // Fin del programa
}

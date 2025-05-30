// Sistema de Historial de Comandos - Aplicación de Diseño (Versión Compacta)
#include <windows.h>
#include <string>
#include <stack>
#include <vector>
#include <sstream>
using namespace std;

// Estructuras principales
enum TipoComando { DIBUJAR = 1, MOVER = 2, ELIMINAR = 3 };

struct ObjetoDiseno {
    int id; string tipo; int x, y; string color; bool activo;
};

struct Comando {
    TipoComando tipo; int objetoId; string descripcion;
    int posX_ant, posY_ant; ObjetoDiseno obj_completo;
};
// Variables globales
vector<ObjetoDiseno> objetos;
stack<Comando> pilaDeshacer, pilaRehacer;
int siguienteId = 1;
const int MAX_HISTORIAL = 10;
HWND hTipo, hX, hY, hColor, hId, hHistorial, hEstado;

// Limitar historial a 10 comandos
void LimitarHistorial() {
    if (pilaDeshacer.size() > MAX_HISTORIAL) {
        stack<Comando> temp;
        for (int i = 0; i < MAX_HISTORIAL && !pilaDeshacer.empty(); i++) {
            temp.push(pilaDeshacer.top()); pilaDeshacer.pop();
        }
        while (!pilaDeshacer.empty()) pilaDeshacer.pop();
        while (!temp.empty()) { pilaDeshacer.push(temp.top()); temp.pop(); }
    }
}

// Actualizar visualización del historial
void ActualizarHistorial() {
    SendMessage(hHistorial, LB_RESETCONTENT, 0, 0);
    stack<Comando> temp = pilaDeshacer;
    vector<string> cmds;
    while (!temp.empty()) { cmds.push_back(temp.top().descripcion); temp.pop(); }
    
    for (int i = cmds.size() - 1; i >= 0; i--) {
        SendMessage(hHistorial, LB_ADDSTRING, 0, (LPARAM)("↶ " + cmds[i]).c_str());
    }
    
    stringstream estado;
    estado << "Objetos: " << objetos.size() << " | Deshacer: " << pilaDeshacer.size() 
           << " | Rehacer: " << pilaRehacer.size();
    SetWindowText(hEstado, estado.str().c_str());
}

// Función para dibujar objeto
void DibujarObjeto(HWND hwnd) {
    char tipo[50], x[10], y[10], color[50];
    GetWindowText(hTipo, tipo, 50); GetWindowText(hX, x, 10);
    GetWindowText(hY, y, 10); GetWindowText(hColor, color, 50);
    
    if (!strlen(tipo) || !strlen(x) || !strlen(y)) {
        MessageBox(hwnd, "Complete todos los campos", "Error", MB_OK); return;
    }
    
    ObjetoDiseno obj = {siguienteId++, string(tipo), atoi(x), atoi(y), string(color), true};
    objetos.push_back(obj);
    
    Comando cmd = {DIBUJAR, obj.id, "Dibujar " + obj.tipo + " en (" + to_string(obj.x) + "," + to_string(obj.y) + ")", 0, 0, obj};
    pilaDeshacer.push(cmd); LimitarHistorial();
    while (!pilaRehacer.empty()) pilaRehacer.pop();
    
    SetWindowText(hTipo, ""); SetWindowText(hX, ""); SetWindowText(hY, ""); SetWindowText(hColor, "");
    ActualizarHistorial();
    MessageBox(hwnd, ("Objeto " + to_string(obj.id) + " creado").c_str(), "Éxito", MB_OK);
}

// Función para mover objeto
void MoverObjeto(HWND hwnd) {
    char id[10], x[10], y[10];
    GetWindowText(hId, id, 10); GetWindowText(hX, x, 10); GetWindowText(hY, y, 10);
    
    if (!strlen(id) || !strlen(x) || !strlen(y)) {
        MessageBox(hwnd, "Complete ID y nueva posición", "Error", MB_OK); return;
    }
    
    int objId = atoi(id), newX = atoi(x), newY = atoi(y);
    for (auto& obj : objetos) {
        if (obj.id == objId && obj.activo) {
            Comando cmd = {MOVER, objId, "Mover ID:" + to_string(objId) + " a (" + to_string(newX) + "," + to_string(newY) + ")", obj.x, obj.y};
            obj.x = newX; obj.y = newY;
            pilaDeshacer.push(cmd); LimitarHistorial();
            while (!pilaRehacer.empty()) pilaRehacer.pop();
            
            SetWindowText(hId, ""); SetWindowText(hX, ""); SetWindowText(hY, "");
            ActualizarHistorial();
            MessageBox(hwnd, "Objeto movido", "Éxito", MB_OK);
            return;
        }
    }
    MessageBox(hwnd, "Objeto no encontrado", "Error", MB_OK);
}

// Función para eliminar objeto
void EliminarObjeto(HWND hwnd) {
    char id[10];
    GetWindowText(hId, id, 10);
    if (!strlen(id)) { MessageBox(hwnd, "Ingrese ID", "Error", MB_OK); return; }
    
    int objId = atoi(id);
    for (auto& obj : objetos) {
        if (obj.id == objId && obj.activo) {
            Comando cmd = {ELIMINAR, objId, "Eliminar ID:" + to_string(objId), 0, 0, obj};
            obj.activo = false;
            pilaDeshacer.push(cmd); LimitarHistorial();
            while (!pilaRehacer.empty()) pilaRehacer.pop();
            
            SetWindowText(hId, "");
            ActualizarHistorial();
            MessageBox(hwnd, "Objeto eliminado", "Éxito", MB_OK);
            return;
        }
    }
    MessageBox(hwnd, "Objeto no encontrado", "Error", MB_OK);
}

// Función deshacer
void DeshacerAccion(HWND hwnd) {
    if (pilaDeshacer.empty()) { MessageBox(hwnd, "Nada que deshacer", "Info", MB_OK); return; }
    
    Comando cmd = pilaDeshacer.top(); pilaDeshacer.pop();
    
    if (cmd.tipo == DIBUJAR) {
        for (auto it = objetos.begin(); it != objetos.end(); ++it) {
            if (it->id == cmd.objetoId) { objetos.erase(it); break; }
        }
    } else if (cmd.tipo == MOVER) {
        for (auto& obj : objetos) {
            if (obj.id == cmd.objetoId) { obj.x = cmd.posX_ant; obj.y = cmd.posY_ant; break; }
        }
    } else if (cmd.tipo == ELIMINAR) {
        for (auto& obj : objetos) {
            if (obj.id == cmd.objetoId) { obj.activo = true; break; }
        }
    }
    
    pilaRehacer.push(cmd);
    ActualizarHistorial();
    MessageBox(hwnd, ("Deshecho: " + cmd.descripcion).c_str(), "Deshacer", MB_OK);
}

// Función rehacer
void RehacerAccion(HWND hwnd) {
    if (pilaRehacer.empty()) { MessageBox(hwnd, "Nada que rehacer", "Info", MB_OK); return; }
    
    Comando cmd = pilaRehacer.top(); pilaRehacer.pop();
    
    if (cmd.tipo == DIBUJAR) {
        objetos.push_back(cmd.obj_completo);
    } else if (cmd.tipo == ELIMINAR) {
        for (auto& obj : objetos) {
            if (obj.id == cmd.objetoId) { obj.activo = false; break; }
        }
    }
    
    pilaDeshacer.push(cmd);
    ActualizarHistorial();
    MessageBox(hwnd, ("Rehecho: " + cmd.descripcion).c_str(), "Rehacer", MB_OK);
}

// Mostrar objetos actuales
void MostrarObjetos(HWND hwnd) {
    stringstream lista; lista << "=== OBJETOS ACTUALES ===\n\n";
    int activos = 0;
    for (const auto& obj : objetos) {
        if (obj.activo) {
            lista << "ID:" << obj.id << " | " << obj.tipo << " | (" << obj.x << "," << obj.y << ") | " << obj.color << "\n";
            activos++;
        }
    }
    if (activos == 0) lista << "Sin objetos\n";
    lista << "\nTotal: " << activos;
    MessageBox(hwnd, lista.str().c_str(), "Objetos", MB_OK);
}

// Procesador de mensajes
LRESULT CALLBACK WindowProcedure(HWND hwnd, UINT msg, WPARAM wp, LPARAM lp) {
    switch (msg) {
    case WM_COMMAND:
        switch (wp) {
        case 1: DibujarObjeto(hwnd); break;   case 2: MoverObjeto(hwnd); break;
        case 3: EliminarObjeto(hwnd); break;  case 4: DeshacerAccion(hwnd); break;
        case 5: RehacerAccion(hwnd); break;   case 6: MostrarObjetos(hwnd); break;
        } break;
    case WM_DESTROY: PostQuitMessage(0); break;
    default: return DefWindowProc(hwnd, msg, wp, lp);
    } return 0;
}

// Crear controles de interfaz
void CrearControles(HWND hwnd) {
    CreateWindow("STATIC", "DIBUJAR OBJETO", WS_VISIBLE | WS_CHILD, 20, 20, 120, 15, hwnd, NULL, NULL, NULL);
    CreateWindow("STATIC", "Tipo:", WS_VISIBLE | WS_CHILD, 20, 40, 40, 15, hwnd, NULL, NULL, NULL);
    hTipo = CreateWindow("EDIT", "", WS_VISIBLE | WS_CHILD | WS_BORDER, 65, 40, 80, 20, hwnd, NULL, NULL, NULL);
    CreateWindow("STATIC", "X:", WS_VISIBLE | WS_CHILD, 160, 40, 15, 15, hwnd, NULL, NULL, NULL);
    hX = CreateWindow("EDIT", "", WS_VISIBLE | WS_CHILD | WS_BORDER, 180, 40, 40, 20, hwnd, NULL, NULL, NULL);
    CreateWindow("STATIC", "Y:", WS_VISIBLE | WS_CHILD, 230, 40, 15, 15, hwnd, NULL, NULL, NULL);
    hY = CreateWindow("EDIT", "", WS_VISIBLE | WS_CHILD | WS_BORDER, 250, 40, 40, 20, hwnd, NULL, NULL, NULL);
    CreateWindow("STATIC", "Color:", WS_VISIBLE | WS_CHILD, 20, 65, 40, 15, hwnd, NULL, NULL, NULL);
    hColor = CreateWindow("EDIT", "", WS_VISIBLE | WS_CHILD | WS_BORDER, 65, 65, 80, 20, hwnd, NULL, NULL, NULL);
    
    CreateWindow("STATIC", "MOVER/ELIMINAR", WS_VISIBLE | WS_CHILD, 20, 95, 120, 15, hwnd, NULL, NULL, NULL);
    CreateWindow("STATIC", "ID:", WS_VISIBLE | WS_CHILD, 20, 115, 25, 15, hwnd, NULL, NULL, NULL);
    hId = CreateWindow("EDIT", "", WS_VISIBLE | WS_CHILD | WS_BORDER, 50, 115, 40, 20, hwnd, NULL, NULL, NULL);
    
    CreateWindow("BUTTON", "Dibujar", WS_VISIBLE | WS_CHILD, 320, 20, 70, 25, hwnd, (HMENU)1, NULL, NULL);
    CreateWindow("BUTTON", "Mover", WS_VISIBLE | WS_CHILD, 320, 50, 70, 25, hwnd, (HMENU)2, NULL, NULL);
    CreateWindow("BUTTON", "Eliminar", WS_VISIBLE | WS_CHILD, 320, 80, 70, 25, hwnd, (HMENU)3, NULL, NULL);
    CreateWindow("BUTTON", "Deshacer", WS_VISIBLE | WS_CHILD, 400, 20, 70, 25, hwnd, (HMENU)4, NULL, NULL);
    CreateWindow("BUTTON", "Rehacer", WS_VISIBLE | WS_CHILD, 400, 50, 70, 25, hwnd, (HMENU)5, NULL, NULL);
    CreateWindow("BUTTON", "Ver Todo", WS_VISIBLE | WS_CHILD, 400, 80, 70, 25, hwnd, (HMENU)6, NULL, NULL);
    
    CreateWindow("STATIC", "HISTORIAL (Max 10)", WS_VISIBLE | WS_CHILD, 20, 145, 120, 15, hwnd, NULL, NULL, NULL);
    hHistorial = CreateWindow("LISTBOX", NULL, WS_VISIBLE | WS_CHILD | WS_BORDER, 20, 165, 450, 100, hwnd, NULL, NULL, NULL);
    
    hEstado = CreateWindow("STATIC", "Objetos: 0 | Deshacer: 0 | Rehacer: 0", WS_VISIBLE | WS_CHILD, 20, 275, 450, 15, hwnd, NULL, NULL, NULL);
    ActualizarHistorial();
}

// Función principal
int WINAPI WinMain(HINSTANCE hInst, HINSTANCE hPrev, LPSTR args, int nCmdShow) {
    WNDCLASS wc = {0};
    wc.hbrBackground = (HBRUSH)COLOR_WINDOW; wc.hCursor = LoadCursor(NULL, IDC_ARROW);
    wc.hInstance = hInst; wc.lpszClassName = "HistorialComandos"; wc.lpfnWndProc = WindowProcedure;
    
    if (!RegisterClass(&wc)) return -1;
    
    HWND hwnd = CreateWindow("HistorialComandos", "Sistema Historial de Comandos - Diseño Gráfico",
        WS_OVERLAPPEDWINDOW | WS_VISIBLE, 100, 100, 520, 350, NULL, NULL, NULL, NULL);
    
    CrearControles(hwnd);
    
    MSG msg = {0};
    while (GetMessage(&msg, NULL, 0, 0)) {
        TranslateMessage(&msg); DispatchMessage(&msg);
    }
    return 0;
}

/*
RESUMEN TÉCNICO:
✓ Pilas (stacks) para deshacer/rehacer - estructura LIFO ideal
✓ Límite de 10 comandos para optimizar memoria
✓ Visualización gráfica del historial en tiempo real
✓ 3 operaciones: Dibujar, Mover, Eliminar con reversión completa
✓ Interfaz compacta pero funcional con todos los controles necesarios
*/
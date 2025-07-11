# Importa las librerías necesarias: pygame para la interfaz gráfica, sys para salir del programa,
# math para cálculos (si fueran necesarios) y time para controlar la velocidad de la animación.
import pygame
import sys
import math
import time

# =========================================================================================
# --- SECCIÓN 1: CONFIGURACIÓN GLOBAL Y CONSTANTES VISUALES ---
# Define constantes para colores, tamaños y fuentes. Facilita cambiar la apariencia
# del programa sin tener que modificar el código de la lógica.
# =========================================================================================
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 800
BG_COLOR = (245, 245, 245)
NODE_COLOR = (70, 130, 180)
NODE_HIGHLIGHT_COLOR = (255, 165, 0) # Naranja para nodos en proceso
NODE_FOUND_COLOR = (50, 205, 50)     # Verde para nodos encontrados o en impresión
LINE_COLOR = (0, 0, 0)
TEXT_COLOR = (255, 255, 255)
STATUS_TEXT_COLOR = (0, 0, 0)
UI_BG_COLOR = (220, 220, 220)
BUTTON_COLOR = (100, 100, 100)
BUTTON_TEXT_COLOR = (255, 255, 255)
NODE_RADIUS = 28
FONT_SIZE = 16
HEIGHT_FONT_SIZE = 12


# =========================================================================================
# --- SECCIÓN 2: ESTRUCTURA DE DATOS - El Cerebro 🧠 ---
# Aquí se define la lógica pura del árbol AVL. Estas clases no saben nada
# sobre dibujar en una pantalla; su único trabajo es manejar los datos.
# =========================================================================================

class Nodo:
    """Define la estructura de cada nodo del árbol."""
    def __init__(self, valor, x=0, y=0):
        self.valor = valor          # El número que almacena el nodo
        self.izquierda = None       # El subárbol izquierdo
        self.derecha = None         # El subárbol derecho
        self.altura = 1             # La altura del nodo (para el balanceo)
        self.x = x                  # Coordenada X para dibujarlo en pantalla
        self.y = y                  # Coordenada Y para dibujarlo en pantalla

class ArbolAVL:
    """
    Implementa el árbol AVL. Contiene toda la lógica para insertar, eliminar,
    buscar y balancear. Lo más importante: GENERA la lista de pasos de animación.
    """
    def __init__(self):
        # Un árbol nuevo empieza vacío (sin raíz) y sin animaciones pendientes.
        self.raiz = None
        self.pasos_animacion = []

    # --- Funciones auxiliares para el balanceo ---
    def _get_altura(self, nodo):
        """Devuelve la altura de un nodo. Si el nodo no existe, su altura es 0."""
        return nodo.altura if nodo else 0

    def _get_balance(self, nodo):
        """Calcula el factor de equilibrio de un nodo (altura izq - altura der)."""
        return self._get_altura(nodo.izquierda) - self._get_altura(nodo.derecha) if nodo else 0
    
    def _get_min_valor_nodo(self, nodo):
        """Encuentra el nodo con el valor más pequeño en un subárbol (siempre el de más a la izquierda)."""
        return self._get_min_valor_nodo(nodo.izquierda) if nodo.izquierda else nodo

    def _recalcular_altura(self, nodo):
        """Actualiza la altura de un nodo basándose en la altura de sus hijos."""
        return 1 + max(self._get_altura(nodo.izquierda), self._get_altura(nodo.derecha))

    # --- Rotaciones: El corazón del auto-balanceo ---
    def _rotar_derecha(self, z):
        """Realiza una rotación simple a la derecha."""
        # Añade pasos a la animación para que el usuario vea qué está pasando.
        self.pasos_animacion.append({'tipo': 'texto', 'msg': f"Desbalance en {z.valor}. Rotando a la derecha..."})
        self.pasos_animacion.append({'tipo': 'highlight', 'nodos': [z, z.izquierda], 'color': NODE_HIGHLIGHT_COLOR})
        
        # Lógica de punteros para la rotación.
        y = z.izquierda
        T3 = y.derecha
        y.derecha = z
        z.izquierda = T3
        
        # Actualiza las alturas de los nodos movidos.
        z.altura = self._recalcular_altura(z)
        y.altura = self._recalcular_altura(y)
        
        # Le dice al visualizador que las posiciones han cambiado y debe redibujar.
        self.pasos_animacion.append({'tipo': 'recalcular_posiciones'})
        return y # Devuelve la nueva raíz del subárbol.

    def _rotar_izquierda(self, z):
        """Realiza una rotación simple a la izquierda."""
        self.pasos_animacion.append({'tipo': 'texto', 'msg': f"Desbalance en {z.valor}. Rotando a la izquierda..."})
        self.pasos_animacion.append({'tipo': 'highlight', 'nodos': [z, z.derecha], 'color': NODE_HIGHLIGHT_COLOR})
        y = z.derecha
        T2 = y.izquierda
        y.izquierda = z
        z.derecha = T2
        z.altura = self._recalcular_altura(z)
        y.altura = self._recalcular_altura(y)
        self.pasos_animacion.append({'tipo': 'recalcular_posiciones'})
        return y

    def _balancear(self, nodo):
        """Verifica si un nodo está desbalanceado y aplica las rotaciones necesarias."""
        balance = self._get_balance(nodo)
        # Caso Izquierda (simple o doble)
        if balance > 1:
            if self._get_balance(nodo.izquierda) < 0: # Caso Izquierda-Derecha
                nodo.izquierda = self._rotar_izquierda(nodo.izquierda)
            return self._rotar_derecha(nodo) # Caso Izquierda-Izquierda
        # Caso Derecha (simple o doble)
        if balance < -1:
            if self._get_balance(nodo.derecha) > 0: # Caso Derecha-Izquierda
                nodo.derecha = self._rotar_derecha(nodo.derecha)
            return self._rotar_izquierda(nodo) # Caso Derecha-Derecha
        return nodo # Si no hay desbalance, devuelve el nodo sin cambios.

    # --- Métodos Públicos: Generadores de "Libretos" de Animación ---
    def insertar(self, valor):
        """Método principal para insertar. Devuelve un libreto de animación."""
        self.pasos_animacion = [] # Limpia el libreto anterior.
        self.raiz = self._insertar_rec(self.raiz, valor) # Llama a la función recursiva que hace el trabajo.
        self.pasos_animacion.append({'tipo': 'recalcular_posiciones'}) # Paso final para ordenar el árbol visualmente.
        self.pasos_animacion.append({'tipo': 'texto', 'msg': f"Inserción de {valor} completada."})
        return self.pasos_animacion # Devuelve el libreto completo.

    def _insertar_rec(self, raiz, valor):
        """Función recursiva que inserta y va grabando los pasos."""
        if not raiz: # Caso base: encontramos un lugar vacío para insertar.
            self.pasos_animacion.append({'tipo': 'texto', 'msg': f"Insertando nuevo nodo: {valor}"})
            return Nodo(valor)
        
        # Graba los pasos de búsqueda.
        self.pasos_animacion.append({'tipo': 'highlight', 'nodos': [raiz], 'color': NODE_HIGHLIGHT_COLOR})
        if valor < raiz.valor:
            self.pasos_animacion.append({'tipo': 'texto', 'msg': f"{valor} < {raiz.valor}. Yendo a la izquierda."})
            raiz.izquierda = self._insertar_rec(raiz.izquierda, valor)
        elif valor > raiz.valor:
            self.pasos_animacion.append({'tipo': 'texto', 'msg': f"{valor} > {raiz.valor}. Yendo a la derecha."})
            raiz.derecha = self._insertar_rec(raiz.derecha, valor)
        else: return raiz # Ignora valores duplicados.

        # Al regresar de la recursión, actualiza alturas y balancea.
        raiz.altura = self._recalcular_altura(raiz)
        return self._balancear(raiz)

    def eliminar(self, valor):
        """Método principal para eliminar. Devuelve un libreto de animación."""
        self.pasos_animacion = []
        self.raiz = self._eliminar_rec(self.raiz, valor)
        self.pasos_animacion.append({'tipo': 'recalcular_posiciones'})
        self.pasos_animacion.append({'tipo': 'texto', 'msg': f"Eliminación de {valor} completada."})
        return self.pasos_animacion

    def _eliminar_rec(self, raiz, valor):
        """Función recursiva para eliminar."""
        if not raiz:
            self.pasos_animacion.append({'tipo': 'texto', 'msg': f"Valor {valor} no encontrado."})
            return raiz
        
        self.pasos_animacion.append({'tipo': 'highlight', 'nodos': [raiz], 'color': NODE_HIGHLIGHT_COLOR})
        if valor < raiz.valor:
            raiz.izquierda = self._eliminar_rec(raiz.izquierda, valor)
        elif valor > raiz.valor:
            raiz.derecha = self._eliminar_rec(raiz.derecha, valor)
        else: # Nodo a eliminar encontrado.
            self.pasos_animacion.append({'tipo': 'texto', 'msg': f"Nodo {valor} encontrado. Eliminando..."})
            if raiz.izquierda is None: return raiz.derecha # Caso con 0 o 1 hijo derecho.
            if raiz.derecha is None: return raiz.izquierda # Caso con 1 hijo izquierdo.
            
            # Caso con 2 hijos: buscar el sucesor (el más pequeño del subárbol derecho).
            temp = self._get_min_valor_nodo(raiz.derecha)
            self.pasos_animacion.append({'tipo': 'texto', 'msg': f"Reemplazando con sucesor: {temp.valor}"})
            raiz.valor = temp.valor
            raiz.derecha = self._eliminar_rec(raiz.derecha, temp.valor)

        raiz.altura = self._recalcular_altura(raiz)
        return self._balancear(raiz)
    
    def buscar(self, valor):
        """Busca un valor y genera la animación del camino recorrido."""
        self.pasos_animacion = []
        nodo = self.raiz
        path = []
        while nodo:
            path.append(nodo)
            self.pasos_animacion.append({'tipo': 'highlight_path', 'nodos': list(path)})
            if valor < nodo.valor:
                nodo = nodo.izquierda
            elif valor > nodo.valor:
                nodo = nodo.derecha
            else:
                self.pasos_animacion.append({'tipo': 'texto', 'msg': f"¡Nodo {valor} encontrado!"})
                self.pasos_animacion.append({'tipo': 'highlight', 'nodos': [nodo], 'color': NODE_FOUND_COLOR})
                return self.pasos_animacion
        
        self.pasos_animacion.append({'tipo': 'texto', 'msg': f"Nodo {valor} no encontrado."})
        return self.pasos_animacion

    def imprimir_animado(self):
        """Genera el libreto para la animación de impresión en orden."""
        self.pasos_animacion = []
        self._imprimir_animado_rec(self.raiz)
        self.pasos_animacion.append({'tipo': 'texto', 'msg': "Impresión en orden completada."})
        return self.pasos_animacion

    def _imprimir_animado_rec(self, nodo):
        """Recorrido in-order (izq, raíz, der) que graba los pasos de la animación."""
        if nodo:
            self._imprimir_animado_rec(nodo.izquierda)
            self.pasos_animacion.append({'tipo': 'highlight', 'nodos': [nodo], 'color': NODE_FOUND_COLOR})
            self.pasos_animacion.append({'tipo': 'add_to_print', 'valor': nodo.valor})
            self._imprimir_animado_rec(nodo.derecha)


# =========================================================================================
# --- SECCIÓN 3: INTERFAZ GRÁFICA - El Cuerpo y los Ojos 👀 ---
# Esta clase usa Pygame para crear la ventana, dibujar el árbol y manejar
# la interacción del usuario. Sigue las instrucciones que le da ArbolAVL.
# =========================================================================================
class VisualizadorPygame:
    def __init__(self, arbol):
        """Prepara todo el escenario: la ventana, las fuentes, los botones y las variables de estado."""
        pygame.init()
        self.arbol = arbol # Guarda una referencia al "cerebro".
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Visualizador de Árbol AVL Interactivo")
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.status_font = pygame.font.Font(None, 28)
        self.height_font = pygame.font.Font(None, HEIGHT_FONT_SIZE)
        self.clock = pygame.time.Clock() # Controla la velocidad de fotogramas.
        
        # Variables de estado que controlan la aplicación.
        self.input_text = '' # Texto que el usuario escribe en la caja.
        self.status_text = 'Ingresa un número y elige una acción' # Mensajes de estado.
        self.print_output_text = '' # Texto para el resultado de la impresión.
        self.animating = False # True si una animación está en curso.
        self.paused = False # True si la animación actual está en pausa.
        self.animation_history = [] # Almacena el libreto de la animación actual.
        self.current_step_index = -1 # El índice del paso actual que se está ejecutando.
        self.animation_speed = 2.0 # Velocidad de la animación (pasos por segundo).

        # Define las áreas rectangulares para los botones y el slider para detectar clics.
        self.buttons = {
            'insert': pygame.Rect(10, 10, 80, 32), 'delete': pygame.Rect(100, 10, 80, 32),
            'find': pygame.Rect(190, 10, 80, 32), 'print': pygame.Rect(280, 10, 80, 32),
            'step_back': pygame.Rect(10, SCREEN_HEIGHT - 42, 80, 32),
            'pause': pygame.Rect(100, SCREEN_HEIGHT - 42, 80, 32),
            'step_forward': pygame.Rect(190, SCREEN_HEIGHT - 42, 80, 32)
        }
        self.slider = {'rect': pygame.Rect(300, SCREEN_HEIGHT - 35, 200, 15), 'handle': pygame.Rect(0,0,10,25)}
        self._update_slider_handle()

    def _update_slider_handle(self):
        """Mueve la manija del slider según el valor de self.animation_speed."""
        x_pos = self.slider['rect'].x + ((self.animation_speed - 0.5) / 9.5) * self.slider['rect'].width
        self.slider['handle'].center = (x_pos, self.slider['rect'].centery)

    def _recalcular_posiciones(self, nodo, x, y, h_spacing):
        """Algoritmo recursivo para asignar coordenadas (x, y) a cada nodo y que se vea ordenado."""
        if nodo:
            nodo.x, nodo.y = x, y
            self._recalcular_posiciones(nodo.izquierda, x - h_spacing, y + 80, h_spacing / 2)
            self._recalcular_posiciones(nodo.derecha, x + h_spacing, y + 80, h_spacing / 2)

    def _draw_arbol_recursivo(self, nodo, highlighted_nodes, path_nodes):
        """Función recursiva que dibuja los nodos y las líneas del árbol."""
        if not nodo: return
        
        # Dibuja la línea y el número de altura si tiene hijo izquierdo.
        if nodo.izquierda:
            pygame.draw.line(self.screen, LINE_COLOR, (nodo.x, nodo.y), (nodo.izquierda.x, nodo.izquierda.y), 2)
            height_text = self.height_font.render(str(self.arbol._get_altura(nodo.izquierda)), True, (255,0,0))
            self.screen.blit(height_text, ((nodo.x + nodo.izquierda.x)/2 + 5, (nodo.y + nodo.izquierda.y)/2))
            self._draw_arbol_recursivo(nodo.izquierda, highlighted_nodes, path_nodes)
        
        # Dibuja la línea y el número de altura si tiene hijo derecho.
        if nodo.derecha:
            pygame.draw.line(self.screen, LINE_COLOR, (nodo.x, nodo.y), (nodo.derecha.x, nodo.derecha.y), 2)
            height_text = self.height_font.render(str(self.arbol._get_altura(nodo.derecha)), True, (255,0,0))
            self.screen.blit(height_text, ((nodo.x + nodo.derecha.x)/2 + 5, (nodo.y + nodo.derecha.y)/2))
            self._draw_arbol_recursivo(nodo.derecha, highlighted_nodes, path_nodes)
        
        # Determina el color del nodo según el estado de la animación.
        color = NODE_COLOR
        if nodo in highlighted_nodes: color = highlighted_nodes[nodo]
        elif nodo in path_nodes: color = NODE_HIGHLIGHT_COLOR
        
        # Dibuja el círculo y el valor del nodo.
        pygame.draw.circle(self.screen, color, (int(nodo.x), int(nodo.y)), NODE_RADIUS)
        text_surface = self.font.render(str(nodo.valor), True, TEXT_COLOR)
        self.screen.blit(text_surface, text_surface.get_rect(center=(int(nodo.x), int(nodo.y))))

    def _draw_ui(self):
        """La función maestra de dibujo: orquesta todo lo que se ve en pantalla en cada fotograma."""
        # Determina qué nodos resaltar en este fotograma específico.
        highlighted_nodes = {}
        path_nodes = []
        if self.animating and 0 <= self.current_step_index < len(self.animation_history):
            paso = self.animation_history[self.current_step_index]
            if paso['tipo'] == 'highlight':
                for n in paso['nodos']: highlighted_nodes[n] = paso['color']
            elif paso['tipo'] == 'highlight_path':
                path_nodes = paso['nodos']

        # Dibuja el fondo y los paneles de la UI.
        self.screen.fill(BG_COLOR)
        pygame.draw.rect(self.screen, UI_BG_COLOR, (0, 0, SCREEN_WIDTH, 52))
        pygame.draw.rect(self.screen, UI_BG_COLOR, (0, SCREEN_HEIGHT - 125, SCREEN_WIDTH, 125))

        # Llama a la función que dibuja el árbol.
        if self.arbol.raiz:
            self._draw_arbol_recursivo(self.arbol.raiz, highlighted_nodes, path_nodes)
        
        # Dibuja la caja de texto, los botones y el slider.
        input_box = pygame.Rect(380, 10, 140, 32)
        pygame.draw.rect(self.screen, (255, 255, 255), input_box)
        pygame.draw.rect(self.screen, (0, 0, 0), input_box, 2)
        self.screen.blit(self.font.render(self.input_text, True, (0, 0, 0)), (input_box.x + 5, input_box.y + 10))

        for name, rect in self.buttons.items():
            pygame.draw.rect(self.screen, BUTTON_COLOR, rect, border_radius=5)
            text = name.replace('_', ' ').title()
            if name == 'pause': text = 'Pause' if not self.paused else 'Play'
            
            text_surface = self.font.render(text, True, BUTTON_TEXT_COLOR)
            text_rect = text_surface.get_rect(center=rect.center)
            self.screen.blit(text_surface, text_rect)
        
        pygame.draw.rect(self.screen, (200,200,200), self.slider['rect'], border_radius=8)
        pygame.draw.rect(self.screen, BUTTON_COLOR, self.slider['handle'], border_radius=3)

        # Dibuja los textos de estado y de impresión.
        status_surface = self.status_font.render(self.status_text, True, STATUS_TEXT_COLOR)
        self.screen.blit(status_surface, (10, SCREEN_HEIGHT - 85))
        print_surface = self.status_font.render(self.print_output_text, True, (0, 100, 0))
        self.screen.blit(print_surface, (10, SCREEN_HEIGHT - 115))

        # Actualiza la pantalla para que el usuario vea todos los cambios.
        pygame.display.flip()
        
    def _handle_click(self, pos):
        """Router de clics: determina qué botón se presionó."""
        for name, rect in self.buttons.items():
            if rect.collidepoint(pos):
                self._handle_button_press(name)
                return
        if self.slider['rect'].collidepoint(pos):
            self.slider['handle'].centerx = pos[0]
            self.animation_speed = 0.5 + ((pos[0] - self.slider['rect'].x) / self.slider['rect'].width) * 9.5
    
    def _start_animation(self, steps):
        """Reinicia el estado de la animación con un nuevo libreto."""
        self.animation_history = steps
        self.current_step_index = -1
        self.animating = True
        self.paused = False

    def _handle_button_press(self, name):
        """Ejecuta la acción correspondiente a cada botón."""
        if name in ['insert', 'delete', 'find']:
            if self.animating: return # No permite iniciar una acción si otra está en curso.
            try:
                valor = int(self.input_text)
                if name == 'insert': self._start_animation(self.arbol.insertar(valor))
                elif name == 'delete': self._start_animation(self.arbol.eliminar(valor))
                elif name == 'find': self._start_animation(self.arbol.buscar(valor))
                self.input_text = ''
            except ValueError:
                self.status_text = "Error: Ingresa un número válido."
        
        elif name == 'print':
            if self.animating: return
            self.print_output_text = '' # Limpia el resultado anterior.
            self._start_animation(self.arbol.imprimir_animado()) # Inicia la nueva animación de impresión.
        
        elif name == 'pause':
            self.paused = not self.paused
        elif name == 'step_forward':
            self.paused = True
            if self.current_step_index < len(self.animation_history) - 1:
                self.current_step_index += 1
                self._process_current_step()
        elif name == 'step_back':
            self.paused = True
            if self.current_step_index > 0:
                self.current_step_index -= 1
                self._process_current_step()
    
    def _process_current_step(self):
        """Ejecuta la acción de un paso de animación UNA SOLA VEZ."""
        if self.animating and 0 <= self.current_step_index < len(self.animation_history):
            paso = self.animation_history[self.current_step_index]
            if paso['tipo'] == 'texto':
                self.status_text = paso['msg']
            elif paso['tipo'] == 'recalcular_posiciones':
                self._recalcular_posiciones(self.arbol.raiz, SCREEN_WIDTH // 2, 100, SCREEN_WIDTH // 4)
            elif paso['tipo'] == 'add_to_print':
                if self.print_output_text:
                    self.print_output_text += f" -> {paso['valor']}"
                else:
                    self.print_output_text = str(paso['valor'])
                self.status_text = "Imprimiendo árbol en orden..."

    def run(self):
        """El motor principal del programa. Contiene el bucle infinito que lo mantiene vivo."""
        last_step_time = 0
        while True:
            # 1. Manejo de Eventos: Revisa si el usuario ha hecho algo (clic, teclear, cerrar ventana).
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE: self.input_text = self.input_text[:-1]
                    else: self.input_text += event.unicode
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self._handle_click(event.pos)
            
            # 2. Lógica de AVANCE de la Animación: Si hay una animación y no está en pausa,
            #    avanza al siguiente paso cuando el temporizador lo indica.
            if self.animating and not self.paused:
                current_time = time.time()
                if current_time - last_step_time > (1 / self.animation_speed):
                    if self.current_step_index < len(self.animation_history) - 1:
                        self.current_step_index += 1
                        self._process_current_step() # Ejecuta la acción del nuevo paso.
                        last_step_time = current_time
                    else:
                        self.animating = False

            # 3. Dibujado: Llama a la función maestra de dibujo para actualizar la pantalla.
            self._draw_ui()
            # Controla que el bucle no corra a más de 60 fotogramas por segundo.
            self.clock.tick(60)

# =========================================================================================
# --- SECCIÓN 4: PUNTO DE ENTRADA DEL PROGRAMA ---
# Este es el código que se ejecuta al iniciar el script.
# =========================================================================================
if __name__ == '__main__':
    arbol = ArbolAVL()                     # 1. Crea el "cerebro".
    visualizador = VisualizadorPygame(arbol) # 2. Crea el "cuerpo" y le pasa el cerebro.
    visualizador.run()                     # 3. Inicia el motor del programa.
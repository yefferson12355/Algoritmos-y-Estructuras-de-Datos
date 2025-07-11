import pygame
import sys
import math
import time

# --- Configuración Visual ---
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 800
BG_COLOR = (245, 245, 245)
NODE_COLOR = (70, 130, 180)
NODE_HIGHLIGHT_COLOR = (255, 165, 0)
NODE_FOUND_COLOR = (50, 205, 50)
LINE_COLOR = (0, 0, 0)
TEXT_COLOR = (255, 255, 255)
STATUS_TEXT_COLOR = (0, 0, 0)
UI_BG_COLOR = (220, 220, 220)
BUTTON_COLOR = (100, 100, 100)
BUTTON_TEXT_COLOR = (255, 255, 255)
NODE_RADIUS = 28
FONT_SIZE = 16
HEIGHT_FONT_SIZE = 12

class Nodo:
    def __init__(self, valor, x=0, y=0):
        self.valor = valor
        self.izquierda = None
        self.derecha = None
        self.altura = 1
        self.x = x
        self.y = y

# --- Clase del Árbol AVL (Mejorada con todas las operaciones) ---
# --- Clase del Árbol AVL (CORREGIDA Y MEJORADA) ---
class ArbolAVL:
    def __init__(self):
        self.raiz = None
        self.pasos_animacion = []

    def _get_altura(self, nodo):
        return nodo.altura if nodo else 0

    def _get_balance(self, nodo):
        return self._get_altura(nodo.izquierda) - self._get_altura(nodo.derecha) if nodo else 0
    
    def _get_min_valor_nodo(self, nodo):
        return self._get_min_valor_nodo(nodo.izquierda) if nodo.izquierda else nodo

    def _recalcular_altura(self, nodo):
        return 1 + max(self._get_altura(nodo.izquierda), self._get_altura(nodo.derecha))

    def _rotar_derecha(self, z):
        self.pasos_animacion.append({'tipo': 'texto', 'msg': f"Desbalance en {z.valor}. Rotando a la derecha..."})
        self.pasos_animacion.append({'tipo': 'highlight', 'nodos': [z, z.izquierda], 'color': NODE_HIGHLIGHT_COLOR})
        y = z.izquierda
        T3 = y.derecha
        y.derecha = z
        z.izquierda = T3
        z.altura = self._recalcular_altura(z)
        y.altura = self._recalcular_altura(y)
        self.pasos_animacion.append({'tipo': 'recalcular_posiciones'})
        return y

    def _rotar_izquierda(self, z):
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
        balance = self._get_balance(nodo)
        if balance > 1:
            if self._get_balance(nodo.izquierda) < 0:
                nodo.izquierda = self._rotar_izquierda(nodo.izquierda)
            return self._rotar_derecha(nodo)
        if balance < -1:
            if self._get_balance(nodo.derecha) > 0:
                # --- CORRECCIÓN DE BUG SUTIL ---
                nodo.derecha = self._rotar_derecha(nodo.derecha) 
            return self._rotar_izquierda(nodo)
        return nodo

    def insertar(self, valor):
        self.pasos_animacion = []
        self.raiz = self._insertar_rec(self.raiz, valor)
        self.pasos_animacion.append({'tipo': 'recalcular_posiciones'})
        self.pasos_animacion.append({'tipo': 'texto', 'msg': f"Inserción de {valor} completada."})
        return self.pasos_animacion

    def _insertar_rec(self, raiz, valor):
        if not raiz:
            self.pasos_animacion.append({'tipo': 'texto', 'msg': f"Insertando nuevo nodo: {valor}"})
            return Nodo(valor)
        
        self.pasos_animacion.append({'tipo': 'highlight', 'nodos': [raiz], 'color': NODE_HIGHLIGHT_COLOR})
        if valor < raiz.valor:
            self.pasos_animacion.append({'tipo': 'texto', 'msg': f"{valor} < {raiz.valor}. Yendo a la izquierda."})
            raiz.izquierda = self._insertar_rec(raiz.izquierda, valor)
        elif valor > raiz.valor:
            self.pasos_animacion.append({'tipo': 'texto', 'msg': f"{valor} > {raiz.valor}. Yendo a la derecha."})
            raiz.derecha = self._insertar_rec(raiz.derecha, valor)
        else: return raiz

        raiz.altura = self._recalcular_altura(raiz)
        return self._balancear(raiz)

    def eliminar(self, valor):
        self.pasos_animacion = []
        self.raiz = self._eliminar_rec(self.raiz, valor)
        self.pasos_animacion.append({'tipo': 'recalcular_posiciones'})
        self.pasos_animacion.append({'tipo': 'texto', 'msg': f"Eliminación de {valor} completada."})
        return self.pasos_animacion

    def _eliminar_rec(self, raiz, valor):
        if not raiz:
            self.pasos_animacion.append({'tipo': 'texto', 'msg': f"Valor {valor} no encontrado."})
            return raiz
        
        self.pasos_animacion.append({'tipo': 'highlight', 'nodos': [raiz], 'color': NODE_HIGHLIGHT_COLOR})
        if valor < raiz.valor:
            raiz.izquierda = self._eliminar_rec(raiz.izquierda, valor)
        elif valor > raiz.valor:
            raiz.derecha = self._eliminar_rec(raiz.derecha, valor)
        else:
            self.pasos_animacion.append({'tipo': 'texto', 'msg': f"Nodo {valor} encontrado. Eliminando..."})
            if raiz.izquierda is None: return raiz.derecha
            if raiz.derecha is None: return raiz.izquierda
            
            temp = self._get_min_valor_nodo(raiz.derecha)
            self.pasos_animacion.append({'tipo': 'texto', 'msg': f"Reemplazando con sucesor: {temp.valor}"})
            raiz.valor = temp.valor
            raiz.derecha = self._eliminar_rec(raiz.derecha, temp.valor)

        raiz.altura = self._recalcular_altura(raiz)
        return self._balancear(raiz)
    
    def buscar(self, valor):
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

    # --- NUEVA FUNCIÓN DE IMPRESIÓN ANIMADA ---
    def imprimir_animado(self):
        self.pasos_animacion = []
        self._imprimir_animado_rec(self.raiz)
        self.pasos_animacion.append({'tipo': 'texto', 'msg': "Impresión en orden completada."})
        return self.pasos_animacion

    def _imprimir_animado_rec(self, nodo):
        if nodo:
            # 1. Recorre subárbol izquierdo
            self._imprimir_animado_rec(nodo.izquierda)
            
            # 2. Visita y anima el nodo actual
            self.pasos_animacion.append({'tipo': 'highlight', 'nodos': [nodo], 'color': NODE_FOUND_COLOR})
            self.pasos_animacion.append({'tipo': 'add_to_print', 'valor': nodo.valor})
            
            # 3. Recorre subárbol derecho
            self._imprimir_animado_rec(nodo.derecha)

# --- Clase Principal del Visualizador con Pygame (CORREGIDA Y MEJORADA) ---
class VisualizadorPygame:
    def __init__(self, arbol):
        pygame.init()
        self.arbol = arbol
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Visualizador de Árbol AVL Interactivo")
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.status_font = pygame.font.Font(None, 28)
        self.height_font = pygame.font.Font(None, HEIGHT_FONT_SIZE)
        self.clock = pygame.time.Clock()
        
        self.input_text = ''
        self.status_text = 'Ingresa un número y elige una acción'
        self.print_output_text = ''
        self.animating = False
        self.paused = False
        self.animation_history = []
        self.current_step_index = -1
        self.animation_speed = 2.0

        self.buttons = {
            'insert': pygame.Rect(10, 10, 80, 32),
            'delete': pygame.Rect(100, 10, 80, 32),
            'find': pygame.Rect(190, 10, 80, 32),
            'print': pygame.Rect(280, 10, 80, 32),
            'step_back': pygame.Rect(10, SCREEN_HEIGHT - 42, 80, 32),
            'pause': pygame.Rect(100, SCREEN_HEIGHT - 42, 80, 32),
            'step_forward': pygame.Rect(190, SCREEN_HEIGHT - 42, 80, 32)
        }
        self.slider = {'rect': pygame.Rect(300, SCREEN_HEIGHT - 35, 200, 15), 'handle': pygame.Rect(0,0,10,25)}
        self._update_slider_handle()

    def _update_slider_handle(self):
        x_pos = self.slider['rect'].x + ((self.animation_speed - 0.5) / 9.5) * self.slider['rect'].width
        self.slider['handle'].center = (x_pos, self.slider['rect'].centery)

    def _recalcular_posiciones(self, nodo, x, y, h_spacing):
        if nodo:
            nodo.x, nodo.y = x, y
            self._recalcular_posiciones(nodo.izquierda, x - h_spacing, y + 80, h_spacing / 2)
            self._recalcular_posiciones(nodo.derecha, x + h_spacing, y + 80, h_spacing / 2)

    def _draw_arbol_recursivo(self, nodo, highlighted_nodes, path_nodes):
        if not nodo: return
        
        if nodo.izquierda:
            pygame.draw.line(self.screen, LINE_COLOR, (nodo.x, nodo.y), (nodo.izquierda.x, nodo.izquierda.y), 2)
            height_text = self.height_font.render(str(self.arbol._get_altura(nodo.izquierda)), True, (255,0,0))
            self.screen.blit(height_text, ((nodo.x + nodo.izquierda.x)/2 + 5, (nodo.y + nodo.izquierda.y)/2))
            self._draw_arbol_recursivo(nodo.izquierda, highlighted_nodes, path_nodes)
        if nodo.derecha:
            pygame.draw.line(self.screen, LINE_COLOR, (nodo.x, nodo.y), (nodo.derecha.x, nodo.derecha.y), 2)
            height_text = self.height_font.render(str(self.arbol._get_altura(nodo.derecha)), True, (255,0,0))
            self.screen.blit(height_text, ((nodo.x + nodo.derecha.x)/2 + 5, (nodo.y + nodo.derecha.y)/2))
            self._draw_arbol_recursivo(nodo.derecha, highlighted_nodes, path_nodes)
        
        color = NODE_COLOR
        if nodo in highlighted_nodes: color = highlighted_nodes[nodo]
        elif nodo in path_nodes: color = NODE_HIGHLIGHT_COLOR
        
        pygame.draw.circle(self.screen, color, (int(nodo.x), int(nodo.y)), NODE_RADIUS)
        text_surface = self.font.render(str(nodo.valor), True, TEXT_COLOR)
        self.screen.blit(text_surface, text_surface.get_rect(center=(int(nodo.x), int(nodo.y))))

    def _draw_ui(self):
        highlighted_nodes = {}
        path_nodes = []
        if self.animating and 0 <= self.current_step_index < len(self.animation_history):
            paso = self.animation_history[self.current_step_index]
            if paso['tipo'] == 'highlight':
                for n in paso['nodos']: highlighted_nodes[n] = paso['color']
            elif paso['tipo'] == 'highlight_path':
                path_nodes = paso['nodos']

        self.screen.fill(BG_COLOR)
        pygame.draw.rect(self.screen, UI_BG_COLOR, (0, 0, SCREEN_WIDTH, 52))
        pygame.draw.rect(self.screen, UI_BG_COLOR, (0, SCREEN_HEIGHT - 125, SCREEN_WIDTH, 125))

        if self.arbol.raiz:
            self._draw_arbol_recursivo(self.arbol.raiz, highlighted_nodes, path_nodes)
        
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

        status_surface = self.status_font.render(self.status_text, True, STATUS_TEXT_COLOR)
        self.screen.blit(status_surface, (10, SCREEN_HEIGHT - 85))

        print_surface = self.status_font.render(self.print_output_text, True, (0, 100, 0))
        self.screen.blit(print_surface, (10, SCREEN_HEIGHT - 115))

        pygame.display.flip()
        
    def _handle_click(self, pos):
        for name, rect in self.buttons.items():
            if rect.collidepoint(pos):
                self._handle_button_press(name)
                return
        if self.slider['rect'].collidepoint(pos):
            self.slider['handle'].centerx = pos[0]
            self.animation_speed = 0.5 + ((pos[0] - self.slider['rect'].x) / self.slider['rect'].width) * 9.5
    
    def _start_animation(self, steps):
        self.animation_history = steps
        self.current_step_index = -1
        self.animating = True
        self.paused = False
        if steps and steps[0].get('tipo') == 'add_to_print':
             self.print_output_text = ''


    # Reemplaza esta función completa en tu clase VisualizadorPygame

    # Reemplaza estas funciones en tu clase VisualizadorPygame y añade la nueva

    def _handle_button_press(self, name):
        if name in ['insert', 'delete', 'find']:
            if self.animating: return 
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
            self.print_output_text = '' 
            self._start_animation(self.arbol.imprimir_animado())
            self._process_current_step() # Procesar el primer paso inmediatamente

        elif name == 'pause':
            self.paused = not self.paused
        elif name == 'step_forward':
            self.paused = True
            if self.current_step_index < len(self.animation_history) - 1:
                self.current_step_index += 1
                self._process_current_step() # <-- CORRECCIÓN
        elif name == 'step_back':
            self.paused = True
            if self.current_step_index > 0:
                self.current_step_index -= 1
                self._process_current_step() # <-- CORRECCIÓN
    
    # --- NUEVA FUNCIÓN AYUDANTE ---
    def _process_current_step(self):
        """ Ejecuta la acción de un paso de animación UNA SOLA VEZ. """
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
        last_step_time = 0
        while True:
            # --- Manejo de Eventos ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE: self.input_text = self.input_text[:-1]
                    else: self.input_text += event.unicode
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self._handle_click(event.pos)
            
            # --- Lógica de AVANCE de la Animación ---
            if self.animating and not self.paused:
                current_time = time.time()
                if current_time - last_step_time > (1 / self.animation_speed):
                    if self.current_step_index < len(self.animation_history) - 1:
                        self.current_step_index += 1
                        # Procesa la acción del nuevo paso JUSTO cuando avanza
                        self._process_current_step() 
                        last_step_time = current_time
                    else:
                        self.animating = False

            # --- Dibujado (ya no procesa la lógica, solo dibuja) ---
            self._draw_ui()
            self.clock.tick(60)
            
if __name__ == '__main__':
    arbol = ArbolAVL()
    visualizador = VisualizadorPygame(arbol)
    visualizador.run()
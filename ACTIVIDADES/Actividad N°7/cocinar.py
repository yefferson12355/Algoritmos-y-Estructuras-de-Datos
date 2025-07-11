import pygame
import sys
import tkinter as tk
from tkinter import simpledialog, messagebox

# --- Configuración Visual ---
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 800
BG_COLOR = (250, 245, 239)
NODE_COLOR = (70, 130, 180)
NODE_CURRENT_COLOR = (255, 165, 0)
NODE_RESULT_COLOR = (50, 205, 50)
LINE_COLOR = (0, 0, 0)
TEXT_COLOR = (255, 255, 255)
QUESTION_TEXT_COLOR = (0, 0, 0)
UI_BG_COLOR = (220, 220, 220)
BUTTON_YES_COLOR = (144, 238, 144)
BUTTON_NO_COLOR = (240, 128, 128)
NODE_RADIUS = 45
FONT_QUESTION = None # Se inicializará en Pygame
FONT_NODE = None

# =========================================================================================
# --- SECCIÓN 1: La Lógica del Árbol de Decisión ---
# =========================================================================================

class NodoDecision:
    """Representa un nodo en el árbol. Puede ser una pregunta o un resultado final."""
    def __init__(self, pregunta=None, resultado=None, si=None, no=None):
        self.pregunta = pregunta    # El texto de la pregunta (si es un nodo interno)
        self.resultado = resultado  # El texto del resultado (si es un nodo hoja)
        self.si = si                # El nodo al que se va si la respuesta es "Sí"
        self.no = no                # El nodo al que se va si la respuesta es "No"
        # Atributos para la visualización
        self.x = 0
        self.y = 0
        self.parent = None # Referencia al padre para dibujar la línea

def crear_arbol_inicial():
    """Crea y devuelve el árbol de decisión con el que empezará el programa."""
    # Nodos hoja (los resultados finales)
    receta_saltado = NodoDecision(resultado="Pollo Saltado")
    receta_lentejas = NodoDecision(resultado="Lentejas")
    receta_huevos = NodoDecision(resultado="Huevos Revueltos")
    receta_ensalada = NodoDecision(resultado="Ensalada Rápida")
    
    # Nodos de pregunta
    pregunta_pollo = NodoDecision(pregunta="¿Tienes pollo?", si=receta_saltado, no=receta_lentejas)
    pregunta_huevos = NodoDecision(pregunta="¿Tienes huevos?", si=receta_huevos, no=receta_ensalada)
    
    # Nodo raíz (la primera pregunta)
    raiz = NodoDecision(pregunta="¿Buscas algo rápido (<20 min)?", si=pregunta_huevos, no=pregunta_pollo)
    
    return raiz

# =========================================================================================
# --- SECCIÓN 2: El Visualizador Gráfico y Animado ---
# =========================================================================================

class VisualizadorArbolDecision:
    def __init__(self, arbol_inicial):
        """Prepara la ventana, los botones y el estado inicial del programa."""
        pygame.init()
        # Esconder la ventana principal de Tkinter que no usaremos
        self.root_tk = tk.Tk()
        self.root_tk.withdraw()

        # Configuración de Pygame
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Sistema Experto: Asistente de Cocina")
        FONT_QUESTION = pygame.font.Font(None, 48)
        FONT_NODE = pygame.font.Font(None, 20)
        self.fonts = {'pregunta': FONT_QUESTION, 'nodo': FONT_NODE}
        
        # Estado del árbol
        self.arbol_raiz = arbol_inicial
        self.nodo_actual = self.arbol_raiz
        
        # Estado de la UI
        self.game_over = False
        self.buttons = {
            'si': pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT - 100, 120, 50),
            'no': pygame.Rect(SCREEN_WIDTH // 2 + 30, SCREEN_HEIGHT - 100, 120, 50)
        }
        
        # Dibuja el estado inicial
        self._recalcular_y_dibujar_todo()

    def _recalcular_posiciones(self, nodo, x, y, h_spacing, y_spacing=120):
        """Asigna coordenadas a cada nodo para que se vea ordenado en pantalla."""
        if nodo:
            nodo.x, nodo.y = x, y
            if nodo.si:
                nodo.si.parent = nodo
                self._recalcular_posiciones(nodo.si, x - h_spacing, y + y_spacing, h_spacing / 2)
            if nodo.no:
                nodo.no.parent = nodo
                self._recalcular_posiciones(nodo.no, x + h_spacing, y + y_spacing, h_spacing / 2)

    def _draw_arbol(self, nodo):
        """Dibuja recursivamente el árbol en la pantalla."""
        if not nodo: return

        # Dibuja la línea que lo conecta a su padre
        if nodo.parent:
            pygame.draw.line(self.screen, LINE_COLOR, (nodo.parent.x, nodo.parent.y), (nodo.x, nodo.y), 2)
        
        # Dibuja los subárboles
        self._draw_arbol(nodo.si)
        self._draw_arbol(nodo.no)
        
        # Determina el color del nodo
        color = NODE_COLOR
        if nodo == self.nodo_actual:
            color = NODE_CURRENT_COLOR # Naranja para el nodo actual
        elif nodo.resultado:
            color = NODE_RESULT_COLOR # Verde para los resultados

        # Dibuja el círculo y el texto del nodo
        pygame.draw.circle(self.screen, color, (nodo.x, nodo.y), NODE_RADIUS)
        texto = nodo.pregunta.split('?')[0] + '?' if nodo.pregunta else nodo.resultado
        text_surface = self.fonts['nodo'].render(texto, True, TEXT_COLOR)
        self.screen.blit(text_surface, text_surface.get_rect(center=(nodo.x, nodo.y)))
        
    def _draw_ui(self):
        """Dibuja todos los elementos de la interfaz."""
        # Dibuja la pregunta o resultado actual en la parte superior
        texto_actual = ""
        if not self.game_over:
            texto_actual = self.nodo_actual.pregunta
        else:
            texto_actual = f"Diagnóstico: ¡{self.nodo_actual.resultado}!"
        
        question_surface = self.fonts['pregunta'].render(texto_actual, True, QUESTION_TEXT_COLOR)
        self.screen.blit(question_surface, question_surface.get_rect(center=(SCREEN_WIDTH // 2, 50)))
        
        # Dibuja los botones "Sí" y "No" si el juego no ha terminado
        if not self.game_over:
            pygame.draw.rect(self.screen, BUTTON_YES_COLOR, self.buttons['si'], border_radius=10)
            pygame.draw.rect(self.screen, BUTTON_NO_COLOR, self.buttons['no'], border_radius=10)
            si_text = self.fonts['pregunta'].render("Sí", True, (0,0,0))
            no_text = self.fonts['pregunta'].render("No", True, (0,0,0))
            self.screen.blit(si_text, si_text.get_rect(center=self.buttons['si'].center))
            self.screen.blit(no_text, no_text.get_rect(center=self.buttons['no'].center))

    def _recalcular_y_dibujar_todo(self):
        """Función central que actualiza y dibuja todo en pantalla."""
        self.screen.fill(BG_COLOR)
        self._recalcular_posiciones(self.arbol_raiz, SCREEN_WIDTH // 2, 150, SCREEN_WIDTH / 4)
        self._draw_arbol(self.arbol_raiz)
        self._draw_ui()
        pygame.display.flip()

    def _manejar_respuesta(self, respuesta_si):
        """Procesa la respuesta del usuario (Sí o No) y avanza en el árbol."""
        if self.game_over: return
        
        # Determina el próximo nodo
        proximo_nodo = self.nodo_actual.si if respuesta_si else self.nodo_actual.no
        if not proximo_nodo: return

        self.nodo_actual = proximo_nodo
        
        # Si el próximo nodo es un resultado, termina el juego.
        if self.nodo_actual.resultado:
            self.game_over = True
        
        self._recalcular_y_dibujar_todo()

        # Si el juego terminó, preguntar al usuario
        if self.game_over:
            self._preguntar_al_finalizar()

    def _preguntar_al_finalizar(self):
        """Muestra una ventana emergente al llegar a un diagnóstico."""
        es_correcto = messagebox.askyesno(
            "Diagnóstico Finalizado",
            f"Mi sugerencia es: {self.nodo_actual.resultado}.\n\n¿Es una buena sugerencia?"
        )
        if not es_correcto:
            self._aprender_nuevo_resultado()
        else:
            # Preguntar si quiere reiniciar
            reiniciar = messagebox.askyesno("Juego Terminado", "¿Quieres jugar de nuevo?")
            if reiniciar:
                self.reiniciar()

    def _aprender_nuevo_resultado(self):
        """Inicia el proceso para enseñarle una nueva receta/pregunta al árbol."""
        viejo_resultado_nodo = self.nodo_actual
        
        nueva_receta = simpledialog.askstring("Aprender", "¡Vaya! Me equivoqué. ¿Cuál era la receta que tenías en mente?")
        if not nueva_receta: 
            self.reiniciar()
            return
            
        nueva_pregunta = simpledialog.askstring("Aprender", f"Por favor, escribe una pregunta de SÍ/NO que diferencie '{nueva_receta}' de '{viejo_resultado_nodo.resultado}'.")
        if not nueva_pregunta:
            self.reiniciar()
            return

        respuesta_para_nueva_receta = messagebox.askquestion("Aprender", f"Y para la pregunta '{nueva_pregunta}', ¿la respuesta para '{nueva_receta}' es 'Sí' o 'No'?")

        # Transforma el nodo hoja actual en un nodo de pregunta
        viejo_resultado_nodo.pregunta = nueva_pregunta
        viejo_resultado_valor = viejo_resultado_nodo.resultado
        viejo_resultado_nodo.resultado = None

        nuevo_nodo_receta = NodoDecision(resultado=nueva_receta)
        viejo_nodo_resultado = NodoDecision(resultado=viejo_resultado_valor)

        # Reorganiza las ramas según la respuesta del usuario
        if respuesta_para_nueva_receta == 'yes':
            viejo_resultado_nodo.si = nuevo_nodo_receta
            viejo_resultado_nodo.no = viejo_nodo_resultado
        else:
            viejo_resultado_nodo.no = nuevo_nodo_receta
            viejo_resultado_nodo.si = viejo_nodo_resultado
        
        messagebox.showinfo("¡Gracias!", "¡He aprendido una nueva receta! Reiniciando el juego.")
        self.reiniciar()

    def reiniciar(self):
        """Reinicia el juego al estado inicial."""
        self.nodo_actual = self.arbol_raiz
        self.game_over = False
        self._recalcular_y_dibujar_todo()

    def run(self):
        """El bucle principal del programa que maneja los eventos."""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.buttons['si'].collidepoint(event.pos):
                        self._manejar_respuesta(True)
                    elif self.buttons['no'].collidepoint(event.pos):
                        self._manejar_respuesta(False)
        pygame.quit()
        sys.exit()


# =========================================================================================
# --- SECCIÓN 3: Punto de Entrada del Programa ---
# =========================================================================================
if __name__ == '__main__':
    arbol_base = crear_arbol_inicial()
    juego = VisualizadorArbolDecision(arbol_base)
    juego.run()
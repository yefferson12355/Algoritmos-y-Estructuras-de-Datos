import pygame
import sys
import tkinter as tk
from tkinter import simpledialog, messagebox
import pickle  # Librería para guardar y cargar objetos de Python
import os      # Librería para interactuar con el sistema operativo (y verificar si un archivo existe)

# --- Constantes ---
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 800
SAVE_FILE = "arbol_de_decision_viajes.pkl"  # Nombre del archivo donde se guardará el árbol

# --- Configuración Visual ---
BG_COLOR = (250, 245, 239)
NODE_COLOR = (0, 128, 128)
NODE_CURRENT_COLOR = (255, 165, 0)
NODE_RESULT_COLOR = (218, 165, 32)
LINE_COLOR = (0, 0, 0)
TEXT_COLOR = (255, 255, 255)
QUESTION_TEXT_COLOR = (0, 0, 0)
BUTTON_YES_COLOR = (144, 238, 144)
BUTTON_NO_COLOR = (240, 128, 128)
BUTTON_CTRL_COLOR = (180, 180, 180)
NODE_RADIUS = 55
FONT_QUESTION = None
FONT_NODE = None

# =========================================================================================
# --- SECCIÓN 1: La Lógica del Árbol de Decisión ---
# =========================================================================================

class NodoDecision:
    """Representa un nodo en el árbol. Es la misma estructura de antes."""
    def __init__(self, pregunta=None, resultado=None, si=None, no=None):
        self.pregunta = pregunta
        self.resultado = resultado
        self.si = si
        self.no = no
        self.x, self.y, self.parent = 0, 0, None

def crear_arbol_viajes_largo():
    """Crea el árbol de decisión por defecto, solo si no existe un archivo guardado."""
    # (El contenido de esta función es el mismo árbol detallado de antes)
    dest_cusco = NodoDecision(resultado="Cusco (Machu Picchu)")
    dest_kuelap = NodoDecision(resultado="Chachapoyas (Kuélap)")
    dest_iquitos = NodoDecision(resultado="Iquitos (Río Amazonas)")
    dest_colca = NodoDecision(resultado="Arequipa (Cañón del Colca)")
    dest_titicaca = NodoDecision(resultado="Puno (Lago Titicaca)")
    dest_mancora = NodoDecision(resultado="Máncora (Fiesta y Surf)")
    dest_paracas = NodoDecision(resultado="Paracas (Naturaleza y Relax)")
    dest_lima = NodoDecision(resultado="Lima (Gastronomía y Cultura)")
    pregunta_canon_lago = NodoDecision(pregunta="¿Cañón profundo o lago de altura?", si=dest_colca, no=dest_titicaca)
    pregunta_selva_andes = NodoDecision(pregunta="¿Prefieres selva o paisajes andinos?", si=dest_iquitos, no=pregunta_canon_lago)
    pregunta_primera_vez_arqueo = NodoDecision(pregunta="¿Es tu primera gran visita arqueológica?", si=dest_cusco, no=dest_kuelap)
    pregunta_fiesta_relax = NodoDecision(pregunta="¿Buscas ambiente de fiesta o tranquilidad?", si=dest_mancora, no=dest_paracas)
    pregunta_historia_naturaleza = NodoDecision(pregunta="¿Tu prioridad es la historia/arqueología?", si=pregunta_primera_vez_arqueo, no=pregunta_selva_andes)
    pregunta_playa_ciudad = NodoDecision(pregunta="¿Prefieres playa o vida de ciudad?", si=pregunta_fiesta_relax, no=dest_lima)
    raiz = NodoDecision(pregunta="¿Prefieres costa o sierra/selva?", si=pregunta_playa_ciudad, no=pregunta_historia_naturaleza)
    return raiz

def cargar_arbol():
    """
    Función para cargar el árbol. Si existe un archivo guardado, lo carga.
    Si no, crea el árbol por defecto.
    """
    if os.path.exists(SAVE_FILE):
        print(f"Cargando árbol guardado desde '{SAVE_FILE}'...")
        with open(SAVE_FILE, 'rb') as f:
            return pickle.load(f)
    else:
        print("No se encontró archivo guardado. Creando árbol por defecto...")
        return crear_arbol_viajes_largo()

# =========================================================================================
# --- SECCIÓN 2: El Visualizador Gráfico (con funciones de guardado) ---
# =========================================================================================

class VisualizadorArbolDecision:
    def __init__(self, arbol_inicial):
        pygame.init()
        self.root_tk = tk.Tk()
        self.root_tk.withdraw()

        pygame.display.set_caption("Sistema Experto con Memoria: Recomendador de Viajes")
        FONT_QUESTION = pygame.font.Font(None, 42)
        FONT_NODE = pygame.font.Font(None, 16)
        self.fonts = {'pregunta': FONT_QUESTION, 'nodo': FONT_NODE}
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.arbol_raiz = arbol_inicial
        self.nodo_actual = self.arbol_raiz
        self.game_over = False
        
        # Se añaden los nuevos botones de control
        self.buttons = {
            'si': pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT - 100, 120, 50),
            'no': pygame.Rect(SCREEN_WIDTH // 2 + 30, SCREEN_HEIGHT - 100, 120, 50),
            'guardar': pygame.Rect(SCREEN_WIDTH - 230, 10, 100, 35),
            'resetear': pygame.Rect(SCREEN_WIDTH - 120, 10, 100, 35)
        }
        self._recalcular_y_dibujar_todo()

    # --- Las funciones de dibujo y recalculo de posiciones son las mismas ---
    def _recalcular_posiciones(self, nodo, x, y, h_spacing, y_spacing=120):
        if nodo:
            nodo.x, nodo.y = x, y
            if nodo.si:
                nodo.si.parent = nodo
                self._recalcular_posiciones(nodo.si, x - h_spacing, y + y_spacing, h_spacing / 2)
            if nodo.no:
                nodo.no.parent = nodo
                self._recalcular_posiciones(nodo.no, x + h_spacing, y + y_spacing, h_spacing / 2)

    def _draw_arbol(self, nodo):
        if not nodo: return
        if nodo.parent:
            pygame.draw.line(self.screen, LINE_COLOR, (nodo.parent.x, nodo.parent.y), (nodo.x, nodo.y), 2)
        self._draw_arbol(nodo.si)
        self._draw_arbol(nodo.no)
        color = NODE_COLOR
        if nodo == self.nodo_actual: color = NODE_CURRENT_COLOR
        elif nodo.resultado: color = NODE_RESULT_COLOR
        pygame.draw.circle(self.screen, color, (nodo.x, nodo.y), NODE_RADIUS)
        texto = nodo.pregunta if nodo.pregunta else nodo.resultado
        palabras = texto.split(' ')
        lineas, linea_actual = [], ""
        for palabra in palabras:
            if self.fonts['nodo'].size(linea_actual + " " + palabra)[0] < (NODE_RADIUS * 2 - 10):
                linea_actual += " " + palabra
            else:
                lineas.append(linea_actual.strip())
                linea_actual = palabra
        lineas.append(linea_actual.strip())
        y_offset = nodo.y - (len(lineas) - 1) * 7
        for i, linea in enumerate(lineas):
            text_surface = self.fonts['nodo'].render(linea, True, TEXT_COLOR)
            self.screen.blit(text_surface, text_surface.get_rect(center=(nodo.x, y_offset + i * 15)))

    def _draw_ui(self):
        """Dibuja la UI, incluyendo los nuevos botones."""
        texto_actual = ""
        if not self.game_over: texto_actual = self.nodo_actual.pregunta
        else: texto_actual = f"¡Te recomiendo visitar {self.nodo_actual.resultado}!"
        
        question_surface = self.fonts['pregunta'].render(texto_actual, True, QUESTION_TEXT_COLOR)
        self.screen.blit(question_surface, question_surface.get_rect(center=(SCREEN_WIDTH // 2, 60)))
        
        if not self.game_over:
            pygame.draw.rect(self.screen, BUTTON_YES_COLOR, self.buttons['si'], border_radius=10)
            pygame.draw.rect(self.screen, BUTTON_NO_COLOR, self.buttons['no'], border_radius=10)
            si_text = self.fonts['pregunta'].render("Sí", True, (0,0,0))
            no_text = self.fonts['pregunta'].render("No", True, (0,0,0))
            self.screen.blit(si_text, si_text.get_rect(center=self.buttons['si'].center))
            self.screen.blit(no_text, no_text.get_rect(center=self.buttons['no'].center))

        # Dibuja los botones de Guardar y Resetear
        pygame.draw.rect(self.screen, BUTTON_CTRL_COLOR, self.buttons['guardar'], border_radius=8)
        pygame.draw.rect(self.screen, BUTTON_CTRL_COLOR, self.buttons['resetear'], border_radius=8)
        guardar_text = self.fonts['nodo'].render("Guardar Progreso", True, (0,0,0))
        reset_text = self.fonts['nodo'].render("Resetear Árbol", True, (0,0,0))
        self.screen.blit(guardar_text, guardar_text.get_rect(center=self.buttons['guardar'].center))
        self.screen.blit(reset_text, reset_text.get_rect(center=self.buttons['resetear'].center))

    def _recalcular_y_dibujar_todo(self):
        self.screen.fill(BG_COLOR)
        self._recalcular_posiciones(self.arbol_raiz, SCREEN_WIDTH // 2, 150, SCREEN_WIDTH / 4)
        self._draw_arbol(self.arbol_raiz)
        self._draw_ui()
        pygame.display.flip()
    
    # --- Nuevas funciones para Guardar y Resetear ---
    def _guardar_arbol(self):
        """Guarda el estado actual del árbol en un archivo usando pickle."""
        with open(SAVE_FILE, 'wb') as f:
            pickle.dump(self.arbol_raiz, f)
        messagebox.showinfo("Guardado", f"¡Progreso guardado en '{SAVE_FILE}'!")

    def _resetear_arbol(self):
        """Resetea el árbol al estado original de fábrica."""
        confirmar = messagebox.askyesno("Resetear Árbol", "¿Estás seguro de que quieres borrar todo el conocimiento aprendido y volver al árbol original?")
        if confirmar:
            self.arbol_raiz = crear_arbol_viajes_largo()
            self.reiniciar()
            messagebox.showinfo("Reseteado", "El árbol ha sido restaurado a su estado original.")
    
    # --- La lógica de aprender y manejar respuestas es la misma ---
    def _manejar_respuesta(self, respuesta_si):
        if self.game_over: return
        proximo_nodo = self.nodo_actual.si if respuesta_si else self.nodo_actual.no
        if not proximo_nodo: return
        self.nodo_actual = proximo_nodo
        if self.nodo_actual.resultado: self.game_over = True
        self._recalcular_y_dibujar_todo()
        if self.game_over: self._preguntar_al_finalizar()

    def _preguntar_al_finalizar(self):
        es_correcto = messagebox.askyesno("Recomendación", f"Mi sugerencia: ¡Visita {self.nodo_actual.resultado}!\n\n¿Es una buena recomendación?")
        if not es_correcto: self._aprender_nuevo_resultado()
        else:
            reiniciar = messagebox.askyesno("¡Buen Viaje!", "¿Quieres otra recomendación?")
            if reiniciar: self.reiniciar()

    def _aprender_nuevo_resultado(self):
        viejo_resultado_nodo = self.nodo_actual
        nuevo_destino = simpledialog.askstring("Aprender", "¡Vaya! ¿Cuál era el destino que tenías en mente?")
        if not nuevo_destino:
            self.reiniciar()
            return
        nueva_pregunta = simpledialog.askstring("Aprender", f"Escribe una pregunta de SÍ/NO para diferenciar '{nuevo_destino}' de '{viejo_resultado_nodo.resultado}'.")
        if not nueva_pregunta:
            self.reiniciar()
            return
        respuesta_para_nuevo_destino = messagebox.askquestion("Aprender", f"Para la pregunta '{nueva_pregunta}', la respuesta para '{nuevo_destino}' es 'Sí' o 'No'?")
        viejo_resultado_nodo.pregunta, viejo_resultado_valor = nueva_pregunta, viejo_resultado_nodo.resultado
        viejo_resultado_nodo.resultado = None
        nuevo_nodo_destino = NodoDecision(resultado=nuevo_destino)
        viejo_nodo_resultado = NodoDecision(resultado=viejo_resultado_valor)
        if respuesta_para_nuevo_destino == 'yes':
            viejo_resultado_nodo.si, viejo_resultado_nodo.no = nuevo_nodo_destino, viejo_nodo_resultado
        else:
            viejo_resultado_nodo.no, viejo_resultado_nodo.si = nuevo_nodo_destino, viejo_nodo_resultado
        messagebox.showinfo("¡Gracias!", f"¡He aprendido sobre '{nuevo_destino}'! Reiniciando.")
        self.reiniciar()

    def reiniciar(self):
        self.nodo_actual = self.arbol_raiz
        self.game_over = False
        self._recalcular_y_dibujar_todo()

    def run(self):
        """Bucle principal del programa, modificado para guardar al salir."""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False # Termina el bucle en lugar de salir directamente
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Router de clics para todos los botones
                    if not self.game_over:
                        if self.buttons['si'].collidepoint(event.pos): self._manejar_respuesta(True)
                        elif self.buttons['no'].collidepoint(event.pos): self._manejar_respuesta(False)
                    if self.buttons['guardar'].collidepoint(event.pos): self._guardar_arbol()
                    if self.buttons['resetear'].collidepoint(event.pos): self._resetear_arbol()

        # --- Se ejecuta JUSTO ANTES de cerrar ---
        self._guardar_arbol() # Guarda el árbol automáticamente al cerrar la ventana.
        pygame.quit()
        sys.exit()

# =========================================================================================
# --- SECCIÓN 3: Punto de Entrada del Programa (Modificado para Cargar) ---
# =========================================================================================
if __name__ == '__main__':
    # 1. Intenta cargar el árbol desde el archivo. Si no puede, crea uno nuevo.
    arbol_base = cargar_arbol()
    # 2. Crea el visualizador con el árbol cargado o nuevo.
    juego = VisualizadorArbolDecision(arbol_base)
    # 3. Inicia el programa.
    juego.run()
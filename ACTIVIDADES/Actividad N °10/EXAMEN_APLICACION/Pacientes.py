import pygame
import sys
import time

# --- 1. CONFIGURACIÓN INICIAL Y CLASES DE LÓGICA (MODELO) ---
# Lógica de la lista enlazada, completamente independiente de Pygame.

class NodoPaciente:
    """Cada nodo de la lista contiene un paciente y un puntero al siguiente."""
    def __init__(self, id_paciente, nombre, edad, prioridad):
        self.id = id_paciente
        self.paciente_info = {
            "nombre": nombre,
            "edad": edad,
            "prioridad": prioridad
        }
        self.siguiente = None

# REEMPLAZA LA CLASE GestionPacientesFIFO CON ESTA:
class GestionPacientesPrioridad:
    """
    Sistema que gestiona pacientes usando dos colas (una para cada prioridad)
    para asegurar que los 'Urgentes' sean atendidos primero.
    """
    def __init__(self):
        # Dos colas separadas, una para cada prioridad
        self.urgente_cabeza = None
        self.urgente_cola = None
        self.normal_cabeza = None
        self.normal_cola = None
        self.total_pacientes = 0
        self.id_counter = 0

    def agregar_paciente(self, nombre, edad, prioridad):
        """Agrega un paciente a la cola que le corresponde según su prioridad."""
        self.id_counter += 1
        nuevo_nodo = NodoPaciente(self.id_counter, nombre, edad, prioridad)
        self.total_pacientes += 1

        if prioridad == 'Urgente':
            if self.urgente_cabeza is None: # Si la cola de urgentes está vacía
                self.urgente_cabeza = nuevo_nodo
                self.urgente_cola = nuevo_nodo
            else:
                self.urgente_cola.siguiente = nuevo_nodo
                self.urgente_cola = nuevo_nodo
        else: # Prioridad 'Normal'
            if self.normal_cabeza is None: # Si la cola de normales está vacía
                self.normal_cabeza = nuevo_nodo
                self.normal_cola = nuevo_nodo
            else:
                self.normal_cola.siguiente = nuevo_nodo
                self.normal_cola = nuevo_nodo
        return nuevo_nodo

    def atender_paciente(self):
        """
        Atiende al siguiente paciente. Revisa primero la cola de urgentes.
        Si está vacía, atiende de la cola de normales.
        """
        if self.esta_vacia():
            return None

        self.total_pacientes -= 1
        nodo_atendido = None

        # Primero, intenta atender de la cola de urgentes
        if self.urgente_cabeza is not None:
            nodo_atendido = self.urgente_cabeza
            self.urgente_cabeza = self.urgente_cabeza.siguiente
            if self.urgente_cabeza is None:
                self.urgente_cola = None # La cola de urgentes quedó vacía
        # Si no hay urgentes, atiende de la cola normal
        elif self.normal_cabeza is not None:
            nodo_atendido = self.normal_cabeza
            self.normal_cabeza = self.normal_cabeza.siguiente
            if self.normal_cabeza is None:
                self.normal_cola = None # La cola de normales quedó vacía
        
        return nodo_atendido

    def esta_vacia(self):
        return self.total_pacientes == 0

    def obtener_pacientes_en_orden(self):
        """
        Generador para iterar sobre los pacientes en el orden de visualización
        (Urgentes primero, luego normales). Esencial para la interfaz gráfica.
        """
        actual = self.urgente_cabeza
        while actual:
            yield actual
            actual = actual.siguiente
        
        actual = self.normal_cabeza
        while actual:
            yield actual
            actual = actual.siguiente

# --- 2. CONFIGURACIÓN DE PYGAME Y ELEMENTOS VISUALES (VISTA Y CONTROLADOR) ---
pygame.init()

# Dimensiones de la pantalla
ANCHO, ALTO = 1280, 720
PANTALLA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Sistema de Gestión de Pacientes FIFO - Visualizador")

# Paleta de colores
COLORES = {
    'fondo': (240, 245, 249),
    'panel': (255, 255, 255),
    'sombra': (210, 218, 226),
    'texto_principal': (33, 47, 60),
    'texto_secundario': (93, 109, 126),
    'acento': (52, 152, 219),
    'acento_oscuro': (41, 128, 185),
    'urgente': (231, 76, 60),
    'normal': (46, 204, 113),
    'input_fondo': (236, 240, 241),
    'borde': (200, 208, 216), # <-- AÑADE ESTA LÍNEA
}

# Fuentes
FONT_TITULO = pygame.font.SysFont('Segoe UI', 32, bold=True)
FONT_SUBTITULO = pygame.font.SysFont('Segoe UI', 20, bold=True)
FONT_NORMAL = pygame.font.SysFont('Segoe UI', 16)
FONT_ETIQUETA = pygame.font.SysFont('Segoe UI', 14, bold=True)
FONT_PACIENTE = pygame.font.SysFont('Segoe UI', 15)
FONT_PACIENTE_BOLD = pygame.font.SysFont('Segoe UI', 16, bold=True)


# --- CLASES PARA COMPONENTES DE LA INTERFAZ ---

class PacienteVisual:
    """Representa la tarjeta gráfica de un paciente."""
    def __init__(self, nodo_logico):
        self.nodo_logico = nodo_logico
        self.ancho, self.alto = 200, 80
        self.pos = pygame.Vector2(ANCHO, ALTO * 0.4) # Inicia fuera de la pantalla
        self.target_pos = pygame.Vector2(0, 0)
        self.color_borde = COLORES['urgente'] if nodo_logico.paciente_info['prioridad'] == 'Urgente' else COLORES['normal']

    def update(self, dt):
        # Movimiento suave hacia la posición objetivo
        self.pos = self.pos.lerp(self.target_pos, min(dt * 8, 1))

    def draw(self, surface):
        rect = pygame.Rect(self.pos.x, self.pos.y, self.ancho, self.alto)
        
        # Sombra
        sombra_rect = rect.copy()
        sombra_rect.topleft += pygame.Vector2(4, 4)
        pygame.draw.rect(surface, COLORES['sombra'], sombra_rect, border_radius=12)

        # Tarjeta principal
        pygame.draw.rect(surface, COLORES['panel'], rect, border_radius=12)
        pygame.draw.rect(surface, self.color_borde, rect, width=3, border_radius=12)

        # Información del paciente
        info = self.nodo_logico.paciente_info
        nombre_surf = FONT_PACIENTE_BOLD.render(info['nombre'], True, COLORES['texto_principal'])
        edad_surf = FONT_PACIENTE.render(f"Edad: {info['edad']}", True, COLORES['texto_secundario'])
        prioridad_surf = FONT_PACIENTE.render(f"Prioridad: {info['prioridad']}", True, self.color_borde)

        surface.blit(nombre_surf, (self.pos.x + 15, self.pos.y + 10))
        surface.blit(edad_surf, (self.pos.x + 15, self.pos.y + 35))
        surface.blit(prioridad_surf, (self.pos.x + 15, self.pos.y + 55))

class InputBox:
    """Componente para campos de texto."""
    def __init__(self, x, y, w, h, font, texto_guia=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.font = font
        self.color_inactivo = COLORES['borde']
        self.color_activo = COLORES['acento']
        self.color = self.color_inactivo
        self.texto = ''
        self.texto_guia = texto_guia
        self.activo = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.activo = self.rect.collidepoint(event.pos)
            self.color = self.color_activo if self.activo else self.color_inactivo
        if event.type == pygame.KEYDOWN and self.activo:
            if event.key == pygame.K_BACKSPACE:
                self.texto = self.texto[:-1]
            else:
                self.texto += event.unicode

    def draw(self, screen):
        pygame.draw.rect(screen, COLORES['input_fondo'], self.rect, border_radius=8)
        pygame.draw.rect(screen, self.color, self.rect, 2, border_radius=8)
        
        if self.texto == '' and not self.activo:
            texto_surf = self.font.render(self.texto_guia, True, COLORES['texto_secundario'])
        else:
            texto_surf = self.font.render(self.texto, True, COLORES['texto_principal'])
        
        screen.blit(texto_surf, (self.rect.x + 10, self.rect.y + (self.rect.h - texto_surf.get_height()) / 2))

class Button:
    """Componente para botones."""
    def __init__(self, x, y, w, h, texto, font, color_base, color_hover):
        self.rect = pygame.Rect(x, y, w, h)
        self.texto = texto
        self.font = font
        self.color_base = color_base
        self.color_hover = color_hover
        self.color_actual = color_base
        self.elevacion = 4
        self.rect_sombra = pygame.Rect(x, y + self.elevacion, w, h)

    def draw(self, screen):
        # Sombra
        pygame.draw.rect(screen, COLORES['sombra'], self.rect_sombra, border_radius=12)
        # Botón
        pygame.draw.rect(screen, self.color_actual, self.rect, border_radius=12)
        
        texto_surf = self.font.render(self.texto, True, (255, 255, 255))
        texto_rect = texto_surf.get_rect(center=self.rect.center)
        screen.blit(texto_surf, texto_rect)

    def handle_event(self, event):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.color_actual = self.color_hover
            if event.type == pygame.MOUSEBUTTONDOWN:
                return True
        else:
            self.color_actual = self.color_base
        return False

# --- 3. CLASE PRINCIPAL DE LA APLICACIÓN ---

class App:
    def __init__(self):
        self.reloj = pygame.time.Clock()
        self.logica = GestionPacientesPrioridad()
        self.pacientes_visuales = {} # Diccionario: id_nodo -> objeto PacienteVisual
        
        # Crear componentes de la UI
        self.input_nombre = InputBox(50, 200, 280, 40, FONT_NORMAL, "Nombre del paciente")
        self.input_edad = InputBox(50, 280, 280, 40, FONT_NORMAL, "Edad")
        self.btn_agregar = Button(50, 450, 280, 50, "Agregar Paciente", FONT_SUBTITULO, COLORES['acento'], COLORES['acento_oscuro'])
        self.btn_atender = Button(50, 520, 280, 50, "Atender Siguiente", FONT_SUBTITULO, COLORES['normal'], (39, 174, 96))
        self.prioridad_actual = 'Normal'
        self.switch_rect = pygame.Rect(50, 360, 120, 40)
        
        self.lista_inputs = [self.input_nombre, self.input_edad]
        self.paciente_atendido_vis = None
        self.atendido_fade_alpha = 255

    # REEMPLAZA ESTE MÉTODO COMPLETO EN LA CLASE App
    def recalcular_posiciones_cola(self):
        """Actualiza la posición objetivo de cada tarjeta de paciente en la cola."""
        x_inicial, y_pos = 400, ALTO * 0.4
        espaciado = 220

        # Usamos el nuevo generador para obtener los nodos en el orden correcto de visualización
        for i, nodo_actual_logico in enumerate(self.logica.obtener_pacientes_en_orden()):
            if nodo_actual_logico.id in self.pacientes_visuales:
                vis = self.pacientes_visuales[nodo_actual_logico.id]
                vis.target_pos = pygame.Vector2(x_inicial + i * espaciado, y_pos)

    def manejar_eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            for box in self.lista_inputs:
                box.handle_event(event)

            if self.btn_agregar.handle_event(event):
                nombre = self.input_nombre.texto
                edad = self.input_edad.texto
                if nombre and edad.isdigit():
                    nuevo_nodo = self.logica.agregar_paciente(nombre, int(edad), self.prioridad_actual)
                    self.pacientes_visuales[nuevo_nodo.id] = PacienteVisual(nuevo_nodo)
                    self.recalcular_posiciones_cola()
                    self.input_nombre.texto = ''
                    self.input_edad.texto = ''
            
            if self.btn_atender.handle_event(event):
                nodo_atendido = self.logica.atender_paciente()
                if nodo_atendido:
                    self.paciente_atendido_vis = self.pacientes_visuales.pop(nodo_atendido.id)
                    self.paciente_atendido_vis.target_pos = pygame.Vector2(-300, ALTO * 0.4)
                    self.atendido_fade_alpha = 255
                    self.recalcular_posiciones_cola()

            if event.type == pygame.MOUSEBUTTONDOWN and self.switch_rect.collidepoint(event.pos):
                self.prioridad_actual = 'Urgente' if self.prioridad_actual == 'Normal' else 'Normal'

    def actualizar(self, dt):
        for vis in list(self.pacientes_visuales.values()):
            vis.update(dt)
        
        if self.paciente_atendido_vis:
            self.paciente_atendido_vis.update(dt)
            if self.paciente_atendido_vis.pos.x < -250:
                self.paciente_atendido_vis = None


    def dibujar_panel_control(self):
        # Panel
        pygame.draw.rect(PANTALLA, COLORES['panel'], (0, 0, 380, ALTO))
        pygame.draw.line(PANTALLA, COLORES['sombra'], (380, 0), (380, ALTO), 2)

        # Títulos
        titulo_surf = FONT_TITULO.render("Panel de Control", True, COLORES['texto_principal'])
        PANTALLA.blit(titulo_surf, (50, 50))
        subtitulo_surf = FONT_SUBTITULO.render("Registro de Pacientes", True, COLORES['texto_secundario'])
        PANTALLA.blit(subtitulo_surf, (50, 100))
        
        # Etiquetas
        PANTALLA.blit(FONT_ETIQUETA.render("NOMBRE COMPLETO", True, COLORES['texto_secundario']), (50, 175))
        PANTALLA.blit(FONT_ETIQUETA.render("EDAD", True, COLORES['texto_secundario']), (50, 255))
        PANTALLA.blit(FONT_ETIQUETA.render("PRIORIDAD", True, COLORES['texto_secundario']), (50, 335))

        # Dibujar inputs y botones
        for box in self.lista_inputs:
            box.draw(PANTALLA)
        self.btn_agregar.draw(PANTALLA)
        self.btn_atender.draw(PANTALLA)
        
        # Dibujar switch de prioridad
        pygame.draw.rect(PANTALLA, COLORES['input_fondo'], self.switch_rect, border_radius=20)
        if self.prioridad_actual == 'Normal':
            pygame.draw.circle(PANTALLA, COLORES['normal'], (self.switch_rect.left + 20, self.switch_rect.centery), 16)
            texto = FONT_NORMAL.render("Normal", True, COLORES['texto_principal'])
        else:
            pygame.draw.circle(PANTALLA, COLORES['urgente'], (self.switch_rect.right - 20, self.switch_rect.centery), 16)
            texto = FONT_NORMAL.render("Urgente", True, COLORES['texto_principal'])
        PANTALLA.blit(texto, texto.get_rect(center=(self.switch_rect.centerx + 20, self.switch_rect.centery)))


    def dibujar_area_visualizacion(self):
        # Título del área
        titulo_surf = FONT_TITULO.render("Fila de Pacientes ", True, COLORES['texto_principal'])
        PANTALLA.blit(titulo_surf, (420, 50))

        # Contador de pacientes
        contador_texto = f"Pacientes en espera: {self.logica.total_pacientes}"
        contador_surf = FONT_SUBTITULO.render(contador_texto, True, COLORES['texto_secundario'])
        PANTALLA.blit(contador_surf, (420, 100))

        # Indicador de "Atendiendo"
        # Solo se muestra si hay al menos un paciente en la fila
        if not self.logica.esta_vacia():
            atendiendo_surf = FONT_SUBTITULO.render("-> Atendiendo", True, COLORES['acento'])
            PANTALLA.blit(atendiendo_surf, (420, ALTO * 0.4 + 90))

        # Dibujar pacientes en la cola
        for vis in self.pacientes_visuales.values():
            vis.draw(PANTALLA)
            
        # Dibujar paciente que está siendo atendido
        if self.paciente_atendido_vis:
            self.paciente_atendido_vis.draw(PANTALLA)


    def run(self):
        """Bucle principal de la aplicación."""
        last_time = time.time()
        while True:
            # Delta time para animaciones fluidas e independientes del framerate
            dt = time.time() - last_time
            last_time = time.time()

            self.manejar_eventos()
            self.actualizar(dt)

            PANTALLA.fill(COLORES['fondo'])
            self.dibujar_area_visualizacion()
            self.dibujar_panel_control()
            
            pygame.display.flip()
            self.reloj.tick(60)

if __name__ == '__main__':
    app = App()
    app.run()

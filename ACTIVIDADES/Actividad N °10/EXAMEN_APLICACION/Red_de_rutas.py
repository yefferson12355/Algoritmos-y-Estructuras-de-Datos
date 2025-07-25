import pygame
import heapq
import math
import random
import os

# --- 1. CONFIGURACIÓN ---
pygame.init()

# Paleta de colores profesional
COLORES = {
    'fondo': (245, 245, 248),
    'panel': (235, 235, 240),
    'sombra': (210, 210, 215),
    'texto': (20, 20, 35),
    'borde': (60, 60, 70),
    'ciudad_base': (44, 62, 80),
    'ciudad_borde': (52, 73, 94),
    'ciudad_texto': (236, 240, 241),
    'ruta': (149, 165, 166),
    'ruta_optima': (231, 76, 60),
    'boton_base': (52, 152, 219),
    'boton_texto': (255, 255, 255),
    'input_activo_borde': (52, 152, 219),
    'input_fondo': (255, 255, 255),
}

# Archivo de persistencia
ARCHIVO_RUTAS = "actualizacion.txt"

# --- 2. CLASE DE LÓGICA DEL GRAFO (MODELO) ---
class Grafo:
    """Representa un grafo dirigido y ponderado."""
    def __init__(self):
        self.adj = {}

    def agregar_nodo(self, nodo):
        """Asegura que un nodo (ciudad) exista en el grafo. Punto único de creación."""
        if nodo not in self.adj:
            self.adj[nodo] = []

    def agregar_ruta(self, origen, destino, peso):
        # Asegura que ambos nodos existan antes de añadir la arista
        self.agregar_nodo(origen)
        self.agregar_nodo(destino)

        for i, (vecino, _) in enumerate(self.adj[origen]):
            if vecino == destino:
                self.adj[origen][i] = (destino, peso)
                return
        self.adj[origen].append((destino, peso))

    def dijkstra(self, ciudad_inicio):
        distancias = {c: float('inf') for c in self.adj}
        if ciudad_inicio not in distancias: return {}, {}
        distancias[ciudad_inicio] = 0
        padres = {c: None for c in self.adj}
        cola_prioridad = [(0, ciudad_inicio)]

        while cola_prioridad:
            dist, actual = heapq.heappop(cola_prioridad)
            if dist > distancias[actual]: continue
            for vecino, peso in self.adj.get(actual, []):
                if distancias[actual] + peso < distancias[vecino]:
                    distancias[vecino] = distancias[actual] + peso
                    padres[vecino] = actual
                    heapq.heappush(cola_prioridad, (distancias[vecino], vecino))
        return distancias, padres

# --- 3. CLASES DE COMPONENTES DE LA INTERFAZ (VISTA/CONTROLADOR) ---
class Ciudad:
    """Representa una ciudad con posición en el 'mundo'."""
    def __init__(self, nombre, x, y):
        self.nombre = nombre
        self.world_pos = pygame.math.Vector2(x, y)

    def draw(self, screen, cam, fonts, es_ruta=False, es_seleccionada=False):
        screen_pos = cam.world_to_screen(self.world_pos)
        radius = int(25 * cam.zoom)

        if not (-radius < screen_pos.x < screen.get_width() + radius and \
                -radius < screen_pos.y < screen.get_height() + radius):
            return

        color_base = COLORES['ruta_optima'] if es_ruta else COLORES['ciudad_base']
        color_borde = COLORES['ciudad_borde']

        pygame.draw.circle(screen, color_borde, screen_pos, radius)
        pygame.draw.circle(screen, color_base, screen_pos, int(radius * 0.9))

        if es_seleccionada:
            pygame.draw.circle(screen, COLORES['boton_base'], screen_pos, int(radius * 1.1), max(1, int(3 * cam.zoom)))

        if cam.zoom > 0.3:
            try:
                font_size = max(8, int(15 * cam.zoom))
                dynamic_font = fonts.get(f'ciudad_{font_size}', fonts['ciudad_default'])
                texto_surf = dynamic_font.render(self.nombre, True, COLORES['ciudad_texto'])
                texto_rect = texto_surf.get_rect(center=screen_pos)
                screen.blit(texto_surf, texto_rect)
            except Exception as e:
                print(f"Error al renderizar fuente de ciudad: {e}")

    def get_screen_rect(self, cam):
        screen_pos = cam.world_to_screen(self.world_pos)
        radius = int(25 * cam.zoom)
        return pygame.Rect(screen_pos.x - radius, screen_pos.y - radius, radius * 2, radius * 2)

class Button:
    def __init__(self, x, y, w, h, texto, font):
        self.rect = pygame.Rect(x, y, w, h)
        self.texto = texto
        self.font = font
    def draw(self, screen):
        pygame.draw.rect(screen, COLORES['boton_base'], self.rect, border_radius=8)
        texto_surf = self.font.render(self.texto, True, COLORES['boton_texto'])
        screen.blit(texto_surf, texto_surf.get_rect(center=self.rect.center))

class InputField:
    def __init__(self, x, y, w, h, font):
        self.rect = pygame.Rect(x, y, w, h)
        self.texto = ""
        self.activo = False
        self.font = font
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and self.activo:
            if event.key == pygame.K_BACKSPACE: self.texto = self.texto[:-1]
            else: self.texto += event.unicode
    def draw(self, screen):
        pygame.draw.rect(screen, COLORES['input_fondo'], self.rect, border_radius=5)
        borde_color = COLORES['input_activo_borde'] if self.activo else COLORES['borde']
        pygame.draw.rect(screen, borde_color, self.rect, width=2, border_radius=5)
        texto_surf = self.font.render(self.texto, True, COLORES['texto'])
        screen.blit(texto_surf, (self.rect.x + 10, self.rect.y + 8))

class Camera:
    """Maneja el zoom y el desplazamiento del mapa."""
    def __init__(self, width, height):
        self.offset = pygame.math.Vector2(-150, -100)
        self.zoom = 0.7
        self.width = width
        self.height = height

    def world_to_screen(self, world_pos):
        return (world_pos + self.offset) * self.zoom

    def screen_to_world(self, screen_pos):
        return (pygame.math.Vector2(screen_pos) / self.zoom) - self.offset

    def handle_event(self, event, mouse_pos):
        if event.type == pygame.MOUSEWHEEL:
            self.zoom_on_point(event.y, mouse_pos)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS: self.zoom_on_point(1, (self.width/2, self.height/2))
            if event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS: self.zoom_on_point(-1, (self.width/2, self.height/2))

    def zoom_on_point(self, amount, point):
        world_point_before_zoom = self.screen_to_world(point)
        self.zoom = max(0.2, min(3.0, self.zoom + amount * 0.05))
        world_point_after_zoom = self.screen_to_world(point)
        self.offset += world_point_before_zoom - world_point_after_zoom

# --- 4. CLASE PRINCIPAL DE LA APLICACIÓN ---
class AppRutasPygame:
    def __init__(self):
        self.screen_width, self.screen_height = 1280, 800
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Sistema Profesional de Rutas (v3.4 - Lógica Corregida)")
        self.clock = pygame.time.Clock()
        self.grafo = Grafo()
        self.camera = Camera(self.screen_width - 300, self.screen_height)

        self._cargar_fuentes()

        self.ciudades = {}
        self.origen_seleccionado = None
        self.destino_seleccionado = None

        self._inicializar_mapa_y_rutas_base()
        self._cargar_rutas_desde_archivo()
        self._crear_ui()

        self.ruta_optima = []
        self.distancia_total = 0

        self.active_input = None
        self.panning = False
        self.pan_start_pos = pygame.math.Vector2(0, 0)

    def _cargar_fuentes(self):
        """Carga todas las fuentes necesarias una sola vez al inicio."""
        self.fonts = {
            'ui': pygame.font.SysFont('Segoe UI', 18),
            'resultado': pygame.font.SysFont('Segoe UI', 16),
            'titulo': pygame.font.SysFont('Segoe UI', 22, bold=True),
            'ciudad_default': pygame.font.SysFont('Segoe UI', 15, bold=True)
        }
        for size in range(8, 31):
            self.fonts[f'ciudad_{size}'] = pygame.font.SysFont('Segoe UI', size, bold=True)
            self.fonts[f'peso_{size}'] = pygame.font.SysFont('Segoe UI', size)

    def _inicializar_mapa_y_rutas_base(self):
        """Crea las ciudades con sus posiciones y añade las rutas iniciales al grafo."""
        self.posiciones_ciudades = {
            "Lima": (300, 450), "Puno": (880, 700), "Cusco": (730, 580),
            "Arequipa": (680, 750), "Iquitos": (650, 150), "Piura": (250, 100),
            "Trujillo": (280, 250), "Tacna": (780, 800)
        }
        # Asegurarse de que todas las ciudades base existan en el grafo y en la UI
        for nombre, pos in self.posiciones_ciudades.items():
            self.ciudades[nombre] = Ciudad(nombre, pos[0], pos[1])
            self.grafo.agregar_nodo(nombre) # <-- Usando el método centralizado
            
        rutas_base = [
            ("Lima", "Trujillo", 560), ("Trujillo", "Piura", 480), ("Lima", "Iquitos", 1015),
            ("Lima", "Arequipa", 1030), ("Arequipa", "Lima", 1030), ("Cusco", "Lima", 1100),
            ("Arequipa", "Cusco", 625), ("Puno", "Cusco", 390), ("Arequipa", "Puno", 290),
            ("Tacna", "Arequipa", 370),
        ]
        for origen, destino, peso in rutas_base:
            self.grafo.agregar_ruta(origen, destino, peso)

    def _cargar_rutas_desde_archivo(self):
        if not os.path.exists(ARCHIVO_RUTAS): return

        with open(ARCHIVO_RUTAS, 'r') as f:
            for linea in f:
                try:
                    origen, destino, peso_str = linea.strip().split(',')
                    self._agregar_o_actualizar_ruta(origen, destino, int(peso_str), guardar=False)
                except (ValueError, IndexError):
                    print(f"Línea mal formada en {ARCHIVO_RUTAS}: {linea.strip()}")

    def _guardar_ruta_en_archivo(self, origen, destino, peso):
        with open(ARCHIVO_RUTAS, 'a') as f:
            f.write(f"{origen},{destino},{peso}\n")

    def _crear_ui(self):
        panel_x = self.screen_width - 280
        self.btn_calcular = Button(panel_x, 150, 260, 40, "Calcular Ruta Más Corta", self.fonts['ui'])
        self.input_origen_add = InputField(panel_x + 80, 300, 180, 35, self.fonts['ui'])
        self.input_destino_add = InputField(panel_x + 80, 350, 180, 35, self.fonts['ui'])
        self.input_peso_add = InputField(panel_x + 80, 400, 180, 35, self.fonts['ui'])
        self.btn_agregar = Button(panel_x, 450, 260, 40, "Agregar/Actualizar Ruta", self.fonts['ui'])
        self.all_inputs = [self.input_origen_add, self.input_destino_add, self.input_peso_add]

    def run(self):
        running = True
        while running:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT: running = False
                self.camera.handle_event(event, mouse_pos)
                if self.active_input: self.active_input.handle_event(event)
                self._handle_mouse_events(event, mouse_pos)
            self.draw()
            self.clock.tick(60)
        pygame.quit()

    def _handle_mouse_events(self, event, mouse_pos):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button in [2, 3]: # Pan
                self.panning = True
                self.pan_start_pos = pygame.math.Vector2(mouse_pos)
            if event.button == 1:
                self.active_input = None
                for i_field in self.all_inputs:
                    i_field.activo = False
                    if i_field.rect.collidepoint(mouse_pos):
                        i_field.activo = True
                        self.active_input = i_field
                if not self.active_input:
                    self._handle_clicks_on_map_and_buttons(mouse_pos)
        if event.type == pygame.MOUSEBUTTONUP and event.button in [2, 3]: self.panning = False
        if event.type == pygame.MOUSEMOTION and self.panning:
            delta = pygame.math.Vector2(mouse_pos) - self.pan_start_pos
            self.camera.offset += delta / self.camera.zoom
            self.pan_start_pos = pygame.math.Vector2(mouse_pos)

    def _handle_clicks_on_map_and_buttons(self, pos):
        if self.btn_calcular.rect.collidepoint(pos): self.ejecutar_dijkstra()
        elif self.btn_agregar.rect.collidepoint(pos): self.procesar_nueva_ruta()

        clicked_city_name = None
        for nombre, ciudad in self.ciudades.items():
            if ciudad.get_screen_rect(self.camera).collidepoint(pos):
                clicked_city_name = nombre
                break
        if clicked_city_name:
            if not self.origen_seleccionado or self.destino_seleccionado:
                self.origen_seleccionado = clicked_city_name
                self.destino_seleccionado = None
            elif clicked_city_name != self.origen_seleccionado:
                self.destino_seleccionado = clicked_city_name
            self.ruta_optima = []
            self.distancia_total = 0

    def ejecutar_dijkstra(self):
        if not self.origen_seleccionado or not self.destino_seleccionado: return
        distancias, padres = self.grafo.dijkstra(self.origen_seleccionado)
        if distancias.get(self.destino_seleccionado, float('inf')) == float('inf'):
            self.ruta_optima, self.distancia_total = [], "No existe ruta"
        else:
            camino = []; paso = self.destino_seleccionado
            while paso is not None: camino.append(paso); paso = padres.get(paso)
            self.ruta_optima, self.distancia_total = camino[::-1], distancias[self.destino_seleccionado]

    def procesar_nueva_ruta(self):
        origen = self.input_origen_add.texto.strip().title()
        destino = self.input_destino_add.texto.strip().title()
        peso_str = self.input_peso_add.texto.strip()
        if origen and destino and peso_str.isdigit():
            self._agregar_o_actualizar_ruta(origen, destino, int(peso_str), guardar=True)
            for i in self.all_inputs: i.texto = ""

    def _agregar_o_actualizar_ruta(self, origen, destino, peso, guardar=False):
        # --- ESTA ES LA CORRECCIÓN CRUCIAL ---
        # Registra la ciudad en el grafo LÓGICO antes de hacer cualquier otra cosa.
        self.grafo.agregar_nodo(origen)
        self.grafo.agregar_nodo(destino)

        # Ahora, crea la ciudad en la UI si no existe para dibujarla
        if origen not in self.ciudades:
            new_pos = self.camera.screen_to_world((random.randint(200, 600), random.randint(200, 600)))
            self.ciudades[origen] = Ciudad(origen, new_pos.x, new_pos.y)
        if destino not in self.ciudades:
            new_pos = self.camera.screen_to_world((random.randint(200, 600), random.randint(200, 600)))
            self.ciudades[destino] = Ciudad(destino, new_pos.x, new_pos.y)
        
        # Finalmente, agrega la ruta
        self.grafo.agregar_ruta(origen, destino, peso)
        
        if guardar: 
            self._guardar_ruta_en_archivo(origen, destino, peso)

    def _draw_flecha(self, p1, p2, color, grosor):
        grosor_real = max(1, int(grosor * self.camera.zoom))
        try:
            pygame.draw.line(self.screen, color, p1, p2, grosor_real)
            angle = math.atan2(p1.y - p2.y, p1.x - p2.x)
            arrow_size = 10 * self.camera.zoom
            if arrow_size > 1:
                p3 = (p2.x + arrow_size * math.cos(angle - math.pi / 6), p2.y - arrow_size * math.sin(angle - math.pi / 6))
                p4 = (p2.x + arrow_size * math.cos(angle + math.pi / 6), p2.y - arrow_size * math.sin(angle + math.pi / 6))
                pygame.draw.polygon(self.screen, color, [p2, p3, p4])
        except Exception:
            pass

    def draw(self):
        self.screen.fill(COLORES['fondo'])
        
        # Dibujar elementos del mapa
        for origen, destinos in self.grafo.adj.items():
            for destino, peso in destinos:
                if origen in self.ciudades and destino in self.ciudades:
                    p1 = self.camera.world_to_screen(self.ciudades[origen].world_pos)
                    p2 = self.camera.world_to_screen(self.ciudades[destino].world_pos)
                    self._draw_flecha(p1, p2, COLORES['ruta'], 2)
                    if self.camera.zoom > 0.4:
                        font_size = max(8, int(14 * self.camera.zoom))
                        dynamic_font = self.fonts.get(f'peso_{font_size}', self.fonts['ui'])
                        self.screen.blit(dynamic_font.render(str(peso), True, COLORES['borde']), (p1 + p2) / 2)

        if len(self.ruta_optima) > 1:
            for i in range(len(self.ruta_optima) - 1):
                p1 = self.camera.world_to_screen(self.ciudades[self.ruta_optima[i]].world_pos)
                p2 = self.camera.world_to_screen(self.ciudades[self.ruta_optima[i+1]].world_pos)
                self._draw_flecha(p1, p2, COLORES['ruta_optima'], 4)
        
        for nombre, ciudad in self.ciudades.items():
            es_ruta = nombre in self.ruta_optima
            es_sel = nombre == self.origen_seleccionado or nombre == self.destino_seleccionado
            ciudad.draw(self.screen, self.camera, self.fonts, es_ruta, es_sel)
            
        # Dibujar panel de UI
        panel_x = self.screen_width - 300
        pygame.draw.rect(self.screen, COLORES['sombra'], (panel_x+4, 4, 292, self.screen_height-8), border_radius=10)
        pygame.draw.rect(self.screen, COLORES['panel'], (panel_x, 0, 300, self.screen_height), border_radius=10)
        
        # Textos y elementos del panel
        font_titulo = self.fonts['titulo']
        font_ui = self.fonts['ui']
        font_resultado = self.fonts['resultado']
        
        self.screen.blit(font_titulo.render("Panel de Control", True, COLORES['texto']), (panel_x + 50, 20))
        self.screen.blit(font_ui.render(f"Origen: {self.origen_seleccionado or '...'}", True, COLORES['texto']), (panel_x + 20, 80))
        self.screen.blit(font_ui.render(f"Destino: {self.destino_seleccionado or '...'}", True, COLORES['texto']), (panel_x + 20, 110))
        self.btn_calcular.draw(self.screen)
        
        self.screen.blit(font_titulo.render("Añadir Ruta", True, COLORES['texto']), (panel_x + 75, 250))
        self.screen.blit(font_ui.render("Origen:", True, COLORES['texto']), (panel_x + 20, 308))
        self.screen.blit(font_ui.render("Destino:", True, COLORES['texto']), (panel_x + 20, 358))
        self.screen.blit(font_ui.render("Peso:", True, COLORES['texto']), (panel_x + 20, 408))
        for input_field in self.all_inputs: input_field.draw(self.screen)
        self.btn_agregar.draw(self.screen)

        # Resultado
        if self.ruta_optima:
            self.screen.blit(font_titulo.render("Resultado", True, COLORES['texto']), (panel_x + 85, 550))
            camino_str = " -> ".join(self.ruta_optima)
            dist_str = f"Distancia Total: {self.distancia_total} km"
            
            line_y = 600
            line_height = font_resultado.get_height() + 5
            max_width = 260
            
            words = camino_str.split(' ')
            line = ""
            for word in words:
                if font_resultado.size(line + word)[0] < max_width: line += word + " "
                else:
                    self.screen.blit(font_resultado.render(line, True, COLORES['texto']), (panel_x+20, line_y))
                    line_y += line_height
                    line = word + " "
            self.screen.blit(font_resultado.render(line, True, COLORES['texto']), (panel_x+20, line_y))
            line_y += line_height * 1.5
            self.screen.blit(font_resultado.render(dist_str, True, COLORES['texto']), (panel_x+20, line_y))

        pygame.display.flip()

if __name__ == '__main__':
    app = AppRutasPygame()
    app.run()
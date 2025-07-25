import pygame
import sys
import time
import math

# --- 1. CONFIGURACIÓN GLOBAL Y CONSTANTES ---
# Se definen aquí para fácil acceso y modificación.

pygame.init()

# Dimensiones de la pantalla
ANCHO, ALTO = 1366, 768
PANTALLA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Visualizador Avanzado de Agenda con Hashing")

# Paleta de colores moderna y limpia
COLORES = {
    'fondo': (248, 249, 250),
    'panel': (255, 255, 255),
    'sombra': (200, 200, 210, 100), # Sombra semitransparente
    'texto_principal': (33, 37, 41),
    'texto_secundario': (108, 117, 125),
    'borde': (222, 226, 230),
    'acento': (0, 123, 255),
    'acento_oscuro': (0, 86, 179),
    'exito': (40, 167, 69),
    'exito_oscuro': (28, 117, 48),
    'error': (220, 53, 69),
    'error_oscuro': (154, 37, 48),
    'info': (23, 162, 184),
    'scrollbar': (222, 226, 230),
    'scrollbar_handle': (173, 181, 189)
}

# Fuentes tipográficas para una mejor jerarquía visual
try:
    FONT_TITULO = pygame.font.SysFont('Segoe UI Variable Display', 32, bold=True)
    FONT_SUBTITULO = pygame.font.SysFont('Segoe UI Variable Text', 18, bold=True)
    FONT_NORMAL = pygame.font.SysFont('Segoe UI Variable Text', 16)
    FONT_PEQUENA = pygame.font.SysFont('Segoe UI Variable Text', 13)
    FONT_MONO = pygame.font.SysFont('Consolas', 18, bold=True)
except pygame.error:
    # Fallback a fuentes estándar si las especificadas no están disponibles
    FONT_TITULO = pygame.font.SysFont('Arial', 32, bold=True)
    FONT_SUBTITULO = pygame.font.SysFont('Arial', 18, bold=True)
    FONT_NORMAL = pygame.font.SysFont('Arial', 16)
    FONT_PEQUENA = pygame.font.SysFont('Arial', 13)
    FONT_MONO = pygame.font.SysFont('monospace', 18, bold=True)


# --- 2. CLASES DE LÓGICA (MODELO) ---
# La lógica del HashMap ahora incluye redimensionamiento (rehashing).

class NodoContacto:
    """Nodo para la lista enlazada (manejo de colisiones por encadenamiento)."""
    def __init__(self, clave, valor):
        self.clave = clave
        self.valor = valor
        self.siguiente = None

class HashMapContactos:
    """
    Implementación robusta de un HashMap que soporta:
    - Hashing por suma de valores ASCII.
    - Manejo de colisiones por encadenamiento.
    - Redimensionamiento dinámico (rehashing) cuando la carga supera un umbral.
    """
    def __init__(self, tamano_inicial=5, factor_carga_max=0.7):
        self.tamano = tamano_inicial
        self.tabla = [None] * self.tamano
        self.num_elementos = 0
        self.factor_carga_max = factor_carga_max

    def _funcion_hash(self, clave):
        """Función hash simple para convertir una clave en un índice."""
        return sum(ord(char) for char in clave) % self.tamano

    def _rehash(self):
        """
        Duplica el tamaño de la tabla y reubica todos los elementos existentes.
        Este es un proceso costoso que se activa para mantener la eficiencia.
        """
        elementos_antiguos = self.obtener_todos()
        self.tamano *= 2  # Duplicar el tamaño
        self.tabla = [None] * self.tamano
        self.num_elementos = 0
        for clave, valor in elementos_antiguos:
            self.agregar(clave, valor) # Re-insertar cada elemento en la nueva tabla

    def agregar(self, clave, valor):
        """Agrega o actualiza un par clave-valor. Dispara rehashing si es necesario."""
        # Comprobar si se necesita rehash ANTES de insertar el nuevo elemento
        if (self.num_elementos + 1) / self.tamano > self.factor_carga_max:
            self._rehash()
            # Devolvemos una señal para que la UI sepa que hubo un rehash
            return "rehash", self._funcion_hash(clave)

        indice = self._funcion_hash(clave)
        if self.tabla[indice] is None:
            self.tabla[indice] = NodoContacto(clave, valor)
            self.num_elementos += 1
            return "agregado", indice
        
        nodo_actual = self.tabla[indice]
        while True:
            if nodo_actual.clave == clave:
                nodo_actual.valor = valor # Actualiza el valor si la clave ya existe
                return "actualizado", indice
            if nodo_actual.siguiente is None:
                break
            nodo_actual = nodo_actual.siguiente
        
        nodo_actual.siguiente = NodoContacto(clave, valor)
        self.num_elementos += 1
        return "colision", indice

    def buscar(self, clave):
        """Busca un valor por su clave y devuelve su posición."""
        indice = self._funcion_hash(clave)
        nodo_actual = self.tabla[indice]
        pos_en_cadena = 0
        while nodo_actual:
            if nodo_actual.clave == clave:
                return nodo_actual.valor, indice, pos_en_cadena
            nodo_actual = nodo_actual.siguiente
            pos_en_cadena += 1
        return None, indice, -1

    def eliminar(self, clave):
        """Elimina un nodo de la tabla hash."""
        indice = self._funcion_hash(clave)
        nodo_actual = self.tabla[indice]
        nodo_previo = None

        while nodo_actual and nodo_actual.clave != clave:
            nodo_previo = nodo_actual
            nodo_actual = nodo_actual.siguiente

        if nodo_actual is None:
            return False, -1 # No se encontró

        if nodo_previo is None:
            self.tabla[indice] = nodo_actual.siguiente
        else:
            nodo_previo.siguiente = nodo_actual.siguiente
        
        self.num_elementos -= 1
        return True, indice

    def obtener_todos(self):
        """Devuelve una lista de todos los pares (clave, valor) en el mapa."""
        todos = []
        for nodo_cabeza in self.tabla:
            nodo_actual = nodo_cabeza
            while nodo_actual:
                todos.append((nodo_actual.clave, nodo_actual.valor))
                nodo_actual = nodo_actual.siguiente
        return todos

# --- 3. CLASES DE LA INTERFAZ GRÁFICA (VISTA) ---

def dibujar_texto(superficie, texto, pos, fuente, color, centrado=False, centro_rect=None):
    """Función de utilidad para dibujar texto fácilmente."""
    text_surf = fuente.render(texto, True, color)
    text_rect = text_surf.get_rect()
    if centrado:
        text_rect.center = pos
    elif centro_rect:
        text_rect.center = centro_rect.center
    else:
        text_rect.topleft = pos
    superficie.blit(text_surf, text_rect)

class ContactoVisual:
    """Representa la tarjeta gráfica de un contacto con animaciones."""
    def __init__(self, nodo_logico, pos_inicial, pos_final):
        self.nodo_logico = nodo_logico
        self.pos = pygame.Vector2(pos_inicial)
        self.target_pos = pygame.Vector2(pos_final)
        self.ancho, self.alto = 220, 80
        self.color_base = pygame.Color(COLORES['panel'])
        self.color_actual = pygame.Color(self.color_base)
        self.alpha = 0
        self.target_alpha = 255
        self.highlight_timer = 0
        self.velocidad_anim = 8 # Más alto = más rápido

    def update(self, dt):
        """Actualiza la posición, transparencia y color de la tarjeta."""
        self.pos = self.pos.lerp(self.target_pos, min(dt * self.velocidad_anim, 1))
        self.alpha += (self.target_alpha - self.alpha) * min(dt * self.velocidad_anim, 1)

        if self.highlight_timer > 0:
            self.highlight_timer -= dt
            # Crea un efecto de pulso sinusoidal para el resaltado
            t = max(0, 1 - (self.highlight_timer / 2.0)) # 2 segundos de highlight
            color_resaltado = pygame.Color(COLORES['exito'])
            self.color_actual = self.color_base.lerp(color_resaltado, abs(math.sin(t * math.pi)))
        else:
            # Vuelve suavemente al color base
            self.color_actual = self.color_actual.lerp(self.color_base, min(dt * self.velocidad_anim, 1))
    
    def draw(self, surface):
        """Dibuja la tarjeta del contacto en la pantalla."""
        if self.alpha < 5: return # No dibujar si es casi invisible

        # Superficie temporal para manejar la transparencia del grupo
        temp_surface = pygame.Surface((self.ancho, self.alto), pygame.SRCALPHA)
        
        # *** CORRECCIÓN DEL ERROR ***
        # Se crea una copia del color y se le asigna el alpha.
        # Luego, este objeto Color se pasa directamente a la función de dibujo.
        color_tarjeta = pygame.Color(self.color_actual)
        color_tarjeta.a = int(self.alpha)
        
        color_borde = pygame.Color(COLORES['borde'])
        color_borde.a = int(self.alpha)

        # Tarjeta principal
        pygame.draw.rect(temp_surface, color_tarjeta, (0, 0, self.ancho, self.alto), border_radius=12)
        # Borde
        pygame.draw.rect(temp_surface, color_borde, (0, 0, self.ancho, self.alto), 2, border_radius=12)

        # Renderizar texto solo si es suficientemente visible
        if self.alpha > 100:
            alpha_texto = int(self.alpha)
            # Copiamos los colores para no modificar el diccionario global
            color_nombre = pygame.Color(COLORES['texto_principal'])
            color_telefono = pygame.Color(COLORES['texto_secundario'])
            color_nombre.a = alpha_texto
            color_telefono.a = alpha_texto
            
            dibujar_texto(temp_surface, self.nodo_logico.clave, (18, 15), FONT_SUBTITULO, color_nombre)
            dibujar_texto(temp_surface, self.nodo_logico.valor, (18, 45), FONT_NORMAL, color_telefono)
        
        # Dibujar la sombra debajo (opcional pero da profundidad)
        sombra_surf = pygame.Surface((self.ancho, self.alto), pygame.SRCALPHA)
        pygame.draw.rect(sombra_surf, COLORES['sombra'], (0,0,self.ancho,self.alto), border_radius=12)
        surface.blit(sombra_surf, self.pos + pygame.Vector2(5, 5))

        surface.blit(temp_surface, self.pos)

class InputBox:
    """Caja de texto editable con clipping para evitar desbordamiento de texto."""
    def __init__(self, x, y, w, h, font, texto_guia=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.font = font
        self.texto = ''
        self.texto_guia = texto_guia
        self.activo = False
        self.color_borde = pygame.Color(COLORES['borde'])
        self.color_borde_activo = pygame.Color(COLORES['acento'])

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.activo = self.rect.collidepoint(event.pos)
        if event.type == pygame.KEYDOWN and self.activo:
            if event.key == pygame.K_BACKSPACE:
                self.texto = self.texto[:-1]
            elif event.key != pygame.K_RETURN: # Ignorar Enter
                self.texto += event.unicode
    
    def draw(self, screen):
        # Dibuja el fondo y el borde del input box
        color_borde = self.color_borde_activo if self.activo else self.color_borde
        pygame.draw.rect(screen, COLORES['panel'], self.rect, border_radius=8)
        pygame.draw.rect(screen, color_borde, self.rect, 2, border_radius=8)
        
        # Elige el texto y color a mostrar (placeholder o texto del usuario)
        texto_a_mostrar = self.texto if self.texto or self.activo else self.texto_guia
        color_texto = COLORES['texto_principal'] if self.texto else COLORES['texto_secundario']

        # --- SOLUCIÓN AL DESBORDAMIENTO (CLIPPING) ---
        # 1. Guarda el área de recorte actual de la pantalla
        clip_original = screen.get_clip()
        
        # 2. Define un área de recorte un poco más pequeña que el input box para el padding
        #    (dejamos 12 píxeles de margen a cada lado)
        clip_rect = self.rect.inflate(-24, -10) 
        screen.set_clip(clip_rect)

        # 3. Dibuja el texto. Se alineará a la izquierda y se centrará verticalmente.
        #    Solo la parte del texto dentro del 'clip_rect' será visible.
        text_surf = self.font.render(texto_a_mostrar, True, color_texto)
        text_rect = text_surf.get_rect(midleft=(self.rect.x + 12, self.rect.centery))
        
        # Si el texto escrito es más ancho que el área visible, lo alineamos a la derecha
        # para que siempre se vea lo último que se está tecleando.
        if text_rect.width > clip_rect.width:
             text_rect.midright = (self.rect.right - 12, self.rect.centery)

        screen.blit(text_surf, text_rect)

        # 4. Restaura el área de recorte original para no afectar a otros dibujos
        screen.set_clip(clip_original)
        
class Button:
    """Botón interactivo con cambio de color al pasar el ratón."""
    def __init__(self, x, y, w, h, texto, font, color_base, color_hover):
        self.rect = pygame.Rect(x, y, w, h)
        self.texto = texto
        self.font = font
        self.color_base = pygame.Color(color_base)
        self.color_hover = pygame.Color(color_hover)
        self.color_actual = self.color_base
        self.hover = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.hover:
            return True
        return False

    def draw(self, screen):
        self.hover = self.rect.collidepoint(pygame.mouse.get_pos())
        target_color = self.color_hover if self.hover else self.color_base
        self.color_actual = self.color_actual.lerp(target_color, 0.2)
        
        pygame.draw.rect(screen, self.color_actual, self.rect, border_radius=8)
        dibujar_texto(screen, self.texto, self.rect.center, self.font, (255, 255, 255), centrado=True)

# --- 4. CLASE PRINCIPAL DE LA APLICACIÓN (CONTROLADOR) ---

class App:
    def __init__(self):
        self.reloj = pygame.time.Clock()
        self.logica = HashMapContactos(tamano_inicial=5)
        self.contactos_visuales = {}  # Mapea id(nodo_logico) -> objeto ContactoVisual
        
        # Sistema de notificaciones
        self.feedback_texto = ""
        self.feedback_color = COLORES['texto_principal']
        self.feedback_alpha = 0
        self.feedback_timer = 0
        
        self.crear_widgets_ui()

    def crear_widgets_ui(self):
        """Inicializa todos los elementos de la interfaz de usuario."""
        self.input_nombre = InputBox(50, 150, 300, 45, FONT_NORMAL, "Nombre del contacto")
        self.input_telefono = InputBox(50, 215, 300, 45, FONT_NORMAL, "Número de teléfono")
        
        self.btn_agregar = Button(50, 290, 145, 50, "Agregar", FONT_SUBTITULO, COLORES['acento'], COLORES['acento_oscuro'])
        self.btn_buscar = Button(205, 290, 145, 50, "Buscar", FONT_SUBTITULO, COLORES['exito'], COLORES['exito_oscuro'])
        self.btn_eliminar = Button(50, 350, 300, 50, "Eliminar", FONT_SUBTITULO, COLORES['error'], COLORES['error_oscuro'])
        
        self.ui_elementos = [self.input_nombre, self.input_telefono, self.btn_agregar, self.btn_buscar, self.btn_eliminar]

    def set_feedback(self, texto, tipo='info', duracion=4):
        """Muestra un mensaje temporal en pantalla."""
        self.feedback_texto = texto
        self.feedback_timer = duracion
        self.feedback_alpha = 255
        if tipo == 'exito': self.feedback_color = COLORES['exito']
        elif tipo == 'error': self.feedback_color = COLORES['error']
        else: self.feedback_color = COLORES['info']

    def _get_posicion_visual(self, indice_tabla, pos_en_cadena):
        """Calcula las coordenadas X, Y para una tarjeta de contacto."""
        PADDING_X, MARGEN_X = 230, 10
        PADDING_Y, MARGEN_Y = 110, 20
        INICIO_X, INICIO_Y = 450, 80
        return (INICIO_X + pos_en_cadena * (PADDING_X + MARGEN_X), 
                INICIO_Y + indice_tabla * (PADDING_Y + MARGEN_Y))

    def recalcular_y_actualizar_visuales(self, origen_animacion, rehash=False):
        """
        Sincroniza el estado visual con el estado lógico.
        Si hay rehash, elimina todos los visuales y los crea de nuevo.
        """
        if rehash:
            # Desvanecer y eliminar todos los contactos visuales antiguos
            for vis in self.contactos_visuales.values():
                vis.target_alpha = 0
            # En una app real, esperaríamos a que la animación termine.
            # Aquí, para simplificar, los recreamos inmediatamente.
            self.contactos_visuales.clear()

        # Crear/actualizar visuales para todos los nodos en la tabla lógica
        for indice, nodo_cabeza in enumerate(self.logica.tabla):
            nodo_actual = nodo_cabeza
            pos_en_cadena = 0
            while nodo_actual:
                target_pos = self._get_posicion_visual(indice, pos_en_cadena)
                
                if id(nodo_actual) not in self.contactos_visuales:
                    # Es un nodo nuevo, crear su visual
                    vis = ContactoVisual(nodo_actual, origen_animacion, target_pos)
                    self.contactos_visuales[id(nodo_actual)] = vis
                else:
                    # El nodo ya existía, solo actualizar su posición destino
                    self.contactos_visuales[id(nodo_actual)].target_pos = pygame.Vector2(target_pos)
                
                nodo_actual = nodo_actual.siguiente
                pos_en_cadena += 1

    def accion_agregar(self):
        nombre = self.input_nombre.texto.strip()
        telefono = self.input_telefono.texto.strip()
        
        if not nombre or not telefono:
            self.set_feedback("Nombre y teléfono no pueden estar vacíos.", 'error')
            return

        status, indice = self.logica.agregar(nombre, telefono)
        
        if status == "rehash":
            self.set_feedback(f"¡Rehashing! Aumentando tamaño de la tabla.", 'info', duracion=5)
            # El rehash ya ocurrió en la lógica, ahora actualizamos toda la UI
            self.recalcular_y_actualizar_visuales(self.btn_agregar.rect.center, rehash=True)
        else:
            if status == "actualizado":
                self.set_feedback(f"Teléfono de '{nombre}' actualizado.", 'exito')
            else:
                self.set_feedback(f"'{nombre}' agregado en índice [{indice}].", 'exito')
            
            self.recalcular_y_actualizar_visuales(self.btn_agregar.rect.center)
        
        self.input_nombre.texto = ""
        self.input_telefono.texto = ""


    def accion_buscar(self):
        nombre = self.input_nombre.texto.strip()
        if not nombre:
            self.set_feedback("Introduce un nombre para buscar.", 'error')
            return
            
        valor, indice, pos = self.logica.buscar(nombre)
        if valor:
            self.set_feedback(f"Encontrado: {nombre} -> {valor}", 'exito')
            
            # Encontrar el nodo lógico para obtener su ID
            nodo_actual = self.logica.tabla[indice]
            for _ in range(pos):
                nodo_actual = nodo_actual.siguiente
            
            if id(nodo_actual) in self.contactos_visuales:
                self.contactos_visuales[id(nodo_actual)].highlight_timer = 2.0
        else:
            self.set_feedback(f"'{nombre}' no fue encontrado.", 'error')

    def accion_eliminar(self):
        nombre = self.input_nombre.texto.strip()
        if not nombre:
            self.set_feedback("Introduce un nombre para eliminar.", 'error')
            return

        # Primero, buscar el objeto para marcarlo para eliminación visual
        valor, indice, pos = self.logica.buscar(nombre)
        if valor:
            nodo_actual = self.logica.tabla[indice]
            for _ in range(pos):
                nodo_actual = nodo_actual.siguiente
            
            obj_id = id(nodo_actual)
            if obj_id in self.contactos_visuales:
                self.contactos_visuales[obj_id].target_alpha = 0 # Iniciar desvanecimiento

            # Luego, eliminarlo de la estructura de datos
            self.logica.eliminar(nombre)
            self.set_feedback(f"'{nombre}' ha sido eliminado.", 'exito')
            
            # Recalcular posiciones de los elementos restantes en la misma cadena
            self.recalcular_y_actualizar_visuales(self.btn_eliminar.rect.center)
            self.input_nombre.texto = ""
        else:
            self.set_feedback(f"No se puede eliminar: '{nombre}' no existe.", 'error')

    def manejar_eventos(self):
        """Procesa todas las entradas del usuario (teclado, ratón)."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Pasar eventos a los widgets
            for elem in self.ui_elementos:
                elem.handle_event(event)

            if self.btn_agregar.handle_event(event): self.accion_agregar()
            if self.btn_buscar.handle_event(event): self.accion_buscar()
            if self.btn_eliminar.handle_event(event): self.accion_eliminar()

    def actualizar(self, dt):
        """Actualiza el estado de todos los objetos animados."""
        # Actualizar contactos visuales y eliminar los que se han desvanecido
        ids_a_eliminar = []
        for id_obj, vis in self.contactos_visuales.items():
            vis.update(dt)
            if vis.target_alpha == 0 and vis.alpha < 1:
                ids_a_eliminar.append(id_obj)
        
        for id_obj in ids_a_eliminar:
            del self.contactos_visuales[id_obj]
            
        # Actualizar temporizador de feedback
        if self.feedback_timer > 0:
            self.feedback_timer -= dt
            if self.feedback_timer <= 0:
                self.feedback_alpha = 0 # Ocultar al terminar

    def dibujar_panel_control(self):
        """Dibuja el panel izquierdo de la UI."""
        panel_rect = pygame.Rect(0, 0, 400, ALTO)
        pygame.draw.rect(PANTALLA, COLORES['panel'], panel_rect)
        pygame.draw.line(PANTALLA, COLORES['borde'], (panel_rect.right, 0), (panel_rect.right, ALTO), 2)
        
        dibujar_texto(PANTALLA, "Agenda de Contactos", (50, 50), FONT_TITULO, COLORES['texto_principal'])
        dibujar_texto(PANTALLA, "Visualizador de Tabla Hash", (50, 90), FONT_NORMAL, COLORES['texto_secundario'])

        for elem in self.ui_elementos:
            elem.draw(PANTALLA)
        
        # Dibujar feedback
        if self.feedback_timer > 0:
            color = pygame.Color(self.feedback_color)
            # Interpolar alpha para un desvanecimiento suave al final
            fade_duration = 0.5
            if self.feedback_timer < fade_duration:
                color.a = int(255 * (self.feedback_timer / fade_duration))
            else:
                color.a = 255
            
            dibujar_texto(PANTALLA, self.feedback_texto, (50, 430), FONT_NORMAL, color)

    def dibujar_visualizador_hash(self):
        """Dibuja el área derecha con la estructura de datos."""
        # Título del área
        dibujar_texto(PANTALLA, f"Tabla Hash (Tamaño: {self.logica.tamano}, Carga: {self.logica.num_elementos / self.logica.tamano:.2f})", 
                      (450, 30), FONT_TITULO, COLORES['texto_principal'])

        # Dibujar los "buckets" o índices de la tabla
        for i in range(self.logica.tamano):
            # Obtenemos la altura correcta para la fila 'i'
            y_fila = self._get_posicion_visual(i, 0)[1] 
            
            # Definimos un rectángulo fijo para el bucket a la izquierda del área de contactos
            ancho_bucket, alto_bucket = 70, 80
            x_bucket = 425 # Posición X fija para que no se mueva al panel izquierdo
            bucket_rect = pygame.Rect(x_bucket, y_fila, ancho_bucket, alto_bucket)

            # Dibujar el rectángulo del bucket y su número de índice en el centro
            pygame.draw.rect(PANTALLA, COLORES['borde'], bucket_rect, 2, border_radius=8)
            dibujar_texto(PANTALLA, f"[{i}]", bucket_rect.center, FONT_MONO, COLORES['texto_secundario'], centrado=True)

        # Dibujar líneas de encadenamiento (colisiones)
        for vis in self.contactos_visuales.values():
            if vis.nodo_logico.siguiente:
                siguiente_id = id(vis.nodo_logico.siguiente)
                if siguiente_id in self.contactos_visuales:
                    vis2 = self.contactos_visuales[siguiente_id]
                    
                    # Solo dibujar línea si ambos nodos son visibles
                    if vis.alpha > 100 and vis2.alpha > 100:
                        start_pos = vis.pos + pygame.Vector2(vis.ancho, vis.alto / 2)
                        end_pos = vis2.pos + pygame.Vector2(0, vis2.alto / 2)
                        pygame.draw.line(PANTALLA, COLORES['info'], start_pos, end_pos, 3)
                        # Dibujar una pequeña flecha
                        vec = end_pos - start_pos
                        if vec.length() > 20:
                            arrow_p1 = end_pos - vec.normalize()*15 + (vec.normalize()*10).rotate(90)
                            arrow_p2 = end_pos - vec.normalize()*15 + (vec.normalize()*10).rotate(-90)
                            pygame.draw.polygon(PANTALLA, COLORES['info'], [end_pos, arrow_p1, arrow_p2])


        # Dibujar las tarjetas de contacto
        for vis in sorted(self.contactos_visuales.values(), key=lambda v: v.pos.y):
            vis.draw(PANTALLA)

    def dibujar(self):
        """Función principal de dibujo que orquesta todo el renderizado."""
        PANTALLA.fill(COLORES['fondo'])
        self.dibujar_panel_control()
        self.dibujar_visualizador_hash()
        pygame.display.flip()

    def run(self):
        """Bucle principal de la aplicación."""
        last_time = time.time()
        while True:
            # Delta time para animaciones independientes de la velocidad de fotogramas
            current_time = time.time()
            dt = current_time - last_time
            last_time = current_time
            
            self.manejar_eventos()
            self.actualizar(dt)
            self.dibujar()
            
            self.reloj.tick(60) # Limitar a 60 FPS

if __name__ == '__main__':
    app = App()
    app.run()

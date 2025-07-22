import tkinter as tk
from tkinter import ttk, messagebox
import math
import random
from typing import List, Tuple, Optional


class RedSocialPersonalizada:
    def __init__(self, master):
        self.master = master
        self.master.title("Analizador de Redes Sociales - Version Personalizada")
        self.master.geometry("1200x900")
        self.master.configure(bg='#f0f0f0')

        self.usuarios: List[str] = []
        self.posiciones: List[Tuple[int, int]] = []
        self.matriz_conexiones: List[List[int]] = []
        self.matriz_intensidad: List[List[int]] = []
        self.grupos: List[int] = []
        self.colores_grupos: List[str] = []
        self.umbral_amistad = 5

        self.crear_interfaz_moderna()
        self.generar_red_social()
        self.encontrar_grupos_de_amigos()
        self.calcular_posiciones_visuales()
        self.dibujar_red_social()

    def crear_interfaz_moderna(self):
        titulo_frame = tk.Frame(self.master, bg='#2c3e50', height=80)
        titulo_frame.pack(fill=tk.X, pady=(0, 10))
        titulo_frame.pack_propagate(False)

        titulo_label = tk.Label(titulo_frame, text="ANALIZADOR DE REDES SOCIALES",
                                font=("Arial", 20, "bold"), fg='white', bg='#2c3e50')
        titulo_label.pack(expand=True)

        subtitulo_label = tk.Label(titulo_frame, text="Descubre como se conectan las personas en tu red",
                                   font=("Arial", 11), fg='#ecf0f1', bg='#2c3e50')
        subtitulo_label.pack()

        main_container = tk.Frame(self.master, bg='#f0f0f0')
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        panel_izquierdo = tk.Frame(main_container, bg='white', relief=tk.RAISED, bd=2)
        panel_izquierdo.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        panel_derecho = tk.Frame(main_container, bg='white', relief=tk.RAISED, bd=2)
        panel_derecho.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.crear_panel_controles(panel_izquierdo)
        self.crear_panel_visualizacion(panel_derecho)

    def crear_panel_controles(self, parent):
        tk.Label(parent, text="CONTROLES", font=("Arial", 14, "bold"),
                 fg='#2c3e50', bg='white').pack(pady=15)

        buscar_frame = tk.LabelFrame(parent, text="Buscar Persona",
                                     font=("Arial", 11, "bold"), fg='#27ae60', bg='white')
        buscar_frame.pack(fill=tk.X, padx=15, pady=10)

        tk.Label(buscar_frame, text="Nombre de la persona:",
                 font=("Arial", 10), bg='white').pack(anchor=tk.W, padx=10, pady=5)

        self.entrada_persona = tk.Entry(buscar_frame, font=("Arial", 11), width=20)
        self.entrada_persona.pack(padx=10, pady=5)

        boton_buscar = tk.Button(buscar_frame, text="Analizar Conexiones",
                                 command=self.analizar_conexiones_persona,
                                 bg='#3498db', fg='white', font=("Arial", 10, "bold"),
                                 relief=tk.FLAT, padx=20, pady=5)
        boton_buscar.pack(pady=10)

        filtro_frame = tk.LabelFrame(parent, text="Filtro de Amistad",
                                     font=("Arial", 11, "bold"), fg='#e74c3c', bg='white')
        filtro_frame.pack(fill=tk.X, padx=15, pady=10)

        tk.Label(filtro_frame, text="Ajusta que tan cercanos deben ser\nlos amigos para formar un grupo:",
                 font=("Arial", 9), bg='white', justify=tk.LEFT).pack(padx=10, pady=5)

        self.valor_umbral = tk.StringVar(value="5")
        self.slider_amistad = tk.Scale(filtro_frame, from_=1, to=10, orient=tk.HORIZONTAL,
                                       variable=self.valor_umbral, command=self.actualizar_filtro_amistad,
                                       bg='white', font=("Arial", 9))
        self.slider_amistad.pack(fill=tk.X, padx=10, pady=5)

        etiquetas_frame = tk.Frame(filtro_frame, bg='white')
        etiquetas_frame.pack(fill=tk.X, padx=10)
        tk.Label(etiquetas_frame, text="Conocidos", font=("Arial", 8), bg='white').pack(side=tk.LEFT)
        tk.Label(etiquetas_frame, text="Amigos Intimos", font=("Arial", 8), bg='white').pack(side=tk.RIGHT)

        info_frame = tk.LabelFrame(parent, text="Estadisticas",
                                   font=("Arial", 11, "bold"), fg='#9b59b6', bg='white')
        info_frame.pack(fill=tk.X, padx=15, pady=10)

        self.info_text = tk.Text(info_frame, height=8, width=25, font=("Arial", 9),
                                 bg='#f8f9fa', relief=tk.FLAT, wrap=tk.WORD)
        self.info_text.pack(padx=10, pady=10)

        botones_frame = tk.Frame(parent, bg='white')
        botones_frame.pack(fill=tk.X, padx=15, pady=10)

        boton_nueva_red = tk.Button(botones_frame, text="Nueva Red",
                                    command=self.generar_nueva_red,
                                    bg='#f39c12', fg='white', font=("Arial", 10, "bold"),
                                    relief=tk.FLAT, padx=15, pady=5)
        boton_nueva_red.pack(fill=tk.X, pady=5)

        boton_ayuda = tk.Button(botones_frame, text="Ayuda",
                                command=self.mostrar_ayuda,
                                bg='#95a5a6', fg='white', font=("Arial", 10, "bold"),
                                relief=tk.FLAT, padx=15, pady=5)
        boton_ayuda.pack(fill=tk.X, pady=5)

    def crear_panel_visualizacion(self, parent):
        tk.Label(parent, text="MAPA DE CONEXIONES SOCIALES",
                 font=("Arial", 14, "bold"), fg='#2c3e50', bg='white').pack(pady=15)

        self.canvas = tk.Canvas(parent, width=800, height=600, bg='#ffffff',
                                relief=tk.SUNKEN, bd=2)
        self.canvas.pack(padx=20, pady=10)

        leyenda_frame = tk.Frame(parent, bg='white')
        leyenda_frame.pack(pady=10)

        tk.Label(leyenda_frame, text="Cada color representa un grupo de amigos cercanos",
                 font=("Arial", 10), bg='white').pack()
        tk.Label(leyenda_frame, text="Los numeros en las lineas muestran que tan fuerte es la amistad (1-10)",
                 font=("Arial", 9), fg='#7f8c8d', bg='white').pack()

    def generar_red_social(self):
        nombres_personas = [
            "Ana", "Luis", "Maria", "Carlos", "Laura", "Diego", "Carmen", "Miguel",
            "Sofia", "Alejandro", "Valentina", "Sebastian", "Isabella", "Mateo",
            "Camila", "Santiago", "Lucia", "Nicolas", "Gabriela", "Andres",
            "Daniela", "Felipe", "Natalia", "Joaquin", "Paola", "Emilio",
            "Catalina", "Tomas", "Fernanda", "Rodrigo"
        ]

        self.usuarios = nombres_personas.copy()
        random.shuffle(self.usuarios)

        n = len(self.usuarios)

        self.matriz_conexiones = [[0 for _ in range(n)] for _ in range(n)]
        self.matriz_intensidad = [[0 for _ in range(n)] for _ in range(n)]

        for i in range(n):
            num_conexiones = random.randint(3, 7)

            for _ in range(num_conexiones):
                j = random.randint(0, n - 1)
                if i != j and self.matriz_conexiones[i][j] == 0:
                    self.matriz_conexiones[i][j] = 1
                    self.matriz_conexiones[j][i] = 1

                    intensidad = random.randint(1, 10)
                    self.matriz_intensidad[i][j] = intensidad
                    self.matriz_intensidad[j][i] = intensidad

    def encontrar_grupos_de_amigos(self):
        n = len(self.usuarios)
        self.grupos = [-1] * n
        self.colores_grupos = []

        colores_bonitos = [
            '#e74c3c', '#3498db', '#2ecc71', '#f39c12', '#9b59b6',
            '#1abc9c', '#e67e22', '#34495e', '#f1c40f', '#e91e63',
            '#00bcd4', '#4caf50', '#ff9800', '#673ab7', '#607d8b'
        ]

        grupo_actual = 0

        for i in range(n):
            if self.grupos[i] == -1:
                if grupo_actual < len(colores_bonitos):
                    color = colores_bonitos[grupo_actual]
                else:
                    color = f"#{random.randint(0, 255):02x}{random.randint(0, 255):02x}{random.randint(0, 255):02x}"

                self.colores_grupos.append(color)
                self.buscar_amigos_cercanos(i, grupo_actual)
                grupo_actual += 1

    def buscar_amigos_cercanos(self, persona: int, grupo_id: int):
        self.grupos[persona] = grupo_id

        for i in range(len(self.usuarios)):
            if (self.matriz_conexiones[persona][i] == 1 and
                    self.matriz_intensidad[persona][i] >= self.umbral_amistad and
                    self.grupos[i] == -1):

                self.buscar_amigos_cercanos(i, grupo_id)

    def calcular_posiciones_visuales(self):
        self.posiciones = []
        centro_x, centro_y = 400, 300

        n = len(self.usuarios)

        if n <= 15:
            radio = 200
            for i in range(n):
                angulo = 2 * math.pi * i / n
                x = int(centro_x + radio * math.cos(angulo))
                y = int(centro_y + radio * math.sin(angulo))
                self.posiciones.append((x, y))
        else:
            radio_interno = 150
            radio_externo = 250

            mitad = n // 2

            for i in range(mitad):
                angulo = 2 * math.pi * i / mitad
                x = int(centro_x + radio_interno * math.cos(angulo))
                y = int(centro_y + radio_interno * math.sin(angulo))
                self.posiciones.append((x, y))

            for i in range(mitad, n):
                angulo = 2 * math.pi * (i - mitad) / (n - mitad)
                x = int(centro_x + radio_externo * math.cos(angulo))
                y = int(centro_y + radio_externo * math.sin(angulo))
                self.posiciones.append((x, y))

    def dibujar_red_social(self):
        self.canvas.delete("all")

        for i in range(len(self.usuarios)):
            for j in range(i + 1, len(self.usuarios)):
                if self.matriz_conexiones[i][j] == 1:
                    x1, y1 = self.posiciones[i]
                    x2, y2 = self.posiciones[j]

                    intensidad = self.matriz_intensidad[i][j]

                    if intensidad >= 8:
                        color = "#e74c3c"
                        grosor = 3
                    elif intensidad >= 6:
                        color = "#f39c12"
                        grosor = 2
                    else:
                        color = "#bdc3c7"
                        grosor = 1

                    self.canvas.create_line(x1, y1, x2, y2, fill=color, width=grosor)

                    if intensidad >= 6:
                        mid_x = (x1 + x2) // 2
                        mid_y = (y1 + y2) // 2
                        self.canvas.create_text(mid_x, mid_y, text=str(intensidad),
                                                fill="white", font=("Arial", 8, "bold"),
                                                tags="intensidad")
                        bbox = self.canvas.bbox("intensidad")
                        if bbox:
                            self.canvas.create_rectangle(bbox[0] - 2, bbox[1] - 2,
                                                         bbox[2] + 2, bbox[3] + 2,
                                                         fill=color, outline="", tags="bg_intensidad")
                            self.canvas.tag_lower("bg_intensidad")

        for i in range(len(self.usuarios)):
            x, y = self.posiciones[i]

            if self.grupos[i] < len(self.colores_grupos):
                color = self.colores_grupos[self.grupos[i]]
            else:
                color = "#95a5a6"

            self.canvas.create_oval(x - 20, y - 20, x + 20, y + 20,
                                    fill=color, outline="white", width=3,
                                    tags=f"persona_{i}")

            self.canvas.create_text(x, y - 35, text=self.usuarios[i],
                                    fill="#2c3e50", font=("Arial", 10, "bold"),
                                    tags=f"nombre_{i}")

            self.canvas.tag_bind(f"persona_{i}", "<Button-1>",
                                 lambda e, nombre=self.usuarios[i]: self.click_persona(nombre))

        self.actualizar_estadisticas()

    def click_persona(self, nombre):
        self.entrada_persona.delete(0, tk.END)
        self.entrada_persona.insert(0, nombre)
        self.analizar_conexiones_persona()

    def analizar_conexiones_persona(self):
        nombre = self.entrada_persona.get().strip()
        if not nombre:
            messagebox.showwarning("Advertencia", "Por favor, ingresa el nombre de una persona")
            return

        try:
            indice = self.usuarios.index(nombre)
        except ValueError:
            messagebox.showerror("Error", f"No se encontro a '{nombre}' en la red")
            return

        conexiones = []
        max_intensidad = 0
        mejor_amigo = ""
        total_conexiones = 0

        for j in range(len(self.usuarios)):
            if self.matriz_conexiones[indice][j] == 1:
                intensidad = self.matriz_intensidad[indice][j]
                conexiones.append((self.usuarios[j], intensidad))
                total_conexiones += 1

                if intensidad > max_intensidad:
                    max_intensidad = intensidad
                    mejor_amigo = self.usuarios[j]

        conexiones.sort(key=lambda x: x[1], reverse=True)

        if conexiones:
            mensaje = f"ANALISIS DE CONEXIONES DE {nombre.upper()}\n"
            mensaje += "=" * 50 + "\n\n"
            mensaje += f"Total de conexiones: {total_conexiones}\n"
            mensaje += f"Mejor amigo: {mejor_amigo} (intensidad {max_intensidad})\n\n"
            mensaje += "TODAS LAS CONEXIONES:\n"
            mensaje += "-" * 30 + "\n"

            for amigo, intensidad in conexiones[:10]:
                mensaje += f"{amigo}: {intensidad}/10\n"

            if len(conexiones) > 10:
                mensaje += f"... y {len(conexiones) - 10} conexiones mas\n"

            messagebox.showinfo(f"Analisis de {nombre}", mensaje)
        else:
            messagebox.showinfo("Sin conexiones", f"{nombre} no tiene conexiones en la red")

    def actualizar_filtro_amistad(self, valor):
        self.umbral_amistad = int(valor)
        self.encontrar_grupos_de_amigos()
        self.dibujar_red_social()

    def actualizar_estadisticas(self):
        self.info_text.delete(1.0, tk.END)

        total_usuarios = len(self.usuarios)
        total_conexiones = sum(sum(fila) for fila in self.matriz_conexiones) // 2

        grupos_unicos = set(self.grupos)
        num_grupos = len(grupos_unicos)

        conexiones_fuertes = 0
        conexiones_medias = 0
        conexiones_debiles = 0

        for i in range(len(self.usuarios)):
            for j in range(i + 1, len(self.usuarios)):
                if self.matriz_conexiones[i][j] == 1:
                    intensidad = self.matriz_intensidad[i][j]
                    if intensidad >= 8:
                        conexiones_fuertes += 1
                    elif intensidad >= 6:
                        conexiones_medias += 1
                    else:
                        conexiones_debiles += 1

        stats = f"""ESTADISTICAS DE LA RED

Personas: {total_usuarios}
Conexiones totales: {total_conexiones}
Grupos de amigos: {num_grupos}

Amistades fuertes (8-10): {conexiones_fuertes}
Amistades medias (6-7): {conexiones_medias}
Conocidos (1-5): {conexiones_debiles}

Filtro actual: {self.umbral_amistad}
"""

        self.info_text.insert(tk.END, stats)

    def generar_nueva_red(self):
        self.generar_red_social()
        self.encontrar_grupos_de_amigos()
        self.calcular_posiciones_visuales()
        self.dibujar_red_social()
        messagebox.showinfo("Nueva Red", "Se ha generado una nueva red social!")

    def mostrar_ayuda(self):
        ayuda = """GUIA DE USO DEL ANALIZADOR DE REDES SOCIALES

QUE HACE ESTA APLICACION?
Esta herramienta te permite visualizar y analizar como se conectan las personas en una red social.

CONTROLES:
- Buscar Persona: Escribe un nombre para ver sus conexiones
- Filtro de Amistad: Ajusta que tan cercanos deben ser los amigos
- Nueva Red: Genera una nueva red social aleatoria

COLORES Y SIMBOLOS:
- Cada color representa un grupo de amigos cercanos
- Las lineas rojas = amistades muy fuertes (8-10)
- Las lineas naranjas = amistades fuertes (6-7)
- Las lineas grises = conocidos (1-5)

INTERACTIVIDAD:
- Haz click en cualquier persona para ver sus conexiones
- Usa el slider para cambiar el filtro de amistad
- Los numeros en las lineas muestran la intensidad de la amistad

ESTADISTICAS:
En el panel izquierdo puedes ver estadisticas en tiempo real de la red.
"""
        messagebox.showinfo("Ayuda", ayuda)


def main():
    root = tk.Tk()
    app = RedSocialPersonalizada(root)
    root.mainloop()


if __name__ == "__main__":
    main()
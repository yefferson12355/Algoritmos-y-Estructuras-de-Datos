# Grafo Dinámico con C++/Qt

Este proyecto es una aplicación de escritorio desarrollada en C++ con el framework Qt 6 para visualizar grafos. Permite crear nodos y aristas dinámicamente, y calcula la ruta más corta entre dos puntos utilizando el algoritmo de Dijkstra.

## 📸 Captura de Pantalla
![Screenshot del programa](funcionando.png)

## ✨ Características
- **Visualización Gráfica**: Dibuja el grafo en pantalla, mostrando nodos, aristas y sus pesos correspondientes.
- **Creación Dinámica**: Permite definir la estructura del grafo mediante una entrada de texto simple.
- **Cálculo de Ruta Más Corta**: Implementa el algoritmo de Dijkstra para encontrar y resaltar el camino de menor coste entre un nodo de inicio y uno de fin.
- **Interfaz Interactiva**: Controles sencillos para crear el grafo y solicitar el cálculo de la ruta.

## ⚙️ Requisitos
Para compilar y ejecutar este proyecto desde el código fuente, es necesario tener instalado el siguiente software:

1.  **Compilador C++**: Se recomienda **Visual Studio 2022** (incluyendo la carga de trabajo "Desarrollo para el escritorio con C++").
2.  **CMake**: Versión 3.16 o superior.
3.  **Git**: Para clonar el repositorio.
4.  **vcpkg**: El gestor de paquetes de C++ de Microsoft, utilizado para instalar Qt.

## 🛠️ Instrucciones de Compilación y Ejecución
Sigue estos pasos para compilar el proyecto en un entorno de desarrollo como Visual Studio Code.

**1. Clonar el repositorio**
```bash
git clone [https://github.com/yefferson12355/Algoritmos-y-Estructuras-de-Datos.git](https://github.com/yefferson12355/Algoritmos-y-Estructuras-de-Datos.git)
# Navega a la carpeta del proyecto específico si es necesario
cd Algoritmos-y-Estructuras-de-Datos/Codebloks/GrafoDinamico
```

**2. Instalar dependencias (Qt 6)**
Usa `vcpkg` para instalar la librería Qt 6. Abre una terminal, navega a tu carpeta de `vcpkg` y ejecuta:
```bash
./vcpkg install qtbase:x64-windows
```

**3. Configurar el Proyecto en VS Code**
1.  Abre la carpeta del proyecto (`GrafoDinamico`) en Visual Studio Code.
2.  La extensión de CMake te pedirá seleccionar un "Kit". Elige el de **`Visual Studio 2022 Release - amd64`**.
3.  Abre la Paleta de Comandos (`Ctrl + Shift + P`) y selecciona `CMake: Edit User-Local CMake Kits`. Modifica el kit que elegiste para añadir la siguiente línea, apuntando a tu instalación de `vcpkg`:
    ```json
    "toolchainFile": "C:/dev/vcpkg/scripts/buildsystems/vcpkg.cmake"
    ```
4.  Finalmente, ejecuta `CMake: Configure` desde la Paleta de Comandos para que el proyecto se configure correctamente.

**4. Compilar (Build)**
- En la barra de estado azul de VS Code, selecciona el modo (`[Debug]` o `[Release]`).
- Haz clic en el botón **`Build`**.

**5. Ejecutar (Run)**
Para evitar errores de librerías no encontradas, es necesario usar la configuración de lanzamiento:
1.  Ve al panel de **"Run and Debug" (🐞)**.
2.  Crea o modifica el archivo `.vscode/launch.json` para que contenga las configuraciones de Debug y Release, asegurando que el `PATH` apunte a las librerías de `vcpkg`.
3.  Selecciona la configuración deseada (ej: `Ejecutar (Release)`) y haz clic en el **botón verde de Play (▶️)**.

## 💻 Uso de la Aplicación
- **Crear Grafo**: En el área de texto superior, ingresa las aristas en el formato `Nodo1 Nodo2 Peso` (una por cada línea) y presiona el botón "Crear Grafo".
- **Buscar Ruta**: Ingresa el nombre del nodo de inicio y de fin en sus respectivos campos de texto y presiona "Buscar Ruta".
- **Resultado**: La ruta más corta y su distancia total se mostrarán en el área de resultados, y el camino se resaltará en rojo en el grafo visual.

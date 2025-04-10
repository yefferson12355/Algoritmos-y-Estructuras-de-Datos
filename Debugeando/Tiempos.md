
                                        C++
```cpp
clock_t inicio = clock();


clock_t es un tipo de dato definido en la librería <ctime> (o <time.h> en C). Se usa para representar tiempo de CPU.

clock() es una función que devuelve el número de ciclos de CPU desde que empezó a ejecutarse el programa.

Al guardar el valor en inicio, estás marcando el tiempo de inicio del bloque que quieres medir.

Más adelante, haces:

clock_t fin = clock();
double tiempo = double(fin - inicio) / CLOCKS_PER_SEC;

fin - inicio: calcula cuántos "ticks de CPU" pasaron.

CLOCKS_PER_SEC: constante que indica cuántos ticks hay en un segundo. Por lo general es 1000, pero depende del sistema.

Dividir entre CLOCKS_PER_SEC convierte los ticks en segundos reales.


```python

import time

# Registrar el tiempo de inicio
inicio = time.time()

# Código a medir (por ejemplo, una operación simple como un bucle)
suma = 0
for i in range(1000000):
    suma += i

# Registrar el tiempo de finalización
fin = time.time()

# Mostrar el resultado de la operación (suma en este caso)
print(f"Suma total: {suma}")

# Mostrar el tiempo transcurrido
print(f"Tiempo de ejecución: {fin - inicio:.6f} segundos")

                                    AMBOS

C++
clock() + CLOCKS_PER_SEC: básico, buena precisión.

chrono::high_resolution_clock: más preciso (recomendado).

Python
time.time(): general.

time.perf_counter(): precisión alta.

time.process_time(): solo CPU.
1. C++:
Usaremos chrono::high_resolution_clock para obtener un tiempo de ejecución de alta precisión. Imagina que estás comparando un algoritmo simple, como la suma de una matriz:
2. Python:
En Python, utilizamos time.perf_counter() para obtener un tiempo de ejecución con alta precisión. El código sería equivalente al de C++:
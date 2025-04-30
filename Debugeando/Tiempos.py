import time

# Marca el inicio
inicio = time.time()

# Código cuya duración deseas medir
for i in range(1000000):
    pass  # Esto es solo un bucle de ejemplo

# Marca el final
fin = time.time()

# Imprime el tiempo transcurrido
print("Tiempo de ejecución:", fin - inicio, "segundos")

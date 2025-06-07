import math
import Telefonos

def buscar_binario(lista, nombre):
    bajo = 0
    alto = len(lista) - 1

    while bajo <= alto:
        medio = (bajo + alto) // 2
        guess = lista[medio][0]

        if guess == nombre:
            return lista[medio][1]  # devuelve el número de teléfono
        elif guess > nombre:
            alto = medio - 1
        else:
            bajo = medio + 1
    return None

# Buscar a "Daniela"
print(buscar_binario(Telefonos.lista_telefonica, "Daniela"))  # 921001054


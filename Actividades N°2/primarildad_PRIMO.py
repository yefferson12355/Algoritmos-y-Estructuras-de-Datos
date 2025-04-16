from math import isqrt  # isqrt evita usar float y es más rápido

def es_primo(val):
    if val < 2:
        return False
    if val == 2:
        return True
    if val % 2 == 0:
        return False

    # Verifica solo números impares hasta la raíz cuadrada
    for i in range(3, isqrt(val) + 1, 2):
        if val % i == 0:
            return False
    return True
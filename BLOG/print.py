print("Hello, World!")
sep, end, file = "             ", "  ", "print.py"
print(f"{sep} {end} {file}")

print("Hello"+sep+"World!"+end+file)
##Las f-strings permiten insertar valores directamente dentro de una cadena de texto, mejorando la legibilidad:
frase = "Sample Phrase"
autor = "Author Name"
print(f"Frase: {frase}, Autor: {autor}")
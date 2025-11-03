
import random
import string


def generar_contraseña():
    # Definir los conjuntos de caracteres
    mayusculas = string.ascii_uppercase
    minusculas = string.ascii_lowercase
    numeros = string.digits
    especiales = '@.!_$'

    # Asegurar al menos un carácter de cada tipo
    contrasena = [
        random.choice(mayusculas),
        random.choice(minusculas),
        random.choice(numeros),
        random.choice(especiales)
    ]

    # Completar hasta 8 caracteres con caracteres aleatorios de todos los tipos
    todos_caracteres = mayusculas + minusculas + numeros + especiales
    contrasena.extend(random.choice(todos_caracteres) for _ in range(4))

    # Mezclar la contraseña
    random.shuffle(contrasena)

    return ''.join(contrasena)

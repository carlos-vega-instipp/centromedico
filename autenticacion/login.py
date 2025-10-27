# login.py

usuarios_registrados = {
    "dbuele420_est@instipp.edu.ec": "12345678",
}

def login(correo, contraseña):
    if correo in usuarios_registrados and usuarios_registrados[correo] == contraseña:
        return "Inicio de sesión exitoso. Bienvenida al panel."
    else:
        return "Credenciales incorrectas o usuario no registrado."


def recuperar_contraseña(correo):
    if correo not in usuarios_registrados:
        return "El correo ingresado no está registrado."
    else:
        codigo_temporal = "TEMP123"
        return f"Código temporal enviado a {correo}: {codigo_temporal}"


def actualizar_contraseña(correo, nueva, confirmar):
    if correo not in usuarios_registrados:
        return "El correo ingresado no está registrado."
    if nueva != confirmar:
        return "Las contraseñas no coinciden."
    usuarios_registrados[correo] = nueva
    return "Contraseña actualizada con éxito."

# ══════════════════════════════════════════════════════════════
# GuardiánClima ITBA — Autenticación y Registro
# ══════════════════════════════════════════════════════════════

from __future__ import annotations

import os
import csv

from config import (
    ARCHIVO_USUARIOS,
    PASSWORD_MIN_LENGTH,
    PASSWORD_CARACTERES_ESPECIALES,
    REGLAS_PASSWORD,
)
from ui import (
    console,
    input_hacker,
    input_password,
    typing_effect,
    mostrar_error,
    mostrar_exito,
    mostrar_info,
    barra_fuerza_password,
    mostrar_ascii,
    ASCII_ESCUDO,
    ASCII_LOGIN,
)

# Ruta absoluta al CSV, relativa a la ubicación de este script
_DIRECTORIO_BASE = os.path.dirname(os.path.abspath(__file__))
_RUTA_USUARIOS = os.path.join(_DIRECTORIO_BASE, ARCHIVO_USUARIOS)


# ══════════════════════════════════════════════════════════════
# GESTIÓN DEL ARCHIVO DE USUARIOS
# ══════════════════════════════════════════════════════════════

def cargar_usuarios() -> dict:
    """Carga los usuarios desde el archivo CSV.

    Lee el archivo CSV con columnas (usuario, password) y devuelve
    un diccionario {nombre_de_usuario: contraseña}.
    Si el archivo no existe, devuelve un diccionario vacío.

    Returns:
        dict: Diccionario con los usuarios y sus contraseñas.
    """
    usuarios = {}

    if not os.path.exists(_RUTA_USUARIOS):
        return usuarios

    try:
        with open(_RUTA_USUARIOS, "r", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                usuario = fila.get("usuario", "").strip()
                password = fila.get("password", "").strip()
                if usuario:
                    usuarios[usuario] = password
    except (IOError, csv.Error) as e:
        mostrar_error(f"No se pudo leer el archivo de usuarios: {e}")

    return usuarios


def guardar_usuario(usuario: str, password: str) -> None:
    """Guarda un nuevo usuario al final del archivo CSV.

    Si el archivo no existe, lo crea con el encabezado correspondiente.

    Args:
        usuario: Nombre de usuario a registrar.
        password: Contraseña del usuario.
    """
    archivo_existe = os.path.exists(_RUTA_USUARIOS)

    try:
        with open(_RUTA_USUARIOS, "a", encoding="utf-8", newline="") as archivo:
            escritor = csv.writer(archivo)
            # Si el archivo es nuevo, escribir la cabecera primero
            if not archivo_existe:
                escritor.writerow(["usuario", "password"])
            escritor.writerow([usuario, password])
    except IOError as e:
        mostrar_error(f"No se pudo guardar el usuario: {e}")


# ══════════════════════════════════════════════════════════════
# VALIDACIÓN DE CONTRASEÑA
# ══════════════════════════════════════════════════════════════

def calcular_fuerza(password: str, username: str) -> int:
    """Calcula la fuerza de una contraseña en base a 5 reglas.

    Cada regla cumplida suma 1 punto al puntaje total.

    Reglas evaluadas:
        1. Longitud mínima de PASSWORD_MIN_LENGTH caracteres
        2. Al menos 1 letra mayúscula
        3. Al menos 1 dígito
        4. Al menos 1 carácter especial
        5. No debe contener el nombre de usuario (case-insensitive)

    Args:
        password: Contraseña a evaluar.
        username: Nombre de usuario para verificar que no esté incluido.

    Returns:
        int: Puntaje de fuerza entre 0 y 5.
    """
    puntaje = 0

    # Regla 1: longitud mínima
    if len(password) >= PASSWORD_MIN_LENGTH:
        puntaje += 1

    # Regla 2: al menos una mayúscula
    if any(c.isupper() for c in password):
        puntaje += 1

    # Regla 3: al menos un dígito
    if any(c.isdigit() for c in password):
        puntaje += 1

    # Regla 4: al menos un carácter especial
    if any(c in PASSWORD_CARACTERES_ESPECIALES for c in password):
        puntaje += 1

    # Regla 5: no contener el nombre de usuario (case-insensitive)
    if username and username.lower() not in password.lower():
        puntaje += 1

    return puntaje


def validar_password(password: str, username: str) -> tuple:
    """Valida una contraseña contra las 5 reglas de seguridad.

    Args:
        password: Contraseña a validar.
        username: Nombre de usuario (para regla de no-inclusión).

    Returns:
        tuple: (es_valida, reglas_fallidas, puntaje)
            - es_valida (bool): True si cumple las 5 reglas.
            - reglas_fallidas (list): Lista de dicts con las reglas que falló.
            - puntaje (int): Fuerza de la contraseña (0-5).
    """
    reglas_fallidas = []

    # Regla 1: longitud mínima
    if len(password) < PASSWORD_MIN_LENGTH:
        reglas_fallidas.append(REGLAS_PASSWORD[0])

    # Regla 2: al menos una mayúscula
    if not any(c.isupper() for c in password):
        reglas_fallidas.append(REGLAS_PASSWORD[1])

    # Regla 3: al menos un dígito
    if not any(c.isdigit() for c in password):
        reglas_fallidas.append(REGLAS_PASSWORD[2])

    # Regla 4: al menos un carácter especial
    if not any(c in PASSWORD_CARACTERES_ESPECIALES for c in password):
        reglas_fallidas.append(REGLAS_PASSWORD[3])

    # Regla 5: no contener el nombre de usuario
    if username and username.lower() in password.lower():
        reglas_fallidas.append(REGLAS_PASSWORD[4])

    puntaje = calcular_fuerza(password, username)
    es_valida = len(reglas_fallidas) == 0

    return es_valida, reglas_fallidas, puntaje


# ══════════════════════════════════════════════════════════════
# FLUJO DE INICIO DE SESIÓN
# ══════════════════════════════════════════════════════════════

def iniciar_sesion() -> str | None:
    """Flujo de inicio de sesión con 3 intentos máximos.

    Muestra el arte ASCII_LOGIN, solicita usuario y contraseña,
    y verifica las credenciales contra el archivo CSV.
    Permite hasta 3 intentos antes de bloquear el acceso.

    Returns:
        str: Nombre de usuario si el login es exitoso.
        None: Si se agotan los intentos o se cancela.
    """
    MAX_INTENTOS = 3

    mostrar_ascii(ASCII_LOGIN, titulo="Inicio de Sesión")
    console.print()
    typing_effect("  🔐 Ingresá tus credenciales para acceder al sistema", velocidad=0.02)
    console.print()

    usuarios = cargar_usuarios()

    for intento in range(1, MAX_INTENTOS + 1):
        intentos_restantes = MAX_INTENTOS - intento

        # Solicitar usuario
        usuario = input_hacker("Usuario")

        # Permitir cancelar escribiendo 'cancelar'
        if usuario.lower() == "cancelar":
            mostrar_info("Inicio de sesión cancelado.")
            return None

        # Solicitar contraseña (sin eco)
        password = input_password("Contraseña")

        # Verificar credenciales
        if usuario in usuarios and usuarios[usuario] == password:
            mostrar_exito(f"¡Bienvenido, {usuario}! Acceso concedido.")
            typing_effect("  ▶ Cargando sistema...", velocidad=0.03, estilo="dim green")
            return usuario
        else:
            if intentos_restantes > 0:
                mostrar_error(
                    f"Credenciales incorrectas. "
                    f"Te quedan {intentos_restantes} intento{'s' if intentos_restantes != 1 else ''}."
                )
            else:
                mostrar_error("Credenciales incorrectas. Se agotaron los intentos.")

    # Se agotaron los 3 intentos
    console.print()
    typing_effect(
        "  🚫 Acceso denegado — demasiados intentos fallidos.",
        velocidad=0.03,
        estilo="red",
    )
    console.print()
    return None


# ══════════════════════════════════════════════════════════════
# FLUJO DE REGISTRO
# ══════════════════════════════════════════════════════════════

def registrar_usuario() -> str | None:
    """Flujo de registro de un nuevo usuario.

    Muestra el arte ASCII_ESCUDO, solicita un nombre de usuario único,
    y luego una contraseña que cumpla las 5 reglas de seguridad.
    Muestra la barra de fuerza y recomendaciones en tiempo real.
    El usuario puede escribir 'cancelar' en cualquier momento para abortar.

    Returns:
        str: Nombre del usuario registrado si el registro es exitoso.
        None: Si el usuario cancela el proceso.
    """
    mostrar_ascii(ASCII_ESCUDO, titulo="Registro de Usuario")
    console.print()
    typing_effect("  🛡  Creá tu cuenta para acceder a GuardiánClima", velocidad=0.02)
    console.print()

    # ── Paso 1: Elegir nombre de usuario ──────────────────────
    usuarios = cargar_usuarios()

    while True:
        usuario = input_hacker("Elegí un nombre de usuario")

        if usuario.lower() == "cancelar":
            mostrar_info("Registro cancelado.")
            return None

        if not usuario:
            mostrar_error("El nombre de usuario no puede estar vacío.")
            continue

        if usuario in usuarios:
            mostrar_error(f"El usuario '{usuario}' ya existe. Elegí otro nombre.")
            continue

        # Usuario válido y disponible
        mostrar_exito(f"Usuario '{usuario}' disponible.")
        break

    # ── Paso 2: Mostrar reglas de contraseña ──────────────────
    console.print()
    console.print("  [bold bright_green]📋 Reglas para la contraseña:[/bold bright_green]")
    console.print()
    for i, regla in enumerate(REGLAS_PASSWORD, 1):
        console.print(f"    [dim green]{i}.[/dim green] [green]{regla['descripcion']}[/green]")
    console.print()

    # ── Paso 3: Solicitar contraseña válida ───────────────────
    while True:
        password = input_password("Elegí una contraseña")

        if password.lower() == "cancelar":
            mostrar_info("Registro cancelado.")
            return None

        if not password:
            mostrar_error("La contraseña no puede estar vacía.")
            continue

        # Validar contraseña y mostrar fuerza
        es_valida, reglas_fallidas, puntaje = validar_password(password, usuario)
        barra_fuerza_password(puntaje)

        if es_valida:
            # Confirmar contraseña
            password_confirm = input_password("Confirmá tu contraseña")

            if password_confirm != password:
                mostrar_error("Las contraseñas no coinciden. Intentá de nuevo.")
                continue

            # Guardar usuario y confirmar registro
            guardar_usuario(usuario, password)
            console.print()
            mostrar_exito(f"¡Usuario '{usuario}' registrado exitosamente!")
            typing_effect(
                "  ▶ Tu cuenta ha sido creada. Ya podés iniciar sesión.",
                velocidad=0.02,
                estilo="dim green",
            )
            console.print()
            return usuario
        else:
            # Mostrar reglas que no se cumplieron con recomendaciones
            console.print("  [red]✘ La contraseña no cumple las siguientes reglas:[/red]")
            console.print()
            for regla in reglas_fallidas:
                console.print(f"    [red]✗[/red] [bright_red]{regla['nombre']}[/bright_red]: {regla['descripcion']}")
                console.print(f"      [dim green]💡 {regla['recomendacion']}[/dim green]")
            console.print()
            mostrar_info("Intentá de nuevo con una contraseña más segura, o escribí 'cancelar' para salir.")

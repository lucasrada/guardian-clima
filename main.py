# ══════════════════════════════════════════════════════════════
# GuardiánClima ITBA — Punto de Entrada Principal
# ══════════════════════════════════════════════════════════════
#
# Ejecutar con: python main.py
# ══════════════════════════════════════════════════════════════

import sys

from ui import (
    console,
    limpiar_pantalla,
    mostrar_banner,
    mostrar_menu,
    mostrar_despedida,
    mostrar_acerca_de,
    typing_effect,
    mostrar_info,
    mostrar_separador,
    pausar, )
from auth import iniciar_sesion, registrar_usuario
from estadisticas import menu_historial_personal, menu_estadisticas_globales
from ia import menu_consejo_ia


# ══════════════════════════════════════════════════════════════
# PANTALLA DE BIENVENIDA
# ══════════════════════════════════════════════════════════════

def pantalla_bienvenida():
    """Muestra la secuencia de bienvenida con efecto Matrix y banner."""
    limpiar_pantalla()
    mostrar_banner()
    typing_effect(
        "  Bienvenido a GuardiánClima ITBA",
        velocidad=0.03,
        estilo="green",
    )
    typing_effect(
        "  Desarrollado para ITBA — Proyecto Integrador",
        velocidad=0.03,
        estilo="dim green",
    )
    mostrar_separador()


# ══════════════════════════════════════════════════════════════
# MENÚ DE ACCESO (PRE-LOGIN)
# ══════════════════════════════════════════════════════════════

def menu_acceso():
    """Menú pre-login: iniciar sesión, registrarse o salir.

    Returns:
        str: Nombre del usuario autenticado.
        None: Si el usuario decide salir.
    """
    while True:
        opcion = mostrar_menu(
            "Acceso al Sistema",
            [
                "Iniciar Sesión",
                "Registrar Nuevo Usuario",
                "Salir",
            ],
        )

        if opcion == "1":
            limpiar_pantalla()
            usuario = iniciar_sesion()
            if usuario:
                return usuario
            pausar()
            limpiar_pantalla()
            mostrar_banner()

        elif opcion == "2":
            limpiar_pantalla()
            usuario = registrar_usuario()
            if usuario:
                # Después de registrarse, pedir que inicie sesión
                mostrar_info("Ahora podés iniciar sesión con tu nueva cuenta.")
                pausar()
            limpiar_pantalla()
            mostrar_banner()

        elif opcion == "3":
            return None


# ══════════════════════════════════════════════════════════════
# MENÚ PRINCIPAL (POST-LOGIN)
# ══════════════════════════════════════════════════════════════

def menu_principal(usuario):
    """Menú principal del sistema para un usuario autenticado.

    Opciones disponibles:
        1. Consultar clima actual
        2. Ver historial personal
        3. Estadísticas globales
        4. Consejo de vestimenta IA
        5. Acerca de
        6. Cerrar sesión

    Args:
        usuario: Nombre del usuario autenticado.

    Returns:
        str: "cerrar_sesion" si el usuario cierra sesión.
    """
    # Variable para guardar la última consulta de clima (para IA)
    ultimo_clima = None

    while True:
        limpiar_pantalla()
        mostrar_banner()

        console.print(f"  [dim green]Sesión activa:[/dim green] [bright_green]{usuario}[/bright_green]")

        opcion = mostrar_menu(
            "Menú Principal",
            [
                "[*] Consultar Clima Actual",
                "[*] Ver Historial Personal",
                "[*] Estadísticas Globales",
                "[*] Consejo de Vestimenta IA",
                "[*] Acerca de",
                "[-] Cerrar Sesión",
            ],
        )

        if opcion == "1":
            limpiar_pantalla()
            ultimo_clima = _consultar_clima_con_retorno(usuario)
            pausar()

        elif opcion == "2":
            limpiar_pantalla()
            menu_historial_personal(usuario)

        elif opcion == "3":
            limpiar_pantalla()
            menu_estadisticas_globales()

        elif opcion == "4":
            limpiar_pantalla()
            menu_consejo_ia(ultimo_clima)

        elif opcion == "5":
            limpiar_pantalla()
            mostrar_acerca_de()
            pausar()

        elif opcion == "6":
            typing_effect(
                f"  [*] Cerrando sesión de {usuario}...",
                velocidad=0.03,
                estilo="green",
            )
            return "cerrar_sesion"


def _consultar_clima_con_retorno(usuario):
    """Wrapper sobre menu_consultar_clima que captura el último resultado.

    Ejecuta la consulta de clima y retorna los datos para uso
    posterior (ej: pasar al consejo IA).

    Args:
        usuario: Nombre del usuario autenticado.

    Returns:
        dict o None: Datos del clima consultado.
    """
    from clima import consultar_clima
    from ui import (
         input_hacker, mostrar_spinner,
        mostrar_clima_panel, mostrar_error, mostrar_exito, mostrar_info,
    )
    from clima import guardar_en_historial
    from config import USE_REAL_API


    ciudad = input_hacker("Ingresá el nombre de la ciudad")

    if not ciudad:
        mostrar_error("Debés ingresar un nombre de ciudad.")
        return None

    modo = "API real" if USE_REAL_API else "simulación"
    mostrar_spinner(f"Consultando clima en {ciudad} (modo {modo})...", duracion=2)

    datos = consultar_clima(ciudad)

    if datos is None:
        mostrar_error("No se pudieron obtener los datos del clima.")
        return None

    mostrar_clima_panel(datos)

    if not USE_REAL_API:
        mostrar_info("Datos generados en modo simulación (mock). Activá USE_REAL_API en config.py para datos reales.")

    guardar_en_historial(usuario, datos["ciudad"], datos)
    mostrar_exito(f"Consulta guardada en el historial para '{datos['ciudad']}'.")

    return datos


# ══════════════════════════════════════════════════════════════
# EJECUCIÓN PRINCIPAL
# ══════════════════════════════════════════════════════════════

def main():
    """Punto de entrada principal de la aplicación GuardiánClima ITBA."""
    try:
        # ── Pantalla de bienvenida ───────────────────────────
        pantalla_bienvenida()

        # ── Loop principal ───────────────────────────────────
        while True:
            # Menú de acceso (login/registro)
            usuario = menu_acceso()

            if usuario is None:
                # El usuario eligió salir
                break

            # Menú principal (post-login)
            menu_principal(usuario)

            # Si resultado == "cerrar_sesion", vuelve al menú de acceso.
            # Desde el Menú de Acceso el usuario puede salir de la aplicación.
            limpiar_pantalla()
            mostrar_banner()

        # ── Despedida ────────────────────────────────────────
        mostrar_despedida()

    except KeyboardInterrupt:
        # Ctrl+C capturado — salida limpia
        mostrar_despedida()
        sys.exit(0)


if __name__ == "__main__":
    main()

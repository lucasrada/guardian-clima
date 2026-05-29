# ══════════════════════════════════════════════════════════════
# GuardiánClima ITBA — Interfaz de Usuario
# ══════════════════════════════════════════════════════════════

import os
import sys
import time
import random

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.align import Align
from rich.columns import Columns
from rich.progress import Progress, BarColumn, TextColumn
from rich.live import Live
from rich.theme import Theme

from config import APP_NOMBRE, APP_VERSION, THEME_COLORS

# ── Tema personalizado Matrix ────────────────────────────────
tema_matrix = Theme({
    "info": "cyan",
    "warning": "yellow",
    "danger": "bold red",
    "success": "bold bright_green",
    "matrix": "green",
    "matrix.bright": "bright_green",
    "matrix.dim": "dim green",
    "titulo": "bold bright_green",
    "subtitulo": "green",
    "borde": "green",
})

console = Console(theme=tema_matrix)

# ══════════════════════════════════════════════════════════════
# ASCII ART
# ══════════════════════════════════════════════════════════════

BANNER_PRINCIPAL = r"""
  ██████╗ ██╗   ██╗ █████╗ ██████╗ ██████╗ ██╗ █████╗ ███╗   ██╗
 ██╔════╝ ██║   ██║██╔══██╗██╔══██╗██╔══██╗██║██╔══██╗████╗  ██║
 ██║  ███╗██║   ██║███████║██████╔╝██║  ██║██║███████║██╔██╗ ██║
 ██║   ██║██║   ██║██╔══██║██╔══██╗██║  ██║██║██╔══██║██║╚██╗██║
 ╚██████╔╝╚██████╔╝██║  ██║██║  ██║██████╔╝██║██║  ██║██║ ╚████║
  ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚═╝╚═╝  ╚═╝╚═╝ ╚═══╝
       ██████╗██╗     ██╗███╗   ███╗ █████╗
      ██╔════╝██║     ██║████╗ ████║██╔══██╗
      ██║     ██║     ██║██╔████╔██║███████║
      ██║     ██║     ██║██║╚██╔╝██║██╔══██║
      ╚██████╗███████╗██║██║ ╚═╝ ██║██║  ██║
       ╚═════╝╚══════╝╚═╝╚═╝     ╚═╝╚═╝  ╚═╝
"""

ASCII_SOL = r"""
      \   |   /
       .-' '-.
    --|       |--
       '-._.-'
      /   |   \
"""

ASCII_NUBE = r"""
       .-~~~-.
     .-'       `-.
    /             \
   |               |
    \             /
     `-._______.-'
"""

ASCII_LLUVIA = r"""
       .-~~~-.
     .-'       `-.
    /             \
   |               |
    \             /
     `-._______.-'
      /  /  /  /
     /  /  /  /
"""

ASCII_NIEVE = r"""
       .-~~~-.
     .-'       `-.
    /             \
   |               |
    \             /
     `-._______.-'
      *  *  *  *
       *  *  *  *
"""

ASCII_ESCUDO = r"""
       __________
      /          \
     /   ______   \
    /   |      |   \
   |    |      |    |
   |    |      |    |
    \   |______|   /
     \            /
      \          /
       \________/
"""

ASCII_ROBOT = r"""
       +-------+
       | O   O |
       |  ---  |
       +---+---+
      +----+----+
      |    |    |
      |   A I   |
      |    |    |
      +----+----+
           |
          -+-
"""

ASCII_GRAFICO = r"""
       __
      |  |   __
    __|  |  |  |
   |  |  |  |  |   __
   |  |  |  |  |  |  |
   |__|__|__|__|__|__|
"""

ASCII_HISTORIAL = r"""
   +--------------+
   | +----------+ |
   | |          | |
   | |   [**]   | |
   | |          | |
   | +----------+ |
   +--------------+
"""

ASCII_LOGIN = r"""
   +-----------------+
   |  +---+          |
   |  | O |  > _     |
   |  +---+          |
   |  ***************|
   |                 |
   +-----------------+
"""

ASCII_DESPEDIDA = r"""
      *  .  *
   .    *    .
  *  HASTA   *
  .  PRONTO  .
  *  . * .   *
   .    *   .
      *  .
"""


# ══════════════════════════════════════════════════════════════
# EFECTOS VISUALES
# ══════════════════════════════════════════════════════════════

def limpiar_pantalla():
    """Limpia la pantalla de la terminal."""
    os.system("cls" if os.name == "nt" else "clear")


def typing_effect(texto, velocidad=0.03, estilo="green"):
    """Efecto de escritura progresiva estilo hacker."""
    text = Text()
    for char in texto:
        text.append(char, style=estilo)
        console.print(text, end="\r")
        time.sleep(velocidad)
    console.print()


def efecto_matrix(duracion=3, ancho=None):
    """Efecto lluvia de caracteres estilo Matrix."""
    if ancho is None:
        ancho = console.width

    chars = "01アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン"
    columnas = [0] * ancho
    intensidades = ["dim green", "green", "bright_green", "bold bright_green"]

    inicio = time.time()

    with Live(console=console, refresh_per_second=15, transient=True) as live:
        while time.time() - inicio < duracion:
            lineas = []
            texto = Text()
            for col in range(ancho):
                if random.random() < 0.1:
                    columnas[col] = random.randint(1, 4)

                if columnas[col] > 0:
                    char = random.choice(chars)
                    intensidad = intensidades[min(columnas[col] - 1, len(intensidades) - 1)]
                    texto.append(char, style=intensidad)
                    columnas[col] -= 1
                else:
                    texto.append(" ")

            live.update(texto)
            time.sleep(0.07)


def mostrar_spinner(mensaje, duracion=2):
    """Muestra un spinner animado con un mensaje."""
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    inicio = time.time()
    i = 0

    with Live(console=console, refresh_per_second=12, transient=True) as live:
        while time.time() - inicio < duracion:
            frame = frames[i % len(frames)]
            text = Text()
            text.append(f"  {frame} ", style="bright_green")
            text.append(mensaje, style="green")
            live.update(text)
            time.sleep(0.08)
            i += 1

    console.print(f"  [bright_green][+][/bright_green] [green]{mensaje}[/green] [dim green]completado[/dim green]")


# ══════════════════════════════════════════════════════════════
# COMPONENTES DE UI
# ══════════════════════════════════════════════════════════════

def mostrar_banner():
    """Muestra el banner principal de la aplicación."""
    banner_text = Text(BANNER_PRINCIPAL, style="bright_green")
    panel = Panel(
        Align.center(banner_text),
        border_style="green",
        subtitle=f"[dim green]v{APP_VERSION} │ ITBA[/dim green]",
        padding=(0, 2),
    )
    console.print(panel)
    console.print()


def mostrar_ascii(arte, titulo=None, color="green"):
    """Muestra ASCII art dentro de un panel opcional."""
    text = Text(arte, style=color)
    if titulo:
        panel = Panel(
            Align.center(text),
            title=f"[bright_green]{titulo}[/bright_green]",
            border_style="green",
            padding=(0, 2),
        )
        console.print(panel)
    else:
        console.print(Align.center(text))


def read_key():
    import sys
    if not sys.stdin.isatty():
        return None
    import tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
        if ch == '\x1b':
            ch2 = sys.stdin.read(2)
            return '\x1b' + ch2
        return ch
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def mostrar_menu(titulo, opciones, ascii_art=None):
    """Muestra un menú estilizado con navegación por flechas.

    Args:
        titulo: Título del menú
        opciones: Lista de strings con las opciones
        ascii_art: ASCII art opcional para mostrar junto al menú

    Returns:
        La opción seleccionada (string numérico)
    """
    import sys
    from rich.console import Group

    # Fallback si no hay TTY
    if not sys.stdin.isatty():
        if ascii_art:
            console.print(Text(ascii_art, style="dim green"), justify="center")
            console.print()
        
        table = Table(show_header=False, border_style="green", box=None, padding=(0, 2), expand=False)
        table.add_column("num", style="bright_green", width=4)
        table.add_column("opcion", style="green")
        for i, opcion in enumerate(opciones, 1):
            table.add_row(f"[{i}]", opcion)
            
        panel = Panel(table, title=f"[bold bright_green]═══ {titulo} ═══[/bold bright_green]", border_style="green", padding=(1, 3))
        console.print(Align.center(panel))
        console.print()
        
        while True:
            opcion = input_hacker("Seleccioná una opción")
            if opcion.isdigit() and 1 <= int(opcion) <= len(opciones):
                return opcion
            console.print("  [red]⚠ Opción inválida. Intentá de nuevo.[/red]")

    # Menú interactivo con flechas
    seleccionado = 0
    
    def get_renderable(sel):
        renderables = []
        if ascii_art:
            renderables.append(Align.center(Text(ascii_art, style="dim green")))
            renderables.append(Text(""))
            
        table = Table(show_header=False, border_style="green", box=None, padding=(0, 2), expand=False)
        table.add_column("cursor", style="bold bright_green", width=2)
        table.add_column("opcion", style="green")

        for i, opcion in enumerate(opciones):
            if i == sel:
                table.add_row(">", f"[bold bright_green]{opcion}[/bold bright_green]")
            else:
                table.add_row(" ", opcion)

        panel = Panel(
            table,
            title=f"[bold bright_green]═══ {titulo} ═══[/bold bright_green]",
            border_style="green",
            padding=(1, 3),
        )
        renderables.append(Align.center(panel))
        renderables.append(Text(""))
        renderables.append(Align.center(Text("Usa las flechas [↑] [↓] y presiona [ENTER]", style="dim green")))
        return Group(*renderables)

    with Live(get_renderable(seleccionado), console=console, auto_refresh=False, transient=True) as live:
        while True:
            key = read_key()
            if not key:
                break
            if key == '\x1b[A': # Arriba
                seleccionado = max(0, seleccionado - 1)
            elif key == '\x1b[B': # Abajo
                seleccionado = min(len(opciones) - 1, seleccionado + 1)
            elif key in ('\r', '\n'): # Enter
                return str(seleccionado + 1)
            elif key == '\x03': # Ctrl+C
                raise KeyboardInterrupt
            
            live.update(get_renderable(seleccionado), refresh=True)
            
    return str(seleccionado + 1)


def input_hacker(prompt):
    """Input estilizado con prompt hacker."""
    console.print(f"  [dim green]┌──([/dim green][bright_green]guardian[/bright_green][dim green])─[/dim green][dim green][[/dim green][green]{prompt}[/green][dim green]][/dim green]")
    try:
        valor = console.input(f"  [dim green]└──▶[/dim green] [bright_green]$ [/bright_green]")
    except (EOFError, KeyboardInterrupt):
        console.print()
        valor = ""
    return valor.strip()


def input_password(prompt):
    """Input para contraseñas (sin eco en pantalla)."""
    import getpass
    console.print(f"  [dim green]┌──([/dim green][bright_green]guardian[/bright_green][dim green])─[/dim green][dim green][[/dim green][green]{prompt}[/green][dim green]][/dim green]")
    console.print(f"  [dim green]└──▶[/dim green] [bright_green]$ [/bright_green]", end="")
    try:
        valor = getpass.getpass(prompt="")
    except (EOFError, KeyboardInterrupt):
        console.print()
        valor = ""
    return valor.strip()


def barra_fuerza_password(puntaje, total=5):
    """Muestra una barra de fuerza de contraseña.

    Args:
        puntaje: Puntaje actual (0 a total)
        total: Puntaje máximo
    """
    porcentaje = puntaje / total

    if porcentaje <= 0.2:
        color = "red"
        label = "MUY DÉBIL"
    elif porcentaje <= 0.4:
        color = "bright_red"
        label = "DÉBIL"
    elif porcentaje <= 0.6:
        color = "yellow"
        label = "REGULAR"
    elif porcentaje <= 0.8:
        color = "bright_green"
        label = "FUERTE"
    else:
        color = "bold bright_green"
        label = "MUY FUERTE"

    barra_llena = "█" * int(porcentaje * 20)
    barra_vacia = "░" * (20 - int(porcentaje * 20))

    console.print()
    console.print(f"  [dim green]Fuerza:[/dim green] [{color}]{barra_llena}{barra_vacia}[/{color}] [{color}]{label}[/{color}] [{color}]{puntaje}/{total}[/{color}]")
    console.print()


def mostrar_clima_panel(datos):
    """Muestra los datos del clima en un panel formateado.

    Args:
        datos: Dict con keys: ciudad, temperatura, humedad, viento, condicion
    """
    condicion = datos.get("condicion", "").lower()

    # Elegir ASCII art según condición
    if "lluvia" in condicion or "lluvioso" in condicion:
        arte = ASCII_LLUVIA
    elif "nieve" in condicion or "nevado" in condicion:
        arte = ASCII_NIEVE
    elif "nublado" in condicion or "nube" in condicion:
        arte = ASCII_NUBE
    else:
        arte = ASCII_SOL

    # Tabla de datos
    table = Table(show_header=False, border_style="green", box=None, padding=(0, 2))
    table.add_column("campo", style="dim green", width=16)
    table.add_column("valor", style="bright_green")

    table.add_row("[TEMP]", f"{datos.get('temperatura', 'N/A')}°C")
    table.add_row("[HUM ]", f"{datos.get('humedad', 'N/A')}%")
    table.add_row("[WIND]", f"{datos.get('viento', 'N/A')} km/h")
    table.add_row("[COND]", f"{datos.get('condicion', 'N/A')}")

    # Contenido del panel
    arte_text = Text(arte, style="dim green")

    panel = Panel(
        Align.center(
            Columns([Align.center(arte_text), table], padding=4, expand=False)
        ),
        title=f"[bold bright_green]═══ Clima en {datos.get('ciudad', '???')} ═══[/bold bright_green]",
        border_style="green",
        padding=(1, 3),
    )
    console.print(panel)


def mostrar_tabla_datos(titulo, columnas, filas):
    """Muestra una tabla estilizada con datos.

    Args:
        titulo: Título de la tabla
        columnas: Lista de nombres de columnas
        filas: Lista de listas con los datos
    """
    table = Table(
        title=f"[bold bright_green]{titulo}[/bold bright_green]",
        border_style="green",
        header_style="bold bright_green",
        row_styles=["green", "dim green"],
        padding=(0, 1),
    )

    for col in columnas:
        table.add_column(col, style="green")

    for fila in filas:
        table.add_row(*[str(v) for v in fila])

    console.print()
    console.print(Align.center(table))
    console.print()


def mostrar_estadistica(label, valor, icono="▸"):
    """Muestra una estadística individual."""
    console.print(f"  [dim green]{icono}[/dim green] [green]{label}:[/green] [bright_green]{valor}[/bright_green]")


def mostrar_consejo_ia(consejo, datos_clima=None):
    """Muestra el consejo de IA en un panel especial."""
    arte_text = Text(ASCII_ROBOT, style="dim green")

    consejo_text = Text()
    consejo_text.append("\n")
    consejo_text.append(consejo, style="green")
    consejo_text.append("\n")

    panel = Panel(
        Align.center(
            Columns([Align.center(arte_text), consejo_text], padding=4, expand=False)
        ),
        title="[bold bright_green]═══ Consejo de Vestimenta IA ═══[/bold bright_green]",
        subtitle="[dim green]Powered by Gemini AI[/dim green]",
        border_style="green",
        padding=(1, 3),
    )
    console.print(panel)


def mostrar_error(mensaje):
    """Muestra un mensaje de error."""
    console.print(f"\n  [red][X] ERROR:[/red] [bright_red]{mensaje}[/bright_red]\n")


def mostrar_exito(mensaje):
    """Muestra un mensaje de éxito."""
    console.print(f"\n  [bright_green][+] {mensaje}[/bright_green]\n")


def mostrar_info(mensaje):
    """Muestra un mensaje informativo."""
    console.print(f"\n  [cyan][i] {mensaje}[/cyan]\n")


def mostrar_separador():
    """Muestra un separador visual."""
    console.print(f"  [dim green]{'═' * 50}[/dim green]")


def pausar():
    """Pausa la ejecución hasta que el usuario presione Enter."""
    console.print()
    console.input("  [dim green]Presioná [bright_green]ENTER[/bright_green] para continuar...[/dim green] ")


def mostrar_despedida():
    """Muestra el mensaje de despedida."""
    limpiar_pantalla()
    console.print(Text(ASCII_DESPEDIDA, style="bright_green"), justify="center")
    typing_effect("  Gracias por usar GuardiánClima ITBA. ¡Hasta la próxima!", velocidad=0.04)
    console.print()

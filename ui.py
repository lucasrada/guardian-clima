# ══════════════════════════════════════════════════════════════
# GuardiánClima ITBA — Interfaz de Usuario
# ══════════════════════════════════════════════════════════════

import os
import sys
import time
import random

# ── Forzar UTF-8 en Windows ─────────────────────────────────
# Sin esto, la consola legacy de Windows usa cp1252 y no puede
# renderizar los caracteres Unicode (box-drawing, katakana, etc.)
if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    # reconfigure() solo existe en Python 3.7+, por eso el hasattr
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

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
# Definición de estilos personalizados para utilizar en las salidas por consola
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

BANNER_PRINCIPAL = r"""  ██████╗ ██╗   ██╗ █████╗ ██████╗ ██████╗ ██╗ █████╗ ███╗   ██╗
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
       ╚═════╝╚══════╝╚═╝╚═╝     ╚═╝╚═╝  ╚═╝"""

ASCII_SOL = r"""      \   |   /
       .-' '-.
    --|       |--
       '-._.-'
      /   |   \ """

ASCII_NUBE = r"""       .-~~~-.
     .-'       `-.
    /             \
   |               |
    \             /
     `-._______.-'"""

ASCII_LLUVIA = r"""       .-~~~-.
     .-'       `-.
    /             \
   |               |
    \             /
     `-._______.-'
      /  /  /  /
     /  /  /  /"""

ASCII_NIEVE = r"""       .-~~~-.
     .-'       `-.
    /             \
   |               |
    \             /
     `-._______.-'
      *  *  *  *
       *  *  *  *"""

ASCII_ESCUDO = r"""       __________
      /          \
     /   ______   \
    /   |      |   \
   |    |      |    |
   |    |      |    |
    \   |______|   /
     \            /
      \          /
       \________/"""

ASCII_ROBOT = r"""       +-------+
       | O   O |
       |  ---  |
       +---+---+
      +----+----+
      |    |    |
      |   A I   |
      |    |    |
      +----+----+
           |
          -+-"""

ASCII_GRAFICO = r"""       __
      |  |   __
    __|  |  |  |
   |  |  |  |  |   __
   |  |  |  |  |  |  |
   |__|__|__|__|__|__|"""

ASCII_HISTORIAL = r"""   +--------------+
   | +----------+ |
   | |          | |
   | |   [**]   | |
   | |          | |
   | +----------+ |
   +--------------+"""

ASCII_LOGIN = r"""   +-----------------+
   |  +---+          |
   |  | O |  > _     |
   |  +---+          |
   |  ***************|
   |                 |
   +-----------------+"""

ASCII_DESPEDIDA = r"""      *  .  *
   .    *    .
  *  HASTA   *
  .  PRONTO  .
  *  . * .   *
   .    *   .
      *  ."""


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
        # Retorno de carro para sobreescribir la línea y simular el efecto de escritura
        console.print(text, end="\r")
        time.sleep(velocidad)
    console.print()  # salto de línea final para no pisar lo que sigue


def efecto_matrix(duracion=3, ancho=None):
    """Efecto lluvia de caracteres estilo Matrix."""
    if ancho is None:
        ancho = console.width

    # Mezcla de 0/1 con katakana japonés para la estética Matrix
    chars = "01アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン"
    # Cada posición en 'columnas' es un contador: cuando > 0, esa columna está "cayendo"
    columnas = [0] * ancho
    # De más tenue a más brillante, simula la estela de la lluvia
    intensidades = ["dim green", "green", "bright_green", "bold bright_green"]

    inicio = time.time()

    # transient=True hace que al terminar se borre la animación de la pantalla
    with Live(console=console, refresh_per_second=15, transient=True) as live:
        while time.time() - inicio < duracion:
            lineas = []
            texto = Text()
            for col in range(ancho):
                # 10% de probabilidad de iniciar una nueva animación en la columna
                if random.random() < 0.1:
                    columnas[col] = random.randint(1, 4)

                if columnas[col] > 0:
                    char = random.choice(chars)
                    # A mayor contador, más brillante; cuando baja se va apagando
                    intensidad = intensidades[min(columnas[col] - 1, len(intensidades) - 1)]
                    texto.append(char, style=intensidad)
                    columnas[col] -= 1
                else:
                    texto.append(" ")  # columna apagada, espacio vacío

            live.update(texto)
            time.sleep(0.07)  # ~14 fps para que se vea fluido


def mostrar_spinner(mensaje, duracion=2):
    """Muestra un spinner animado con un mensaje."""
    # Caracteres braille que al rotar generan la animación del spinner
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    inicio = time.time()
    i = 0

    with Live(console=console, refresh_per_second=12, transient=True) as live:
        while time.time() - inicio < duracion:
            frame = frames[i % len(frames)]  # cicla entre los frames con módulo
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
    # Lectura de tecla cruda, sin esperar Enter — necesario para el menú interactivo
    import sys
    if not sys.stdin.isatty():
        return None  # si no hay terminal (ej: pipe), no podemos leer teclas

    if sys.platform == "win32":
        # En Windows usamos msvcrt que lee teclas directamente
        import msvcrt
        ch = msvcrt.getwch()
        if ch in ('\x00', '\xe0'):
            # Special key: read the second byte
            # Las teclas de dirección en Windows envían 2 bytes; conversión al formato ANSI
            ch2 = msvcrt.getwch()
            # H=arriba, P=abajo, K=izquierda, M=derecha → los convertimos a secuencias ANSI
            key_map = {'H': '\x1b[A', 'P': '\x1b[B', 'K': '\x1b[D', 'M': '\x1b[C'}
            return key_map.get(ch2, '')
        return ch
    else:
        # En Unix/Linux/Mac usamos tty+termios para poner la terminal en modo raw
        import tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)  # guardamos la config original
        try:
            tty.setraw(sys.stdin.fileno())  # modo raw: cada tecla se lee al instante
            ch = sys.stdin.read(1)
            if ch == '\x1b':
                # Si arranca con ESC, es una secuencia de escape (ej: flecha)
                ch2 = sys.stdin.read(2)
                return '\x1b' + ch2
            return ch
        finally:
            # Restauración de la configuración de la terminal para evitar estado inconsistente
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

    # Fallback si no hay TTY (ej: si se ejecuta en un pipe o en un IDE sin terminal)
    # En ese caso mostramos un menú clásico con números en vez de flechas
    if not sys.stdin.isatty():
        if ascii_art:
            console.print(Text(ascii_art, style="dim green"), justify="center")
        
        table = Table(show_header=False, border_style="green", box=None, padding=(0, 2), expand=False)
        table.add_column("num", style="bright_green", width=4)
        table.add_column("opcion", style="green")
        for i, opcion in enumerate(opciones, 1):
            table.add_row(f"[{i}]", opcion)
            
        panel = Panel(table, title=f"[bold bright_green]═══ {titulo} ═══[/bold bright_green]", border_style="green", padding=(0, 3))
        console.print(Align.center(panel))
        
        # Bucle hasta obtener una entrada numérica válida
        while True:
            opcion = input_hacker("Seleccioná una opción")
            if opcion.isdigit() and 1 <= int(opcion) <= len(opciones):
                return opcion
            console.print("  [red]⚠ Opción inválida. Intentá de nuevo.[/red]")

    # Lógica principal del menú interactivo con teclas de dirección
    seleccionado = 0  # índice del ítem que tiene el cursor
    
    def get_renderable(sel):
        # Arma todo el contenido visual del menú cada vez que cambia la selección
        renderables = []
        if ascii_art:
            renderables.append(Align.center(Text(ascii_art, style="dim green")))
            renderables.append(Text(""))
            
        table = Table(show_header=False, border_style="green", box=None, padding=(0, 2), expand=False)
        table.add_column("cursor", style="bold bright_green", width=2)
        table.add_column("opcion", style="green")

        for i, opcion in enumerate(opciones):
            if i == sel:
                # El ítem seleccionado se muestra con ">" y más brillante
                table.add_row(">", f"[bold bright_green]{opcion}[/bold bright_green]")
            else:
                table.add_row(" ", opcion)

        panel = Panel(
            table,
            title=f"[bold bright_green]═══ {titulo} ═══[/bold bright_green]",
            border_style="green",
            padding=(0, 3),
        )
        renderables.append(Align.center(panel))
        renderables.append(Text(""))
        renderables.append(Align.center(Text("Usa las flechas [↑] [↓] y presiona [ENTER]", style="dim green")))
        # Group junta todos los renderables en un solo bloque para Live
        return Group(*renderables)

    # auto_refresh=False porque nosotros controlamos cuándo redibujar (al apretar tecla)
    # transient=True para que al salir del menú se limpie el render
    with Live(get_renderable(seleccionado), console=console, auto_refresh=False, transient=True) as live:
        while True:
            key = read_key()  # Llamada bloqueante a la espera de una entrada por teclado
            if not key:
                break
            if key == '\x1b[A': # Arriba
                seleccionado = max(0, seleccionado - 1)  # no baja de 0
            elif key == '\x1b[B': # Abajo
                seleccionado = min(len(opciones) - 1, seleccionado + 1)  # no pasa del último
            elif key in ('\r', '\n'): # Enter
                return str(seleccionado + 1)  # devolvemos 1-indexed como string
            elif key == '\x03': # Ctrl+C
                raise KeyboardInterrupt
            
            # Redibujamos el menú con la nueva selección
            live.update(get_renderable(seleccionado), refresh=True)
            
    return str(seleccionado + 1)


def input_hacker(prompt):
    """Input estilizado con prompt hacker."""
    # Dibujamos un prompt estilo terminal hacker con bordes box-drawing
    console.print(f"  [dim green]┌──([/dim green][bright_green]guardian[/bright_green][dim green])─[/dim green][dim green][[/dim green][green]{prompt}[/green][dim green]][/dim green]")
    try:
        valor = console.input(f"  [dim green]└──▶[/dim green] [bright_green]$ [/bright_green]")
    except (EOFError, KeyboardInterrupt):
        valor = ""  # Si se interrumpe la entrada, se retorna una cadena vacía
    return valor.strip()


def input_password(prompt):
    """Input para contraseñas (sin eco en pantalla)."""
    import getpass
    console.print(f"  [dim green]┌──([/dim green][bright_green]guardian[/bright_green][dim green])─[/dim green][dim green][[/dim green][green]{prompt}[/green][dim green]][/dim green]")
    console.print(f"  [dim green]└──▶[/dim green] [bright_green]$ [/bright_green]", end="")
    try:
        # getpass oculta la entrada por teclado, adecuado para contraseñas
        valor = getpass.getpass(prompt="")
    except (EOFError, KeyboardInterrupt):
        valor = ""
    return valor.strip()


def barra_fuerza_password(puntaje, total=5):
    """Muestra una barra de fuerza de contraseña.

    Args:
        puntaje: Puntaje actual (0 a total)
        total: Puntaje máximo
    """
    porcentaje = puntaje / total  # normalizamos a 0.0 – 1.0

    # Escalonamos color y label según el porcentaje — de rojo a verde brillante
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

    # Barra de 20 chars: █ para lo lleno, ░ para lo vacío
    barra_llena = "█" * int(porcentaje * 20)
    barra_vacia = "░" * (20 - int(porcentaje * 20))

    console.print(f"  [dim green]Fuerza:[/dim green] [{color}]{barra_llena}{barra_vacia}[/{color}] [{color}]{label}[/{color}] [{color}]{puntaje}/{total}[/{color}]")


def mostrar_clima_panel(datos):
    """Muestra los datos del clima en un panel formateado.

    Args:
        datos: Dict con keys: ciudad, temperatura, humedad, viento, condicion
    """
    # Tabla de datos
    table = Table(show_header=False, border_style="green", box=None, padding=(0, 2))
    table.add_column("campo", style="dim green", width=16)
    table.add_column("valor", style="bright_green")

    table.add_row("Temperatura:", f"{datos.get('temperatura', 'N/A')}°C")
    table.add_row("Humedad:", f"{datos.get('humedad', 'N/A')}%")
    table.add_row("Viento:", f"{datos.get('viento', 'N/A')} km/h")
    table.add_row("Condición:", f"{datos.get('condicion', 'N/A')}")

    panel = Panel(
        Align.center(table),
        title=f"[bold bright_green]═══ Clima en {datos.get('ciudad', '???')} ═══[/bold bright_green]",
        border_style="green",
        padding=(0, 3),
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
        style="green",
        padding=(0, 1),
        show_lines=True,
    )

    for col in columnas:
        table.add_column(col, style="green", overflow="fold")

    for fila in filas:
        table.add_row(*[str(v) for v in fila])

    console.print(Align.center(table))


def mostrar_estadistica(label, valor, icono="▸"):
    """Muestra una estadística individual."""
    console.print(f"  [dim green]{icono}[/dim green] [green]{label}:[/green] [bright_green]{valor}[/bright_green]")


def mostrar_consejo_ia(consejo, datos_clima=None):
    """Muestra el consejo de IA en un panel especial."""
    consejo_text = Text()
    consejo_text.append("\n")
    consejo_text.append(consejo, style="green")
    consejo_text.append("\n")

    panel = Panel(
        Align.center(consejo_text),
        title="[bold bright_green]═══ Consejo de Vestimenta IA ═══[/bold bright_green]",
        subtitle="[dim green]Powered by Gemini AI[/dim green]",
        border_style="green",
        padding=(0, 3),
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
    console.input("  [dim green]Presioná [bright_green]ENTER[/bright_green] para continuar...[/dim green] ")


def mostrar_despedida():
    """Muestra el mensaje de despedida."""
    limpiar_pantalla()
    typing_effect("  Gracias por usar GuardiánClima ITBA.", velocidad=0.04)

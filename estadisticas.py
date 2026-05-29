# ══════════════════════════════════════════════════════════════
# GuardiánClima ITBA — Historial y Estadísticas
# ══════════════════════════════════════════════════════════════

import os
import csv
from collections import Counter

from config import ARCHIVO_HISTORIAL
from ui import (
    console,
    input_hacker,
    mostrar_tabla_datos,
    mostrar_estadistica,
    mostrar_error,
    mostrar_info,
    mostrar_ascii,
    mostrar_separador,
    pausar,
    ASCII_HISTORIAL,
    ASCII_GRAFICO,
)

# ── Ruta base del módulo ─────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# ══════════════════════════════════════════════════════════════
# CARGA DE DATOS
# ══════════════════════════════════════════════════════════════

def cargar_historial():
    """Lee el archivo CSV de historial global y devuelve una lista de dicts.

    Cada diccionario tiene las claves correspondientes a las columnas
    del CSV: fecha, hora, usuario, ciudad, temperatura, humedad,
    viento, condicion.

    Returns:
        list[dict]: Lista de registros del historial. Vacía si el
                    archivo no existe o está vacío.
    """
    ruta = os.path.join(BASE_DIR, ARCHIVO_HISTORIAL)
    try:
        with open(ruta, newline="", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)
            return list(lector)
    except FileNotFoundError:
        return []


# ══════════════════════════════════════════════════════════════
# HISTORIAL PERSONAL
# ══════════════════════════════════════════════════════════════

def menu_historial_personal(usuario):
    """Muestra el historial de consultas de un usuario.

    Permite filtrar las consultas solo por usuario o por usuario
    y ciudad. Los resultados se muestran en una tabla estilizada.

    Args:
        usuario (str): Nombre del usuario cuyo historial se consulta.
    """
    mostrar_ascii(ASCII_HISTORIAL, titulo="Historial Personal")
    mostrar_separador()

    # ── Submenú de filtrado ──────────────────────────────────
    console.print("\n  [bright_green][1][/bright_green] [green]Ver todo mi historial[/green]")
    console.print("  [bright_green][2][/bright_green] [green]Filtrar por ciudad[/green]\n")

    opcion = input_hacker("Seleccioná una opción")

    # Cargar historial completo
    historial = cargar_historial()

    if not historial:
        mostrar_info("No hay registros en el historial todavía.")
        pausar()
        return

    # ── Filtrar registros del usuario ────────────────────────
    registros = [r for r in historial if r.get("usuario", "").lower() == usuario.lower()]

    # ── Filtro adicional por ciudad ──────────────────────────
    if opcion == "2":
        ciudad = input_hacker("Ingresá el nombre de la ciudad")
        registros = [
            r for r in registros
            if r.get("ciudad", "").lower() == ciudad.strip().lower()
        ]

    # ── Verificar resultados ─────────────────────────────────
    if not registros:
        mostrar_info("No se encontraron consultas con los filtros seleccionados.")
        pausar()
        return

    # ── Construir filas para la tabla ────────────────────────
    columnas = ["Fecha", "Hora", "Ciudad", "Temp (°C)", "Humedad (%)", "Viento (km/h)", "Condición"]
    filas = [
        [
            r.get("fecha", ""),
            r.get("hora", ""),
            r.get("ciudad", ""),
            r.get("temperatura", ""),
            r.get("humedad", ""),
            r.get("viento", ""),
            r.get("condicion", ""),
        ]
        for r in registros
    ]

    mostrar_tabla_datos(f"Historial de {usuario}", columnas, filas)
    pausar()


# ══════════════════════════════════════════════════════════════
# ESTADÍSTICAS GLOBALES
# ══════════════════════════════════════════════════════════════

def menu_estadisticas_globales():
    """Calcula y muestra estadísticas globales del historial.

    Estadísticas mostradas:
      • Ciudad más consultada (con cantidad de consultas).
      • Total de consultas registradas.
      • Temperatura promedio global (con 1 decimal).
      • Tabla con el top 5 de ciudades más consultadas.
    """
    mostrar_ascii(ASCII_GRAFICO, titulo="Estadísticas Globales")
    mostrar_separador()

    historial = cargar_historial()

    # ── Historial vacío ──────────────────────────────────────
    if not historial:
        mostrar_info("No hay datos en el historial para generar estadísticas.")
        pausar()
        return

    # ── Cálculos ─────────────────────────────────────────────
    total_consultas = len(historial)

    # Conteo de ciudades
    ciudades = [r.get("ciudad", "Desconocida") for r in historial]
    conteo_ciudades = Counter(ciudades)
    ciudad_top, ciudad_top_count = conteo_ciudades.most_common(1)[0]

    # Temperatura promedio global
    temperaturas = []
    for r in historial:
        try:
            temperaturas.append(float(r.get("temperatura", 0)))
        except (ValueError, TypeError):
            pass  # Ignorar registros con temperatura inválida

    temp_promedio = sum(temperaturas) / len(temperaturas) if temperaturas else 0.0

    # ── Mostrar estadísticas ─────────────────────────────────
    console.print()
    mostrar_estadistica("Ciudad más consultada", f"{ciudad_top} ({ciudad_top_count} consultas)", icono="[#]")
    mostrar_estadistica("Total de consultas", str(total_consultas), icono="[*]")
    mostrar_estadistica("Temperatura promedio global", f"{temp_promedio:.1f}°C", icono="[+]")
    console.print()

    # ── Top 5 ciudades más consultadas ───────────────────────
    top_5 = conteo_ciudades.most_common(5)
    columnas = ["#", "Ciudad", "Consultas"]
    filas = [
        [str(i), ciudad, str(cantidad)]
        for i, (ciudad, cantidad) in enumerate(top_5, 1)
    ]

    mostrar_tabla_datos("Top 5 — Ciudades Más Consultadas", columnas, filas)
    pausar()

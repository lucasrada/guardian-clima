# ══════════════════════════════════════════════════════════════
# GuardiánClima ITBA — Módulo de Consulta Climática
# ══════════════════════════════════════════════════════════════

from __future__ import annotations

import os
import csv
import random
import hashlib
from datetime import datetime

from config import (
    USE_REAL_API,
    OPENWEATHER_API_KEY,
    OPENWEATHER_BASE_URL,
    OPENWEATHER_UNITS,
    OPENWEATHER_LANG,
    ARCHIVO_HISTORIAL,
)
from ui import (
    console,
    input_hacker,
    mostrar_spinner,
    mostrar_clima_panel,
    mostrar_error,
    mostrar_exito,
    mostrar_info,
    typing_effect,
    mostrar_ascii,
    ASCII_SOL,
)

# Ruta base del módulo (para ubicar archivos CSV junto al script)
_DIR_BASE = os.path.dirname(os.path.abspath(__file__))

# Condiciones climáticas posibles (en español)
_CONDICIONES = [
    "Soleado",
    "Nublado",
    "Lluvia ligera",
    "Lluvia fuerte",
    "Tormenta",
    "Nevado",
    "Parcialmente nublado",
]


# ══════════════════════════════════════════════════════════════
# CONSULTA MOCK (datos simulados)
# ══════════════════════════════════════════════════════════════

def consultar_clima_mock(ciudad: str) -> dict:
    """Genera datos climáticos simulados de forma determinista para una ciudad.

    Usa un hash de la ciudad como semilla para que la misma ciudad
    devuelva resultados consistentes entre ejecuciones.

    Args:
        ciudad: Nombre de la ciudad a consultar.

    Returns:
        Dict con keys: ciudad, temperatura, humedad, viento, condicion.
    """
    # Crear semilla determinista a partir del nombre de la ciudad
    semilla = int(hashlib.md5(ciudad.lower().encode("utf-8")).hexdigest(), 16)
    rng = random.Random(semilla)

    temperatura = round(rng.uniform(-5, 40), 1)
    humedad = rng.randint(20, 100)
    viento = round(rng.uniform(0, 50), 1)
    condicion = rng.choice(_CONDICIONES)

    return {
        "ciudad": ciudad.title(),
        "temperatura": temperatura,
        "humedad": humedad,
        "viento": viento,
        "condicion": condicion,
    }


# ══════════════════════════════════════════════════════════════
# CONSULTA REAL (OpenWeatherMap API)
# ══════════════════════════════════════════════════════════════

def consultar_clima_real(ciudad: str) -> dict | None:
    """Consulta el clima actual de una ciudad usando la API de OpenWeatherMap.

    Args:
        ciudad: Nombre de la ciudad a consultar.

    Returns:
        Dict con keys: ciudad, temperatura, humedad, viento, condicion,
        o None si ocurre un error.
    """
    try:
        import requests
    except ImportError:
        mostrar_error("El módulo 'requests' no está instalado. Ejecutá: pip install requests")
        return None

    params = {
        "q": ciudad,
        "appid": OPENWEATHER_API_KEY,
        "units": OPENWEATHER_UNITS,
        "lang": OPENWEATHER_LANG,
    }

    try:
        respuesta = requests.get(OPENWEATHER_BASE_URL, params=params, timeout=10)
        respuesta.raise_for_status()
        datos_api = respuesta.json()

        return {
            "ciudad": datos_api.get("name", ciudad.title()),
            "temperatura": round(datos_api["main"]["temp"], 1),
            "humedad": datos_api["main"]["humidity"],
            "viento": round(datos_api["wind"]["speed"] * 3.6, 1),  # m/s → km/h
            "condicion": datos_api["weather"][0]["description"].capitalize(),
        }

    except requests.exceptions.ConnectionError:
        mostrar_error("No se pudo conectar con el servidor. Verificá tu conexión a internet.")
    except requests.exceptions.Timeout:
        mostrar_error("La solicitud tardó demasiado. Intentá de nuevo más tarde.")
    except requests.exceptions.HTTPError as e:
        if respuesta.status_code == 401:
            mostrar_error("API Key inválida. Revisá tu configuración en config.py.")
        elif respuesta.status_code == 404:
            mostrar_error(f"Ciudad '{ciudad}' no encontrada. Verificá el nombre e intentá de nuevo.")
        else:
            mostrar_error(f"Error HTTP {respuesta.status_code}: {e}")
    except (KeyError, IndexError):
        mostrar_error("La respuesta de la API tiene un formato inesperado.")
    except Exception as e:
        mostrar_error(f"Error inesperado al consultar el clima: {e}")

    return None


# ══════════════════════════════════════════════════════════════
# DELEGADOR DE CONSULTA
# ══════════════════════════════════════════════════════════════

def consultar_clima(ciudad: str) -> dict | None:
    """Consulta el clima de una ciudad, delegando al modo mock o real.

    Usa la variable USE_REAL_API de config.py para decidir qué
    fuente de datos utilizar.

    Args:
        ciudad: Nombre de la ciudad a consultar.

    Returns:
        Dict con datos climáticos o None si hay error (solo en modo real).
    """
    if USE_REAL_API:
        return consultar_clima_real(ciudad)
    else:
        return consultar_clima_mock(ciudad)


# ══════════════════════════════════════════════════════════════
# HISTORIAL
# ══════════════════════════════════════════════════════════════

def guardar_en_historial(usuario: str, ciudad: str, datos: dict) -> None:
    """Guarda una consulta climática en el archivo de historial CSV.

    Si el archivo no existe, lo crea con la cabecera correspondiente.
    Cada registro incluye fecha, hora, usuario, ciudad y datos climáticos.

    Args:
        usuario: Nombre de usuario que realizó la consulta.
        ciudad: Ciudad consultada.
        datos: Dict con las claves temperatura, humedad, viento, condicion.
    """
    ruta_historial = os.path.join(_DIR_BASE, ARCHIVO_HISTORIAL)
    archivo_existe = os.path.isfile(ruta_historial)

    ahora = datetime.now()
    fecha = ahora.strftime("%Y-%m-%d")
    hora = ahora.strftime("%H:%M:%S")

    fila = [
        fecha,
        hora,
        usuario,
        ciudad,
        datos.get("temperatura", ""),
        datos.get("humedad", ""),
        datos.get("viento", ""),
        datos.get("condicion", ""),
    ]

    try:
        with open(ruta_historial, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            # Escribir cabecera solo si el archivo es nuevo
            if not archivo_existe:
                writer.writerow([
                    "fecha", "hora", "usuario", "ciudad",
                    "temperatura", "humedad", "viento", "condicion",
                ])
            writer.writerow(fila)
    except OSError as e:
        mostrar_error(f"No se pudo guardar en el historial: {e}")


# ══════════════════════════════════════════════════════════════
# MENÚ PRINCIPAL DE CONSULTA
# ══════════════════════════════════════════════════════════════

def menu_consultar_clima(usuario: str) -> None:
    """Flujo completo de consulta climática para el usuario.

    Muestra arte ASCII, solicita la ciudad, consulta el clima,
    presenta los resultados en un panel y guarda el registro
    en el historial.

    Args:
        usuario: Nombre del usuario que realiza la consulta.
    """
    # Mostrar arte del sol como encabezado
    mostrar_ascii(ASCII_SOL, titulo="Consulta Climática")
    console.print()

    # Solicitar ciudad al usuario
    ciudad = input_hacker("Ingresá el nombre de la ciudad")

    if not ciudad:
        mostrar_error("Debés ingresar un nombre de ciudad.")
        return

    # Mostrar animación de carga
    modo = "API real" if USE_REAL_API else "simulación"
    mostrar_spinner(f"Consultando clima en {ciudad} (modo {modo})...", duracion=2)
    console.print()

    # Consultar datos climáticos
    datos = consultar_clima(ciudad)

    if datos is None:
        mostrar_error("No se pudieron obtener los datos del clima.")
        return

    # Mostrar resultados en panel formateado
    mostrar_clima_panel(datos)
    console.print()

    if not USE_REAL_API:
        mostrar_info("Datos generados en modo simulación (mock). Activá USE_REAL_API en config.py para datos reales.")

    # Guardar consulta en el historial
    guardar_en_historial(usuario, datos["ciudad"], datos)
    mostrar_exito(f"Consulta guardada en el historial para '{datos['ciudad']}'.")

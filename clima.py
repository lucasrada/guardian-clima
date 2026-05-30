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
    input_hacker,
    mostrar_spinner,
    mostrar_clima_panel,
    mostrar_error,
    mostrar_exito,
    mostrar_info,
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

_CAMPOS_HISTORIAL = [
    "fecha",
    "hora",
    "usuario",
    "ciudad",
    "temperatura",
    "sensacion_termica",
    "humedad",
    "viento",
    "condicion",
]


def _detalle_error_openweather(respuesta) -> str:
    """Extrae un mensaje legible del cuerpo de error de OpenWeather."""
    try:
        datos = respuesta.json()
    except ValueError:
        datos = {}

    mensaje = datos.get("message") if isinstance(datos, dict) else None
    if mensaje:
        return str(mensaje)

    texto = getattr(respuesta, "text", "").strip()
    return texto[:200] if texto else "sin detalle adicional"


def _calcular_sensacion_termica_mock(temperatura: float, humedad: int, viento: float) -> float:
    """Estima una sensación térmica simple para el modo simulación."""
    sensacion = temperatura

    if temperatura <= 10 and viento > 10:
        sensacion -= min(6, viento / 12)
    elif temperatura >= 27 and humedad > 60:
        sensacion += min(7, (humedad - 60) / 8)
    elif viento > 25:
        sensacion -= 1.0

    return round(sensacion, 1)


def _asegurar_esquema_historial(ruta_historial: str) -> bool:
    """Actualiza historiales viejos para incluir sensacion_termica."""
    if not os.path.isfile(ruta_historial):
        return False

    with open(ruta_historial, newline="", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        campos_actuales = lector.fieldnames or []
        if campos_actuales == _CAMPOS_HISTORIAL:
            return True
        filas = list(lector)

    for fila in filas:
        if not fila.get("sensacion_termica"):
            fila["sensacion_termica"] = fila.get("temperatura", "")

    with open(ruta_historial, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=_CAMPOS_HISTORIAL)
        escritor.writeheader()
        for fila in filas:
            escritor.writerow({campo: fila.get(campo, "") for campo in _CAMPOS_HISTORIAL})

    return True


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
        Dict con keys: ciudad, temperatura, sensacion_termica, humedad,
        viento, condicion.
    """
    # Crear semilla determinista a partir del nombre de la ciudad
    semilla = int(hashlib.sha256(ciudad.lower().encode("utf-8")).hexdigest(), 16)
    rng = random.Random(semilla)  # nosec B311

    temperatura = round(rng.uniform(-5, 40), 1)
    humedad = rng.randint(20, 100)
    viento = round(rng.uniform(0, 50), 1)
    condicion = rng.choice(_CONDICIONES)
    sensacion_termica = _calcular_sensacion_termica_mock(temperatura, humedad, viento)

    return {
        "ciudad": ciudad.title(),
        "temperatura": temperatura,
        "sensacion_termica": sensacion_termica,
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
        Dict con keys: ciudad, temperatura, sensacion_termica, humedad,
        viento, condicion, o None si ocurre un error.
    """
    try:
        import requests
    except ImportError:
        mostrar_error("El módulo 'requests' no está instalado. Ejecutá: pip install requests")
        return None

    if not OPENWEATHER_API_KEY:
        mostrar_error(
            "OPENWEATHER_API_KEY no está configurada. "
            "Definila como variable de entorno o usá el modo simulación."
        )
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
        datos_main = datos_api["main"]
        temperatura = round(datos_main["temp"], 1)

        return {
            "ciudad": datos_api.get("name", ciudad.title()),
            "temperatura": temperatura,
            "sensacion_termica": round(datos_main.get("feels_like", temperatura), 1),
            "humedad": datos_main["humidity"],
            "viento": round(datos_api["wind"]["speed"] * 3.6, 1),  # m/s → km/h
            "condicion": datos_api["weather"][0]["description"].capitalize(),
        }

    except requests.exceptions.ConnectionError:
        mostrar_error("No se pudo conectar con el servidor. Verificá tu conexión a internet.")
    except requests.exceptions.Timeout:
        mostrar_error("La solicitud tardó demasiado. Intentá de nuevo más tarde.")
    except requests.exceptions.HTTPError as e:
        detalle = _detalle_error_openweather(respuesta)
        if respuesta.status_code == 401:
            mostrar_error(
                "OpenWeather rechazó la API key. "
                "Verificá OPENWEATHER_API_KEY/OPENWEATHERMAP_API_KEY en tu entorno o .env. "
                "Si la key es nueva, OpenWeather puede demorar unas horas en activarla. "
                f"Detalle: {detalle}"
            )
        elif respuesta.status_code == 404:
            mostrar_error(f"Ciudad '{ciudad}' no encontrada. Verificá el nombre e intentá de nuevo.")
        elif respuesta.status_code in (402, 403):
            mostrar_error(
                "OpenWeather respondió que la key no tiene acceso a este servicio. "
                f"Detalle: {detalle}"
            )
        else:
            mostrar_error(f"Error HTTP {respuesta.status_code}: {e}. Detalle: {detalle}")
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
        datos: Dict con las claves temperatura, sensacion_termica, humedad,
               viento, condicion.
    """
    ruta_historial = os.path.join(_DIR_BASE, ARCHIVO_HISTORIAL)

    try:
        archivo_existe = _asegurar_esquema_historial(ruta_historial)

        ahora = datetime.now()
        fila = {
            "fecha": ahora.strftime("%Y-%m-%d"),
            "hora": ahora.strftime("%H:%M:%S"),
            "usuario": usuario,
            "ciudad": ciudad,
            "temperatura": datos.get("temperatura", ""),
            "sensacion_termica": datos.get("sensacion_termica", datos.get("temperatura", "")),
            "humedad": datos.get("humedad", ""),
            "viento": datos.get("viento", ""),
            "condicion": datos.get("condicion", ""),
        }

        with open(ruta_historial, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=_CAMPOS_HISTORIAL)
            # Escribir cabecera solo si el archivo es nuevo
            if not archivo_existe:
                writer.writeheader()
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

    # Solicitar ciudad al usuario
    ciudad = input_hacker("Ingresá el nombre de la ciudad")

    if not ciudad:
        mostrar_error("Debés ingresar un nombre de ciudad.")
        return

    # Mostrar animación de carga
    modo = "API real" if USE_REAL_API else "simulación"
    mostrar_spinner(f"Consultando clima en {ciudad} (modo {modo})...", duracion=2)

    # Consultar datos climáticos
    datos = consultar_clima(ciudad)

    if datos is None:
        mostrar_error("No se pudieron obtener los datos del clima.")
        return

    # Mostrar resultados en panel formateado
    mostrar_clima_panel(datos)

    if not USE_REAL_API:
        mostrar_info("Datos generados en modo simulación (mock). Activá USE_REAL_API en config.py para datos reales.")

    # Guardar consulta en el historial
    guardar_en_historial(usuario, datos["ciudad"], datos)
    mostrar_exito(f"Consulta guardada en el historial para '{datos['ciudad']}'.")

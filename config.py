"""Configuración central de GuardiánClima."""

import os

_DIRECTORIO_BASE = os.path.dirname(os.path.abspath(__file__))


def _limpiar_valor_env(valor: str) -> str:
    """Normaliza valores leídos del entorno o de .env."""
    valor = valor.strip()
    if len(valor) >= 2 and valor[0] == valor[-1] and valor[0] in {"'", '"'}:
        return valor[1:-1].strip()
    return valor


def _cargar_dotenv(ruta=None) -> None:
    """Carga un .env simple sin agregar dependencias externas."""
    rutas = [ruta] if ruta else [
        os.path.join(os.getcwd(), ".env"),
        os.path.join(_DIRECTORIO_BASE, ".env"),
    ]

    for ruta_dotenv in dict.fromkeys(rutas):
        if not ruta_dotenv or not os.path.exists(ruta_dotenv):
            continue

        try:
            with open(ruta_dotenv, encoding="utf-8") as archivo:
                for linea in archivo:
                    linea = linea.strip()
                    if not linea or linea.startswith("#") or "=" not in linea:
                        continue
                    nombre, valor = linea.split("=", 1)
                    nombre = nombre.strip()
                    if nombre and nombre not in os.environ:
                        os.environ[nombre] = _limpiar_valor_env(valor)
        except OSError:
            pass


def _obtener_env(*nombres: str, default: str = "") -> str:
    """Devuelve el primer valor definido entre varios nombres de entorno."""
    for nombre in nombres:
        valor = os.getenv(nombre)
        if valor:
            return _limpiar_valor_env(valor)
    return default


_cargar_dotenv()

# ── Modo de operación ──────────────────────────────────────────
_TRUE_VALUES = {"1", "true", "yes", "y", "si", "sí"}
USE_REAL_API = _obtener_env("GUARDIAN_USE_REAL_API", default="false").lower() in _TRUE_VALUES

# ── API Keys ──────────────────────────────────────────────────
OPENWEATHER_API_KEY = _obtener_env(
    "OPENWEATHER_API_KEY",
    "OPENWEATHERMAP_API_KEY",
    "OPENWEATHER_APP_ID",
    "OPENWEATHERMAP_APPID",
)
GEMINI_API_KEY = _obtener_env("GEMINI_API_KEY")
GEMINI_MODEL = _obtener_env("GEMINI_MODEL", default="gemini-3.5-flash")

# ── OpenWeatherMap ────────────────────────────────────────────
OPENWEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
OPENWEATHER_UNITS = "metric"  # Celsius
OPENWEATHER_LANG = "es"

# ── Archivos de datos ────────────────────────────────────────
ARCHIVO_USUARIOS = "usuarios_simulados.csv"
ARCHIVO_HISTORIAL = "historial_global.csv"

# ── Información de la app ────────────────────────────────────
APP_NOMBRE = "GuardiánClima ITBA"
APP_VERSION = "1.0.0"

# ── Reglas de contraseña ─────────────────────────────────────
PASSWORD_MIN_LENGTH = 8
PASSWORD_CARACTERES_ESPECIALES = "!@#$%^&*()_+-=[]{}|;:',.<>?/~`"  # nosec B105

REGLAS_PASSWORD = [
    {
        "nombre": "Longitud mínima",
        "descripcion": f"Debe tener al menos {PASSWORD_MIN_LENGTH} caracteres",
        "recomendacion": "Usá una frase larga o combiná varias palabras"
    },
    {
        "nombre": "Letra mayúscula",
        "descripcion": "Debe contener al menos 1 letra mayúscula",
        "recomendacion": "Capitalizá la primera letra o usá mayúsculas intercaladas"
    },
    {
        "nombre": "Número",
        "descripcion": "Debe contener al menos 1 número",
        "recomendacion": "Agregá números al final o reemplazá letras (ej: 'a' → '4')"
    },
    {
        "nombre": "Carácter especial",
        "descripcion": f"Debe contener al menos 1 carácter especial ({PASSWORD_CARACTERES_ESPECIALES[:10]}...)",
        "recomendacion": "Agregá símbolos como !, @, #, $ entre palabras"
    },
    {
        "nombre": "No contener usuario",
        "descripcion": "No debe contener tu nombre de usuario",
        "recomendacion": "Evitá usar datos personales en tu contraseña"
    }
]

# ── Colores del tema ─────────────────────────────────────────
THEME_COLORS = {
    "primary": "green",
    "accent": "bright_green",
    "error": "red",
    "warning": "yellow",
    "info": "cyan",
    "muted": "dim green",
    "highlight": "bold bright_green",
}

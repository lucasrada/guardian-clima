"""Configuración central de GuardiánClima."""

import os

# ── Modo de operación ──────────────────────────────────────────
_TRUE_VALUES = {"1", "true", "yes", "y", "si", "sí"}
USE_REAL_API = os.getenv("GUARDIAN_USE_REAL_API", "false").strip().lower() in _TRUE_VALUES

# ── API Keys ──────────────────────────────────────────────────
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "").strip()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash").strip()

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

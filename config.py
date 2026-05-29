# ══════════════════════════════════════════════════════════════
# GuardiánClima ITBA — Configuración
# ══════════════════════════════════════════════════════════════

# ── Modo de operación ──────────────────────────────────────────
# Cambiar a True cuando tengas las API keys reales
USE_REAL_API = False

# ── API Keys ──────────────────────────────────────────────────
# Reemplazar con tus keys reales cuando actives USE_REAL_API
OPENWEATHER_API_KEY = "TU_API_KEY_AQUI"
GEMINI_API_KEY = "TU_API_KEY_AQUI"

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
PASSWORD_CARACTERES_ESPECIALES = "!@#$%^&*()_+-=[]{}|;:',.<>?/~`"

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

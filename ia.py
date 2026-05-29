# ══════════════════════════════════════════════════════════════
# GuardiánClima ITBA — Módulo de Consejo de Vestimenta IA
# ══════════════════════════════════════════════════════════════
#
# Genera consejos de vestimenta basados en datos climáticos.
# Puede usar la API de Gemini (modo real) o respuestas
# generadas localmente (modo mock).
# ══════════════════════════════════════════════════════════════

from config import USE_REAL_API, GEMINI_API_KEY
from ui import (
    console,
    input_hacker,
    mostrar_spinner,
    mostrar_consejo_ia,
    mostrar_error,
    mostrar_info,
     typing_effect,
    pausar,
)


# ══════════════════════════════════════════════════════════════
# CONSEJO MOCK (sin API)
# ══════════════════════════════════════════════════════════════

def consejo_vestimenta_mock(datos_clima):
    """Genera consejo de vestimenta contextual basado en datos climáticos.

    Analiza temperatura, humedad, viento y condición meteorológica
    para armar una recomendación completa y natural en español.

    Args:
        datos_clima: dict con keys: temperatura, humedad, viento,
                     condicion, ciudad.

    Returns:
        str: Consejo de vestimenta multi-línea formateado.
    """
    temperatura = datos_clima.get("temperatura", 20)
    humedad = datos_clima.get("humedad", 50)
    viento = datos_clima.get("viento", 10)
    condicion = datos_clima.get("condicion", "despejado").lower()
    ciudad = datos_clima.get("ciudad", "tu ciudad")

    # ── Consejo base según rango de temperatura ──────────────
    if temperatura < 5:
        ropa_base = (
            "Hace mucho frío, así que abrigate bien. Usá un abrigo "
            "pesado, bufanda, guantes y gorro de lana. Optá por "
            "capas térmicas interiores para mantener el calor corporal."
        )
        emoji_temp = ""
    elif temperatura < 15:
        ropa_base = (
            "El clima está fresco. Te recomiendo una campera abrigada, "
            "vestirte en capas y usar pantalón largo. Una remera "
            "térmica debajo es una gran idea para esta temperatura."
        )
        emoji_temp = ""
    elif temperatura < 25:
        ropa_base = (
            "La temperatura es agradable. Podés usar ropa liviana "
            "como jeans y una remera. Llevá una manga larga o buzo "
            "fino por si refresca, sobre todo a la tarde-noche."
        )
        emoji_temp = ""
    else:
        ropa_base = (
            "Hace calor, así que usá ropa fresca y holgada. "
            "No te olvides del protector solar y mantenete "
            "bien hidratado durante el día. Colores claros ayudan."
        )
        emoji_temp = ""

    # ── Consideraciones por condición climática ──────────────
    consejos_extra = []

    if "lluvia" in condicion or "lluvioso" in condicion or "tormenta" in condicion:
        consejos_extra.append(
            "Hay pronóstico de lluvia: llevá un paraguas y "
            "preferí calzado impermeable. Un impermeable o campera "
            "con capucha te va a salvar el día."
        )
    elif "nieve" in condicion or "nevado" in condicion:
        consejos_extra.append(
            "Se esperan nevadas: usá botas impermeables con "
            "suela antideslizante y ropa térmica reforzada."
        )
    elif "nublado" in condicion or "nube" in condicion:
        consejos_extra.append(
            "El cielo está nublado: aunque no llueva, llevá "
            "una campera liviana por las dudas."
        )

    # ── Consideraciones por viento ───────────────────────────
    if viento > 40:
        consejos_extra.append(
            "Hay vientos muy fuertes: usá un buen rompevientos "
            "y evitá accesorios que se puedan volar (gorros sueltos, "
            "bufandas largas)."
        )
    elif viento > 20:
        consejos_extra.append(
            "Hay viento moderado: un rompevientos o campera "
            "cortaviento sería ideal para estar cómodo."
        )

    # ── Consideraciones por humedad ──────────────────────────
    if humedad > 80:
        consejos_extra.append(
            "La humedad es alta: elegí ropa transpirable de "
            "algodón o materiales técnicos que sequen rápido. "
            "Evitá telas sintéticas pesadas."
        )
    elif humedad < 30:
        consejos_extra.append(
            "El ambiente está muy seco: hidratá bien tu piel "
            "y usá protector labial. Mantenete tomando agua."
        )

    # ── Armado del consejo final ─────────────────────────────
    lineas = [
        f"Consejo para {ciudad} ({temperatura}°C):",
        "",
        ropa_base,
    ]

    if consejos_extra:
        lineas.append("")
        for extra in consejos_extra:
            lineas.append(extra)

    lineas.append("")
    lineas.append("¡Vestite bien y disfrutá el día!")

    return "\n".join(lineas)


# ══════════════════════════════════════════════════════════════
# CONSEJO REAL (API de Gemini)
# ══════════════════════════════════════════════════════════════

def consejo_vestimenta_real(datos_clima):
    """Genera consejo de vestimenta usando la API de Google Gemini.

    Envía un prompt contextual en español con los datos climáticos
    y recibe un consejo generado por IA.

    Args:
        datos_clima: dict con keys: temperatura, humedad, viento,
                     condicion, ciudad.

    Returns:
        str: Consejo generado por Gemini, o None si hay un error.
    """
    try:
        import google.generativeai as genai

        genai.configure(api_key=GEMINI_API_KEY)
        modelo = genai.GenerativeModel("gemini-pro")

        temperatura = datos_clima.get("temperatura", "N/A")
        humedad = datos_clima.get("humedad", "N/A")
        viento = datos_clima.get("viento", "N/A")
        condicion = datos_clima.get("condicion", "N/A")
        ciudad = datos_clima.get("ciudad", "desconocida")

        prompt = (
            f"Sos un asistente de moda y clima amigable. Dá un consejo "
            f"práctico y breve de vestimenta para hoy basado en estos "
            f"datos meteorológicos:\n\n"
            f"- Ciudad: {ciudad}\n"
            f"- Temperatura: {temperatura}°C\n"
            f"- Humedad: {humedad}%\n"
            f"- Viento: {viento} km/h\n"
            f"- Condición: {condicion}\n\n"
            f"Respondé en español rioplatense (argentino), de forma "
            f"amigable y práctica. Incluí recomendaciones específicas "
            f"de prendas, calzado y accesorios. Máximo 6 líneas."
        )

        respuesta = modelo.generate_content(prompt)
        return respuesta.text

    except ImportError:
        mostrar_error(
            "El módulo 'google-generativeai' no está instalado. "
            "Instalalo con: pip install google-generativeai"
        )
        return None
    except Exception as e:
        mostrar_error(f"Error al conectar con Gemini: {e}")
        return None


# ══════════════════════════════════════════════════════════════
# FUNCIÓN PRINCIPAL DE CONSEJO
# ══════════════════════════════════════════════════════════════

def consejo_vestimenta(datos_clima):
    """Genera consejo de vestimenta, delegando a mock o API real.

    Usa la API de Gemini si USE_REAL_API está activado en config.
    En caso de fallo, cae automáticamente al modo mock.

    Args:
        datos_clima: dict con keys: temperatura, humedad, viento,
                     condicion, ciudad.

    Returns:
        str: Consejo de vestimenta generado.
    """
    if USE_REAL_API:
        resultado = consejo_vestimenta_real(datos_clima)
        if resultado:
            return resultado
        # Fallback al mock si la API falla
        mostrar_info("Usando modo offline para generar el consejo.")

    return consejo_vestimenta_mock(datos_clima)


# ══════════════════════════════════════════════════════════════
# MENÚ INTERACTIVO DE CONSEJO IA
# ══════════════════════════════════════════════════════════════

def menu_consejo_ia(ultimo_clima=None):
    """Menú interactivo para obtener consejos de vestimenta por IA.

    Si se proporciona ultimo_clima, lo usa directamente. Si no,
    ofrece al usuario ingresar datos manualmente.

    Args:
        ultimo_clima: dict opcional con datos del clima (temperatura,
                      humedad, viento, condicion, ciudad). Si es None,
                      se solicitan los datos al usuario.
    """
    # Mostrar el arte ASCII del robot IA

    # ── Obtener datos climáticos ─────────────────────────────
    if ultimo_clima:
        datos_clima = ultimo_clima
        mostrar_info(
            f"Usando datos del clima de {datos_clima.get('ciudad', '???')} "
            f"({datos_clima.get('temperatura', '?')}°C)"
        )
    else:
        # Preguntar si desea ingresar datos manualmente
        mostrar_info(
            "No hay datos de clima recientes. Podés ingresar "
            "los datos manualmente para recibir un consejo."
        )
        respuesta = input_hacker("¿Querés ingresar datos del clima? (s/n)")

        if respuesta.lower() not in ("s", "si", "sí"):
            mostrar_info("Volviendo al menú anterior.")
            pausar()
            return

        # Solicitar datos al usuario
        ciudad = input_hacker("Ciudad")
        if not ciudad:
            ciudad = "Buenos Aires"

        temp_str = input_hacker("Temperatura (°C)")
        try:
            temperatura = float(temp_str)
        except (ValueError, TypeError):
            mostrar_error("Temperatura inválida, usando 20°C por defecto.")
            temperatura = 20.0

        hum_str = input_hacker("Humedad (%)")
        try:
            humedad = int(hum_str)
        except (ValueError, TypeError):
            mostrar_error("Humedad inválida, usando 50% por defecto.")
            humedad = 50

        viento_str = input_hacker("Velocidad del viento (km/h)")
        try:
            viento = float(viento_str)
        except (ValueError, TypeError):
            mostrar_error("Viento inválido, usando 10 km/h por defecto.")
            viento = 10.0

        condicion = input_hacker("Condición (despejado/nublado/lluvia/nieve/tormenta)")
        if not condicion:
            condicion = "despejado"

        datos_clima = {
            "ciudad": ciudad,
            "temperatura": temperatura,
            "humedad": humedad,
            "viento": viento,
            "condicion": condicion,
        }

    # ── Generar el consejo ───────────────────────────────────
    mostrar_spinner("Analizando condiciones climáticas", duracion=1.5)
    mostrar_spinner("Generando consejo de vestimenta con IA", duracion=2)

    consejo = consejo_vestimenta(datos_clima)

    # ── Mostrar el consejo ───────────────────────────────────
    mostrar_consejo_ia(consejo, datos_clima)

    # Efecto de escritura para resaltar el consejo principal
    typing_effect(
        "  ✨ Consejo generado exitosamente. ¡Que tengas un gran día!",
        velocidad=0.03,
        estilo="bright_green",
    )

    pausar()

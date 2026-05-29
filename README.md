# GuardiánClima ITBA

GuardiánClima es una aplicación de consola desarrollada en Python que permite a los usuarios interactuar con datos meteorológicos, gestionar historiales de consulta, obtener estadísticas globales y recibir recomendaciones de vestimenta generadas por Inteligencia Artificial.

El proyecto fue diseñado con un fuerte enfoque en la experiencia de usuario en terminal, utilizando la librería `rich` para proveer una interfaz visualmente atractiva, interactiva y robusta.

## Características Principales

*   **Autenticación Segura:** Sistema de registro e inicio de sesión. Incluye una validación estricta de contraseñas con feedback en tiempo real y un indicador visual de seguridad (0 a 5 niveles).
*   **Consulta Climática:** Permite obtener el clima actual de cualquier ciudad. Puede operar de forma simulada (datos generados localmente) o mediante conexión real a la API de OpenWeatherMap.
*   **Historial y Estadísticas:** Guarda automáticamente cada consulta en archivos CSV. Los usuarios pueden consultar su historial personal (con opción de filtrado por ciudad) y visualizar estadísticas globales como la ciudad más buscada o la temperatura promedio.
*   **Asistente IA de Vestimenta:** Integración con Google Gemini para ofrecer consejos prácticos sobre qué ropa usar, basándose en la temperatura, humedad, condición climática y velocidad del viento.

## Requisitos del Sistema

*   Python 3.7 o superior (para soporte completo de codificación UTF-8 en terminal).
*   Las dependencias listadas en el archivo `requirements.txt`.

## Instalación

1.  Clonar el repositorio o descargar los archivos del proyecto.
2.  Instalar las dependencias necesarias ejecutando:

```bash
pip install -r requirements.txt
```

## Configuración

Antes de ejecutar la aplicación con datos reales, es necesario ajustar el archivo `config.py`:

1.  **Modo de operación:**
    Por defecto, la aplicación funciona en modo simulación para facilitar las pruebas sin consumir cuotas de API. Para activar las consultas reales, cambia la siguiente variable a `True`:
    ```python
    USE_REAL_API = True
    ```

2.  **API Keys:**
    Si activaste el modo real, deberás proveer tus propias claves de acceso:
    ```python
    OPENWEATHER_API_KEY = "TU_API_KEY_AQUI"
    GEMINI_API_KEY = "TU_API_KEY_AQUI"
    ```

## Uso

Para iniciar la aplicación, ejecuta el archivo principal desde la terminal:

```bash
python main.py
```

El sistema presentará un menú interactivo. Puedes navegar por las opciones utilizando las teclas de dirección (flechas arriba/abajo) y confirmar tu selección con la tecla Enter.

## Estructura del Proyecto

*   `main.py`: Punto de entrada de la aplicación; maneja el ciclo de vida y los menús principales.
*   `config.py`: Variables de configuración, claves de API, rutas de archivos y reglas de negocio.
*   `ui.py`: Motor gráfico de la aplicación. Gestiona animaciones, paneles, colores y la lectura interactiva de teclado.
*   `auth.py`: Lógica de gestión de usuarios, lectura/escritura en CSV y validación de contraseñas.
*   `clima.py`: Delegador de consultas climáticas (maneja la alternancia entre el modo simulado y la API real) y registro en el historial.
*   `estadisticas.py`: Módulo para el análisis y visualización de datos históricos, tanto personales como globales.
*   `ia.py`: Generador de consejos de vestimenta (soporta generación local basada en reglas o integración con Gemini).

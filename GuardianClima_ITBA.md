# Challenge Tecnológico Integrador: "GuardiánClima ITBA"

¡Bienvenidos al Challenge Tecnológico "GuardiánClima ITBA"!

Este desafío está diseñado para que, trabajando en equipo, desarrollen una aplicación de consola en Python que les permita interactuar con datos climáticos, implementar mecanismos de validación de contraseñas (incluyendo guía hacia opciones más seguras), analizar datos globales de uso y utilizar inteligencia artificial.

---

# Objetivo General

Desarrollar una aplicación de consola en Python llamada **"GuardiánClima ITBA"**.

La aplicación presentará un menú inicial para iniciar sesión o registrar nuevos usuarios. El proceso de registro pondrá un fuerte énfasis en la validación de contraseñas según criterios de seguridad establecidos, y guiará al usuario hacia la creación de opciones más seguras si su intento inicial no es suficiente.

Una vez autenticado, el usuario accederá a un menú principal para:

- Consultar el clima
- Guardar un historial global de consultas
- Generar estadísticas globales
- Ofrecer consejos de vestimenta mediante IA

---

# Menú de Acceso (Pre-Login)

## 1. Iniciar Sesión

- Solicitar nombre de usuario y contraseña.
- Leer el archivo `usuarios_simulados.csv`.
- Verificar credenciales.
- Si la autenticación es exitosa, proceder al Menú Principal.

---

## 2. Registrar Nuevo Usuario

- Solicitar un nuevo nombre de usuario.
- Verificar que no exista previamente.

### Validación de contraseña

La contraseña debe cumplir al menos 3 criterios mínimos de seguridad definidos por el grupo.

Ejemplo de mensaje:

> "Tu contraseña no cumple con [listar reglas incumplidas]. Para una contraseña más segura, considera usar [recomendaciones]."

---

# Menú Principal

## Opción 1 — Consultar Clima Actual

- Solicitar ciudad.
- Obtener datos usando OpenWeatherMap.
- Mostrar:
  - Temperatura
  - Humedad
  - Viento
  - Condición climática

Guardar datos en `historial_global.csv`.

---

## Opción 2 — Ver Historial Personal

- Filtrar historial por:
  - Usuario
  - Ciudad

---

## Opción 3 — Estadísticas Globales

Mostrar:

- Ciudad más consultada
- Total de consultas
- Temperatura promedio

### Gráficos sugeridos

- Barras
- Líneas
- Torta

---

## Opción 4 — Consejo IA

Usar Google Gemini para generar consejos de vestimenta según el clima.

---

# Stack Tecnológico

- Python 3.x
- requests
- google-generativeai
- csv

---

# APIs

## OpenWeatherMap

Endpoint:

```text
https://api.openweathermap.org/data/2.5/weather
```

## Gemini

Instalación:

```bash
pip install google-generativeai
```

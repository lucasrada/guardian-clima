import csv
import importlib
from pathlib import Path
from types import SimpleNamespace

import auth
import clima
import ia
import main
import requests


def test_guardar_usuario_hashea_password(tmp_path, monkeypatch):
    ruta = tmp_path / "usuarios.csv"
    monkeypatch.setattr(auth, "_RUTA_USUARIOS", str(ruta))

    auth.guardar_usuario("alice", "Clave123!")

    contenido = ruta.read_text(encoding="utf-8")
    assert "Clave123!" not in contenido
    assert "password_hash" in contenido

    usuarios = auth.cargar_usuarios()
    assert auth._verificar_password("Clave123!", usuarios["alice"])
    assert not auth._verificar_password("Clave124!", usuarios["alice"])


def test_migra_password_legacy_a_hash(tmp_path, monkeypatch):
    ruta = tmp_path / "usuarios.csv"
    ruta.write_text("usuario,password\nlegacy,Legacy123!\n", encoding="utf-8")
    monkeypatch.setattr(auth, "_RUTA_USUARIOS", str(ruta))

    usuarios = auth.cargar_usuarios()
    assert auth._verificar_password("Legacy123!", usuarios["legacy"])

    auth._actualizar_password_usuario("legacy", "Legacy123!")

    contenido = ruta.read_text(encoding="utf-8")
    assert "Legacy123!" not in contenido
    assert "password_hash" in contenido
    assert auth._verificar_password("Legacy123!", auth.cargar_usuarios()["legacy"])


def test_consultar_clima_mock_es_determinista():
    primera = clima.consultar_clima_mock("Buenos Aires")
    segunda = clima.consultar_clima_mock("buenos aires")

    assert primera == segunda
    assert set(primera) == {
        "ciudad",
        "temperatura",
        "sensacion_termica",
        "humedad",
        "viento",
        "condicion",
    }


def test_guardar_en_historial_crea_csv(tmp_path, monkeypatch):
    monkeypatch.setattr(clima, "_DIR_BASE", str(tmp_path))
    datos = {
        "temperatura": 21.5,
        "sensacion_termica": 20.2,
        "humedad": 70,
        "viento": 12.1,
        "condicion": "Nublado",
    }

    clima.guardar_en_historial("alice", "Buenos Aires", datos)

    ruta = tmp_path / clima.ARCHIVO_HISTORIAL
    with ruta.open(encoding="utf-8", newline="") as archivo:
        filas = list(csv.DictReader(archivo))

    assert len(filas) == 1
    assert filas[0]["usuario"] == "alice"
    assert filas[0]["ciudad"] == "Buenos Aires"
    assert filas[0]["temperatura"] == "21.5"
    assert filas[0]["sensacion_termica"] == "20.2"


def test_guardar_en_historial_migra_csv_legacy(tmp_path, monkeypatch):
    monkeypatch.setattr(clima, "_DIR_BASE", str(tmp_path))
    ruta = tmp_path / clima.ARCHIVO_HISTORIAL
    ruta.write_text(
        "fecha,hora,usuario,ciudad,temperatura,humedad,viento,condicion\n"
        "2026-05-30,10:00:00,admin,Córdoba,12.5,70,8,Nublado\n",
        encoding="utf-8",
    )

    clima.guardar_en_historial(
        "admin",
        "Buenos Aires",
        {
            "temperatura": 18.0,
            "sensacion_termica": 16.7,
            "humedad": 64,
            "viento": 19.8,
            "condicion": "Cielo claro",
        },
    )

    with ruta.open(encoding="utf-8", newline="") as archivo:
        filas = list(csv.DictReader(archivo))

    assert "sensacion_termica" in filas[0]
    assert filas[0]["sensacion_termica"] == "12.5"
    assert filas[1]["sensacion_termica"] == "16.7"


def test_api_real_sin_keys_falla_sin_llamar_servicios(monkeypatch):
    errores = []

    monkeypatch.setattr(clima, "OPENWEATHER_API_KEY", "")
    monkeypatch.setattr(clima, "mostrar_error", errores.append)
    assert clima.consultar_clima_real("Buenos Aires") is None

    monkeypatch.setattr(ia, "GEMINI_API_KEY", "")
    monkeypatch.setattr(ia, "mostrar_error", errores.append)
    assert ia.consejo_vestimenta_real({"ciudad": "Buenos Aires"}) is None

    assert any("OPENWEATHER_API_KEY" in error for error in errores)
    assert any("GEMINI_API_KEY" in error for error in errores)


def test_config_carga_dotenv_y_alias_openweather(tmp_path, monkeypatch):
    dotenv = tmp_path / ".env"
    dotenv.write_text(
        "\n".join(
            [
                "GUARDIAN_USE_REAL_API=true",
                'OPENWEATHERMAP_API_KEY="alias-key"',
                "GEMINI_API_KEY=gemini-key",
            ]
        ),
        encoding="utf-8",
    )

    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("GUARDIAN_USE_REAL_API", raising=False)
    monkeypatch.delenv("OPENWEATHER_API_KEY", raising=False)
    monkeypatch.delenv("OPENWEATHERMAP_API_KEY", raising=False)
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)

    config_path = Path(__file__).resolve().parents[1] / "config.py"
    spec = importlib.util.spec_from_file_location("config_dotenv_test", config_path)
    config_recargado = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config_recargado)

    assert config_recargado.USE_REAL_API is True
    assert config_recargado.OPENWEATHER_API_KEY == "alias-key"
    assert config_recargado.GEMINI_API_KEY == "gemini-key"


def test_detalle_error_openweather_usa_mensaje_json():
    respuesta = SimpleNamespace(
        json=lambda: {"cod": 401, "message": "Invalid API key"},
        text='{"cod":401}',
    )

    assert clima._detalle_error_openweather(respuesta) == "Invalid API key"


def test_menu_principal_tiene_acerca_de_y_sin_salida_directa(monkeypatch):
    captura = {}

    def menu_fake(titulo, opciones):
        captura["titulo"] = titulo
        captura["opciones"] = opciones
        return "6"

    monkeypatch.setattr(main, "limpiar_pantalla", lambda: None)
    monkeypatch.setattr(main, "mostrar_banner", lambda: None)
    monkeypatch.setattr(main, "mostrar_menu", menu_fake)
    monkeypatch.setattr(main, "typing_effect", lambda *args, **kwargs: None)
    monkeypatch.setattr(main.console, "print", lambda *args, **kwargs: None)

    assert main.menu_principal("admin") == "cerrar_sesion"
    assert captura["titulo"] == "Menú Principal"
    assert captura["opciones"] == [
        "[*] Consultar Clima Actual",
        "[*] Ver Historial Personal",
        "[*] Estadísticas Globales",
        "[*] Consejo de Vestimenta IA",
        "[*] Acerca de",
        "[-] Cerrar Sesión",
    ]
    assert not any("Salir" in opcion for opcion in captura["opciones"])


def test_consultar_clima_real_parsea_respuesta_openweather(monkeypatch):
    llamadas = []

    class RespuestaFake:
        def raise_for_status(self):
            return None

        def json(self):
            return {
                "name": "Buenos Aires",
                "main": {"temp": 18.26, "feels_like": 16.94, "humidity": 64},
                "wind": {"speed": 5.5},
                "weather": [{"description": "cielo claro"}],
            }

    def get_fake(url, params, timeout):
        llamadas.append((url, params, timeout))
        return RespuestaFake()

    monkeypatch.setattr(clima, "OPENWEATHER_API_KEY", "test-key")
    monkeypatch.setattr(requests, "get", get_fake)

    datos = clima.consultar_clima_real("Buenos Aires")

    assert datos == {
        "ciudad": "Buenos Aires",
        "temperatura": 18.3,
        "sensacion_termica": 16.9,
        "humedad": 64,
        "viento": 19.8,
        "condicion": "Cielo claro",
    }
    assert llamadas[0][1]["appid"] == "test-key"
    assert llamadas[0][1]["q"] == "Buenos Aires"
    assert llamadas[0][2] == 10


def test_consejo_mock_incluye_riesgos_climaticos():
    consejo = ia.consejo_vestimenta_mock(
        {
            "ciudad": "Buenos Aires",
            "temperatura": 12,
            "sensacion_termica": 8,
            "humedad": 85,
            "viento": 30,
            "condicion": "lluvia ligera",
        }
    )

    assert "paraguas" in consejo.lower()
    assert "rompevientos" in consejo.lower()
    assert "humedad" in consejo.lower()
    assert "sensación 8" in consejo.lower()


def test_extraer_texto_gemini_ignora_partes_no_texto():
    respuesta = SimpleNamespace(
        candidates=[
            SimpleNamespace(
                content=SimpleNamespace(
                    parts=[
                        SimpleNamespace(thought_signature="abc123"),
                        SimpleNamespace(text="Usá abrigo liviano."),
                    ]
                )
            )
        ]
    )

    assert ia._extraer_texto_gemini(respuesta) == "Usá abrigo liviano."

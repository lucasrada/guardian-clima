import csv

import auth
import clima
import ia


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
    assert set(primera) == {"ciudad", "temperatura", "humedad", "viento", "condicion"}


def test_guardar_en_historial_crea_csv(tmp_path, monkeypatch):
    monkeypatch.setattr(clima, "_DIR_BASE", str(tmp_path))
    datos = {
        "temperatura": 21.5,
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


def test_consejo_mock_incluye_riesgos_climaticos():
    consejo = ia.consejo_vestimenta_mock(
        {
            "ciudad": "Buenos Aires",
            "temperatura": 12,
            "humedad": 85,
            "viento": 30,
            "condicion": "lluvia ligera",
        }
    )

    assert "paraguas" in consejo.lower()
    assert "rompevientos" in consejo.lower()
    assert "humedad" in consejo.lower()

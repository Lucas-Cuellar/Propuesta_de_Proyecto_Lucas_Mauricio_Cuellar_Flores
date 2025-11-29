# config/monitor_config.py
"""
Módulo de configuración central del sistema.

Objetivo:
- Cargar configuración desde monitor_settings.yaml (si existe).
- Permitir sobrescribir TODO por variables de entorno para portabilidad.
- NO hardcodear rutas ni credenciales.

Prioridad de configuración:
1) Variables de entorno 2) YAML (monitor_settings.yaml) 3) Defaults seguros en código
"""
from dataclasses import dataclass
import os
from typing import Any

import yaml

# ----------------- utilidades internas -----------------
def _load_yaml() -> dict:
    """
    Carga el archivo monitor_settings.yaml ubicado en esta carpeta.
    Si no existe o falla la lectura, devuelve {}.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    yaml_path = os.path.join(base_dir, "monitor_settings.yaml")

    if not os.path.isfile(yaml_path):
        print("⚠ monitor_settings.yaml no encontrado. Se usarán variables de entorno y defaults.")
        return {}

    try:
        with open(yaml_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        print(f"📄 Config YAML cargado: {yaml_path}")
        return data
    except Exception as e:
        print(f"⚠ Error leyendo monitor_settings.yaml: {e}")
        return {}


def _get(cfg: dict, path: list[str], default: Any = None) -> Any:
    """
    Acceso seguro a campos anidados en el YAML.
    path = ["paths", "models_dir"] por ejemplo.
    """
    current: Any = cfg
    for key in path:
        if not isinstance(current, dict) or key not in current:
            return default
        current = current[key]
    return current


# ----------------- carga base -----------------

_cfg = _load_yaml()

# Raíz del proyecto (carpeta padre de config/)
CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CONFIG_DIR)

# ----------------- rutas de modelos y logs -----------------

# Primero intentamos leer del YAML
_yaml_models_dir = _get(_cfg, ["paths", "models_dir"], None)
_yaml_logs_dir = _get(_cfg, ["paths", "logs_dir"], None)

# Luego variables de entorno (tienen prioridad)
MODELS_DIR = os.getenv(
    "SOUND_MODELS_DIR",
    _yaml_models_dir if _yaml_models_dir else os.path.join(PROJECT_ROOT, "modelos"),
)

LOGS_DIR = os.getenv(
    "SOUND_LOGS_DIR",
    _yaml_logs_dir if _yaml_logs_dir else os.path.join(PROJECT_ROOT, "logs"),
)

# Asegurar que existan
os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

# ----------------- audio -----------------

# YAML
_yaml_rate = _get(_cfg, ["audio", "rate"], 44100)
_yaml_chunk_sec = _get(_cfg, ["audio", "chunk_duration_sec"], 2)

# Env override
RATE = int(os.getenv("AUDIO_RATE", _yaml_rate))
CHUNK_DURATION_SEC = int(os.getenv("AUDIO_CHUNK_DURATION_SEC", _yaml_chunk_sec))
CHUNK_SIZE = RATE * CHUNK_DURATION_SEC

# ----------------- monitoreo (cooldown) -----------------

_yaml_cooldown = _get(_cfg, ["monitoring", "alert_cooldown_sec"], 10)
ALERT_COOLDOWN_SEC = float(os.getenv("ALERT_COOLDOWN_SEC", _yaml_cooldown))

# ----------------- Telegram (ENV > YAML > default) -----------------
# ----------------- Telegram (ENV > YAML > default) -----------------

# YAML (lo que venga del monitor_settings.yaml)
_yaml_tel_token = _get(_cfg, ["telegram", "token"], "")
_yaml_tel_chat_id = _get(_cfg, ["telegram", "chat_id"], "")
_yaml_tel_timeout = _get(_cfg, ["telegram", "timeout"], 10)

# ENV tiene prioridad sobre YAML
TEL_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", _yaml_tel_token)
TEL_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", _yaml_tel_chat_id)
TEL_TIMEOUT = int(os.getenv("TELEGRAM_TIMEOUT", _yaml_tel_timeout))

# DEBUG para ver qué estás mandando REALMENTE
print(f"[DEBUG] TELEGRAM TOKEN: {'OK' if TEL_TOKEN else 'MISSING'}")
print(f"[DEBUG] TELEGRAM CHAT_ID: {TEL_CHAT_ID!r}")
print(f"[DEBUG] TELEGRAM TIMEOUT: {TEL_TIMEOUT}")

# Validación mínima
if not TEL_TOKEN:
    raise RuntimeError(
        "Config Telegram inválida: TOKEN vacío.\n"
        "Define TELEGRAM_BOT_TOKEN en el entorno o 'telegram.token' en monitor_settings.yaml"
    )

if not TEL_CHAT_ID:
    raise RuntimeError(
        "Config Telegram inválida: CHAT_ID vacío.\n"
        "Define TELEGRAM_CHAT_ID en el entorno o 'telegram.chat_id' en monitor_settings.yaml"
    )


@dataclass(frozen=True)
class TelegramConfig:
    token: str = TEL_TOKEN
    chat_id: str = TEL_CHAT_ID
    timeout: int = TEL_TIMEOUT


@dataclass(frozen=True)
class AudioConfig:
 
    rate: int = RATE
    chunk_size: int = CHUNK_SIZE
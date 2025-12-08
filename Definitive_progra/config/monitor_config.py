# config/monitor_config.py
"""
Módulo de configuración central.
Incluye: Rutas absolutas, Telegram y Email.
"""
from dataclasses import dataclass
import os
from typing import Any
import yaml

# --- Utilidades ---
def _load_yaml() -> dict:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    yaml_path = os.path.join(base_dir, "monitor_settings.yaml")
    if not os.path.isfile(yaml_path): return {}
    try:
        with open(yaml_path, "r", encoding="utf-8") as f: return yaml.safe_load(f) or {}
    except: return {}

def _get(cfg: dict, path: list[str], default: Any = None) -> Any:
    curr = cfg
    for k in path:
        if not isinstance(curr, dict) or k not in curr: return default
        curr = curr[k]
    return curr

_cfg = _load_yaml()

# --- 1. Rutas (Fix Absoluto) ---
CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CONFIG_DIR)

_def_models = _get(_cfg, ["paths", "models_dir"], "modelos")
_def_logs = _get(_cfg, ["paths", "logs_dir"], "logs")

MODELS_DIR = os.getenv("SOUND_MODELS_DIR", os.path.join(PROJECT_ROOT, _def_models))
LOGS_DIR = os.getenv("SOUND_LOGS_DIR", os.path.join(PROJECT_ROOT, _def_logs))

os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

# --- 2. Audio & Monitoreo ---
RATE = int(os.getenv("AUDIO_RATE", _get(_cfg, ["audio", "rate"], 44100)))
CHUNK_DURATION_SEC = float(os.getenv("AUDIO_CHUNK_DURATION_SEC", _get(_cfg, ["audio", "chunk_duration_sec"], 2)))
CHUNK_SIZE = int(RATE * CHUNK_DURATION_SEC)

ALERT_COOLDOWN_SEC = float(os.getenv("ALERT_COOLDOWN_SEC", _get(_cfg, ["monitoring", "alert_cooldown_sec"], 10)))
MIN_CONFIDENCE_ALERT = float(os.getenv("MIN_CONFIDENCE_THRESHOLD", _get(_cfg, ["monitoring", "min_confidence_threshold"], 0.85)))

@dataclass(frozen=True)
class AudioConfig:
    rate: int = RATE
    chunk_size: int = CHUNK_SIZE

# --- 3. Telegram ---
TEL_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", _get(_cfg, ["telegram", "token"], ""))
TEL_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", _get(_cfg, ["telegram", "chat_id"], ""))
TEL_TIMEOUT = int(os.getenv("TELEGRAM_TIMEOUT", _get(_cfg, ["telegram", "timeout"], 10)))

@dataclass(frozen=True)
class TelegramConfig:
    token: str = TEL_TOKEN
    chat_id: str = TEL_CHAT_ID
    timeout: int = TEL_TIMEOUT

# --- 4. Email (NUEVO) ---
EMAIL_SENDER = os.getenv("EMAIL_SENDER", _get(_cfg, ["email", "sender"], ""))
EMAIL_PASS = os.getenv("EMAIL_PASSWORD", _get(_cfg, ["email", "password"], ""))
EMAIL_DEST = os.getenv("EMAIL_RECIPIENT", _get(_cfg, ["email", "recipient"], ""))
EMAIL_TIMEOUT = int(os.getenv("EMAIL_TIMEOUT", _get(_cfg, ["email", "timeout"], 10)))
@dataclass(frozen=True)
class EmailConfig:
    sender: str = EMAIL_SENDER
    password: str = EMAIL_PASS
    recipient: str = EMAIL_DEST
    timeout: int = EMAIL_TIMEOUT
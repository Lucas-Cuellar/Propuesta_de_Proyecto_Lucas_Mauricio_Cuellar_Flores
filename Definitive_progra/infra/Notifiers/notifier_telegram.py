# notifier_telegram.py
"""
Notificador vía Telegram.

Responsabilidad:
- Construir mensaje de alerta
- Enviar mensaje mediante Telegram Bot API
- Manejar errores de red

Implementa BaseNotifier.
"""

import requests

from core.BaseNotifier import BaseNotifier        # si está en otra carpeta, ajusta este import
from config.monitor_config import TelegramConfig  # igual: ajusta ruta si está en /config


class TelegramNotifier(BaseNotifier):
    """
    Implementación de BaseNotifier para enviar alertas por Telegram.
    """

    def __init__(self, config: TelegramConfig | None = None) -> None:
        # Si no se pasa una config explícita, usamos la del módulo de config
        self._config = config or TelegramConfig()
        self._api_url = f"https://api.telegram.org/bot{self._config.token}/sendMessage"

    def notify(self, status: str, confidence: float) -> None:
        """
        Envía un mensaje al chat configurado con el estado detectado.

        Si falta token o chat_id, no hace nada (fail-safe) pero avisa por consola.
        """
        if not self._config.token or not self._config.chat_id:
            print("⚠️ Telegram sin token o chat_id. Revisa monitor_settings.yaml.")
            print(f"   token='{self._config.token}', chat_id='{self._config.chat_id}'")
            return

        message = self._build_message(status, confidence)
        payload = {
            "chat_id": self._config.chat_id,
            "text": message,
            "parse_mode": "Markdown",
        }

        print(f"📨 Intentando enviar alerta a Telegram (chat_id={self._config.chat_id})...")
        try:
            resp = requests.post(
                self._api_url,
                data=payload,
                timeout=self._config.timeout,
            )
            if resp.status_code == 200:
                print("✅ Notificación de Telegram enviada correctamente.")
            else:
                print(
                    f"⚠️ Error al enviar Telegram "
                    f"(código {resp.status_code}): {resp.text}"
                )
        except requests.exceptions.RequestException as e:
            print(f"❌ Error de red al enviar notificación: {e}")

    @staticmethod
    def _build_message(status: str, confidence: float) -> str:
        """Construye el texto del mensaje de alerta."""
        pct = confidence * 100
        return (
            "🚨 *ALERTA DE SISTEMA* 🚨\n\n"
            "Se ha detectado un comportamiento anómalo en el equipo.\n\n"
            f"Estado detectado: *{status.upper()}*\n"
            f"Confianza: *{pct:.2f}%*\n\n"
            "_Se recomienda revisión por parte del técnico._"
        )


def build_default_telegram_notifier() -> TelegramNotifier:
    """
    Fábrica del notificador por defecto.

    Usa la configuración definida en monitor_settings.yaml:
      telegram:
        token: ...
        chat_id: ...
        timeout: ...
    """
    cfg = TelegramConfig()
    if not cfg.token or not cfg.chat_id:
        print(
            "⚠️ Advertencia: TelegramConfig no tiene token/chat_id válidos.\n"
            "   Revisa la sección [telegram] de monitor_settings.yaml."
        )
    return TelegramNotifier(cfg)
# infra/notifier_composite.py
from core.BaseNotifier import BaseNotifier

class CompositeNotifier(BaseNotifier):
    """
    Agrupa múltiples notificadores (Telegram, Email, etc.) 
    y envía la alerta a todos ellos secuencialmente.
    """
    def __init__(self, notifiers: list[BaseNotifier]) -> None:
        self._notifiers = notifiers

    def notify(self, status: str, confidence: float) -> None:
        # Recorre la lista de notificadores y ejecuta cada uno
        for notifier in self._notifiers:
            try:
                notifier.notify(status, confidence)
            except Exception as e:
                # Si falla uno (ej. no hay internet para el correo), 
                # imprimimos el error pero NO detenemos al resto (ej. Telegram).
                print(f"⚠️ Error en un notificador secundario: {e}")
# core/monitor_controller.py
from __future__ import annotations
import threading
import time
from datetime import datetime
from typing import Callable

from core.BaseClassifier import BaseClassifier
from core.BaseNotifier import BaseNotifier
from core.BaseLogger  import BaseLogger
from config.monitor_config import ALERT_COOLDOWN_SEC, MIN_CONFIDENCE_ALERT


class MonitoringController:
    """
    Orquesta la lógica del monitoreo.
    Lógica separada:
    - Notificaciones: Continuas (siempre que supere el umbral).
    - Logs: Controlados por tiempo (Cooldown) para no saturar disco.
    """

    def __init__(
        self,
        classifier: BaseClassifier,
        notifier: BaseNotifier,
        logger: BaseLogger,
        cooldown_sec: float = ALERT_COOLDOWN_SEC,
        clock: Callable[[], float] | None = None,
    ) -> None:
        self._classifier = classifier
        self._notifier = notifier
        self._logger = logger
        self._cooldown = cooldown_sec
        self._clock = clock or time.time

        # Solo necesitamos controlar el tiempo del LOG
        self._last_log_time: float = 0.0

    def reset_session(self) -> None:
        self._last_log_time = 0.0

    def process_audio_chunk(self, audio_data) -> tuple[str, float]:
        status, confidence = self._classifier.predict(audio_data)

        if status == "DISFUNCIONAL":
            self._handle_alert_logic(status, confidence)

        return status, confidence

    def _handle_alert_logic(self, status: str, confidence: float) -> None:
        # 1. Filtro Maestro: Nadie pasa si la confianza es baja
        if confidence < MIN_CONFIDENCE_ALERT:
            return

        now = self._clock()
        timestamp = datetime.now()

        # =================================================
        # CAMINO A: NOTIFICACIONES (Telegram / Gmail)
        # =================================================
        # "Son continuas": No verificamos tiempo, solo disparamos.
        # (Esto enviará una alerta cada 2 segundos mientras dure la falla)
        threading.Thread(
            target=self._notifier.notify,
            args=(status, confidence),
            daemon=True,
        ).start()

        # =================================================
        # CAMINO B: LOGS (SQL / CSV)
        # =================================================
        # "Dependiendo del cooldown": Verificamos el tiempo.
        if now - self._last_log_time > self._cooldown:
            
            # Actualizamos el reloj del log
            self._last_log_time = now
            
            threading.Thread(
                target=self._logger.log_failure,
                args=(status, confidence, timestamp),
                daemon=True,
            ).start()
            
            print(f"💾 Falla registrada en BD (Cooldown activado por {self._cooldown}s)")
        else:
            print(f"⏳ Log ignorado por cooldown (Alerta enviada, pero no guardada)")
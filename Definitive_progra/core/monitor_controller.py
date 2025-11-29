# core/monitor_controller.py
import time
from datetime import datetime
from typing import Callable, Any

from core.interfaces import BaseClassifier, BaseNotifier
from core.logger_interface import BaseLogger


class MonitoringController:
    def __init__(
        self,
        classifier: BaseClassifier,
        notifier: BaseNotifier,
        logger: BaseLogger,
        cooldown_sec: float,
        clock: Callable[[], float] = time.time,
    ) -> None:
        self._classifier = classifier
        self._notifier = notifier
        self._logger = logger
        self._cooldown = cooldown_sec
        self._clock = clock

        self._last_alert_time: float = 0.0
        self._session_logged: bool = False

    def process_audio_chunk(self, audio_data: Any) -> tuple[str, float]:
        status, confidence = self._classifier.predict(audio_data)
        self._maybe_trigger_actions(status, confidence)
        return status, confidence

    def reset_session(self) -> None:
        self._session_logged = False

    def _maybe_trigger_actions(self, status: str, confidence: float) -> None:
        now = self._clock()

        if status != "DISFUNCIONAL":
            return

        if now - self._last_alert_time < self._cooldown:
            return

        self._last_alert_time = now
        self._notifier.notify(status, confidence)

        if not self._session_logged:
            self._logger.log_failure(status, confidence, datetime.now())
            self._session_logged = True

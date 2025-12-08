# infra/logger_composite.py
from datetime import datetime
from core.BaseLogger import BaseLogger

class CompositeLogger(BaseLogger):
    """
    Escribe el registro de falla en múltiples destinos (ej. CSV y SQL) simultáneamente.
    """
    def __init__(self, loggers: list[BaseLogger]) -> None:
        self._loggers = loggers

    def log_failure(self, status: str, confidence: float, timestamp: datetime) -> None:
        # Recorre la lista de loggers y guarda en cada uno
        for logger in self._loggers:
            try:
                logger.log_failure(status, confidence, timestamp)
            except Exception as e:
                print(f"⚠️ Error en logger secundario: {e}")
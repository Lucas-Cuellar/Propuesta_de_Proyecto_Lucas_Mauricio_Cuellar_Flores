# core/logger_interface.py
from abc import ABC, abstractmethod
from datetime import datetime

"""
Interfaz abstracta para el sistema de logging.

Responsabilidad:
- Permitir múltiples tipos de loggers (CSV, JSON, BaseDatos, etc.)
- Garantizar independencia del controlador respecto al formato de log.
"""

class BaseLogger(ABC):
    @abstractmethod
    def log_failure(self, status: str, confidence: float, timestamp: datetime) -> None:
        raise NotImplementedError

# core/logger_interface.py
from abc import ABC, abstractmethod
from datetime import datetime


class BaseLogger(ABC):
    @abstractmethod
    def log_failure(self, status: str, confidence: float, timestamp: datetime) -> None:
        raise NotImplementedError

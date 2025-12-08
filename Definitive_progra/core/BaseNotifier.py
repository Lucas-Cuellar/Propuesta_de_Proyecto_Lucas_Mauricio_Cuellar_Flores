# core/interfaces.py
from abc import ABC, abstractmethod

class BaseNotifier(ABC):
    @abstractmethod
    def notify(self, status: str, confidence: float) -> None:
        raise NotImplementedError
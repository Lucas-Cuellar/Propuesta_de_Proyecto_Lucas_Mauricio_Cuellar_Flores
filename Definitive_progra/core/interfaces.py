# core/interfaces.py
from abc import ABC, abstractmethod
import numpy as np


class BaseClassifier(ABC):
    @abstractmethod
    def load(self, model_path: str, params_path: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def predict(self, audio_data: np.ndarray) -> tuple[str, float]:
        raise NotImplementedError


class BaseNotifier(ABC):
    @abstractmethod
    def notify(self, status: str, confidence: float) -> None:
        raise NotImplementedError

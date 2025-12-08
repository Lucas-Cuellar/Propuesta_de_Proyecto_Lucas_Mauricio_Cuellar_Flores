# core/interfaces.py
from abc import ABC, abstractmethod
import numpy as np
"""
Define interfaces base del dominio.

Responsabilidad:
- Servir como contrato para clasificadores y notificadores.
- Garantizar que el controlador NO dependa de implementaciones concretas.

"""

class BaseClassifier(ABC):
    @abstractmethod
    def load(self, model_path: str, params_path: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def predict(self, audio_data: np.ndarray) -> tuple[str, float]:
        raise NotImplementedError




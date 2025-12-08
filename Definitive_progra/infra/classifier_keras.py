# infra/classifier_keras.py
import numpy as np
import tensorflow as tf

from core.BaseClassifier import BaseClassifier
from infra.audio_features import compute_mfcc, normalize_features, pad_or_trim
from config.monitor_config import RATE
"""
Clasificador basado en Keras (.h5 + preproc.npz)

Responsabilidad:
- Preprocesar audio
- Ejecutar el modelo de IA
- Entregar (clase, confianza)

Se conecta con:
- infra/audio_features
"""

class KerasSoundClassifier(BaseClassifier):
    def __init__(self) -> None:
        self._model: tf.keras.Model | None = None
        self._params: dict = {}
        self._labels: list[str] = []

    def load(self, model_path: str, params_path: str) -> bool:
        try:
            self._model = tf.keras.models.load_model(model_path)
            npz = np.load(params_path, allow_pickle=True)
            self._params = dict(npz)

            self._labels = list(
                self._params.get(
                    "labels",
                    ["AMBIENTE", "FUNCIONAL", "DISFUNCIONAL"],
                )
            )

            print("✅ Modelo Keras y parámetros cargados correctamente.")
            return True
        except Exception as e:
            print(f"❌ Error cargando modelo o parámetros: {e}")
            self._model = None
            return False

    def _preprocess(self, audio: np.ndarray) -> np.ndarray | None:
        if self._model is None or audio.size == 0:
            return None

        try:
            n_mfcc = int(self._params.get("n_mfcc", 20))

            mfcc = compute_mfcc(audio, RATE, n_mfcc)
            mean = float(self._params.get("mean", 0.0))
            std = float(self._params.get("std", 1.0))
            mfcc_norm = normalize_features(mfcc, mean, std)

            frames = mfcc_norm.T

            if "input_shape" in self._params:
                expected = tuple(self._params["input_shape"])
            else:
                expected = self._model.input_shape[1:]

            frames = pad_or_trim(frames, expected[0])

            out = np.expand_dims(frames, axis=0).astype(np.float32)

            if len(expected) == 3 and expected[2] == 1:
                out = np.expand_dims(out, axis=-1)

            return out
        except Exception as e:
            print(f"⚠️ Error en preprocesamiento: {e}")
            return None

    def predict(self, audio: np.ndarray) -> tuple[str, float]:
        if self._model is None:
            return "ERROR_MODELO", 0.0

        processed = self._preprocess(audio)
        if processed is None:
            return "ERROR_PREPROC", 0.0

        try:
            pred = self._model.predict(processed, verbose=0)[0]
            idx = int(np.argmax(pred))
            confidence = float(pred[idx])

            if 0 <= idx < len(self._labels):
                status = self._labels[idx].upper()
            else:
                status = f"CLASE_{idx}"

            return status, confidence
        except Exception as e:
            print(f"❌ Error en predicción: {e}")
            return "ERROR_PREDICC", 0.0

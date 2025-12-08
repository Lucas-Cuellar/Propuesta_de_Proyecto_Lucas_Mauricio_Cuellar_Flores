# infra/audio_features.py
import numpy as np
import librosa

"""
Responsabilidad:
- Preprocesar audio para el modelo Keras
- Mantener lógica DSP separada del clasificador
"""

def compute_mfcc(audio: np.ndarray, sr: int, n_mfcc: int) -> np.ndarray:
    return librosa.feature.mfcc(
        y=audio,
        sr=sr,
        n_mfcc=n_mfcc,
        n_fft=1024,
        hop_length=256,
    )


def normalize_features(mfcc: np.ndarray, mean: float, std: float) -> np.ndarray:
    if std == 0:
        std = 1.0
    return (mfcc - mean) / std


def pad_or_trim(frames: np.ndarray, target_frames: int) -> np.ndarray:
    current = frames.shape[0]
    if current < target_frames:
        pad = target_frames - current
        return np.pad(frames, ((0, pad), (0, 0)), mode="constant")
    return frames[:target_frames, :]

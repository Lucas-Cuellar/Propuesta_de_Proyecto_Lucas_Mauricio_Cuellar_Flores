# audio_features.py
import numpy as np
import librosa
from config import (
    SAMPLE_RATE,
    SAMPLES_PER_CHUNK,
    HOP_LENGTH_SAMPLES,
    N_MFCC,
)

def load_mono_audio(path: str):
    """Carga un audio mono a SAMPLE_RATE."""
    audio, sr = librosa.load(path, sr=SAMPLE_RATE, mono=True)
    return audio, sr

def generate_chunks(audio: np.ndarray):
    """Genera chunks solapados de tamaño fijo."""
    for start in range(0, len(audio) - SAMPLES_PER_CHUNK, HOP_LENGTH_SAMPLES):
        yield audio[start:start + SAMPLES_PER_CHUNK]

def extract_mfcc_features(audio_chunk: np.ndarray, sr: int):
    """
    Extrae MFCC de un chunk.
    Parámetros ajustados para balance entre detalle y robustez.
    """
    mfccs = librosa.feature.mfcc(
        y=audio_chunk,
        sr=sr,
        n_mfcc=N_MFCC,
        n_fft=1024,
        hop_length=256
    )
    return mfccs.T  # (frames, n_mfcc)

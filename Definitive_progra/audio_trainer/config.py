# config.py
import os

# Audio y segmentación
SAMPLE_RATE = 44100
CHUNK_DURATION_SEC = 2.0
HOP_DURATION_SEC = 0.5

SAMPLES_PER_CHUNK = int(SAMPLE_RATE * CHUNK_DURATION_SEC)
HOP_LENGTH_SAMPLES = int(SAMPLE_RATE * HOP_DURATION_SEC)

# Features
N_MFCC = 20

# Dataset / entrenamiento
TEST_FRACTION_PER_CLASS = 0.2
EPOCHS = 60
BATCH_SIZE = 32
CLASSES = ["ambiente", "funcional", "disfuncional"]

# Data augmentation
AUGMENT_NOISE_STD = 0.01
MIN_CHUNKS_WARNING = 5

# Modelos
MODELS_DIR = r"C:\Users\PERSONAL\Desktop\Ultimate_Progra\Definitive_progra\Muestras"

# Asegura que exista el directorio de modelos
os.makedirs(MODELS_DIR, exist_ok=True)

# data_pipeline.py
import numpy as np
from sklearn.preprocessing import OneHotEncoder

from config import (
    CLASSES,
    TEST_FRACTION_PER_CLASS,
    AUGMENT_NOISE_STD,
    MIN_CHUNKS_WARNING,
)
from audio_features import load_mono_audio, generate_chunks, extract_mfcc_features


def build_train_test_datasets(file_paths: dict):
    """
    Construye X_train, X_test, y_train, y_test listos para entrar a la CNN.
    - Split por clase y por tiempo (no mezcla chunks de la misma zona en train/test).
    - Data augmentation con ruido leve en train.
    - Normalización usando SOLO train.
    """

    X_train_list, y_train_list = [], []
    X_test_list,  y_test_list  = [], []

    # 1. Generar features por clase y separar train/test
    for class_idx, label_name in enumerate(CLASSES):
        audio_path = file_paths[label_name]
        print(f"[DATA] Procesando clase '{label_name}' desde: {audio_path}")

        audio, sr = load_mono_audio(audio_path)

        class_chunks = []
        for chunk in generate_chunks(audio):
            feats = extract_mfcc_features(chunk, sr)
            class_chunks.append(feats)

        n_chunks = len(class_chunks)
        if n_chunks < MIN_CHUNKS_WARNING:
            print(f"⚠ Advertencia: muy pocos fragmentos para la clase '{label_name}' ({n_chunks}).")

        # split por tiempo
        split_idx = int((1 - TEST_FRACTION_PER_CLASS) * n_chunks)
        train_chunks = class_chunks[:split_idx]
        test_chunks  = class_chunks[split_idx:]

        # Train: original + versión con ruido
        for feats in train_chunks:
            X_train_list.append(feats)
            y_train_list.append(class_idx)

            noise = AUGMENT_NOISE_STD * np.random.randn(*feats.shape)
            noisy_feats = feats + noise
            X_train_list.append(noisy_feats)
            y_train_list.append(class_idx)

        # Test: sin augment
        for feats in test_chunks:
            X_test_list.append(feats)
            y_test_list.append(class_idx)

    print(f"[DATA] Fragmentos de entrenamiento: {len(X_train_list)}")
    print(f"[DATA] Fragmentos de prueba: {len(X_test_list)}")

    X_train = np.array(X_train_list)
    X_test  = np.array(X_test_list)
    y_train = np.array(y_train_list)
    y_test  = np.array(y_test_list)

    # 2. One-hot consistente (train + test juntos)
    encoder = OneHotEncoder(sparse_output=False)
    y_all = np.concatenate([y_train, y_test])
    y_all_oh = encoder.fit_transform(y_all.reshape(-1, 1))
    y_train_oh = y_all_oh[:len(y_train)]
    y_test_oh  = y_all_oh[len(y_train):]

    # 3. Normalización con solo train
    mean = np.mean(X_train)
    std  = np.std(X_train)
    if std == 0:
        std = 1.0

    X_train_norm = (X_train - mean) / std
    X_test_norm  = (X_test  - mean) / std

    # 4. Añadir canal para CNN: (samples, h, w, 1)
    X_train_cnn = X_train_norm[..., np.newaxis]
    X_test_cnn  = X_test_norm[..., np.newaxis]
    input_shape = X_train_cnn.shape[1:]

    return X_train_cnn, X_test_cnn, y_train_oh, y_test_oh, mean, std, input_shape

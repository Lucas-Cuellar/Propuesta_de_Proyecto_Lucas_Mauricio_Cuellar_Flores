# trainer.py
import os
import numpy as np
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping

from config import (
    MODELS_DIR,
    CLASSES,
    EPOCHS,
    BATCH_SIZE,
)
from data_pipeline import build_train_test_datasets
from model_builder import build_cnn


def train_model(model_name: str, file_paths: dict, log_fn=print):
    """
    Entrena el modelo con los archivos indicados y guarda:
    - model.h5
    - preproc.npz
    Devuelve un diccionario con métricas y rutas útiles.
    """

    try:
        log = log_fn  # alias corto

        log("=" * 50)
        log(f"[TRAIN] Iniciando entrenamiento para modelo: {model_name}")
        log("=" * 50)

        # 1. Preparar datos
        X_train, X_test, y_train, y_test, mean, std, input_shape = \
            build_train_test_datasets(file_paths)

        log(f"[TRAIN] Input shape CNN: {input_shape}")

        # 2. Construir modelo
        model = build_cnn(input_shape)
        model.summary(print_fn=log)
        model.compile(
            optimizer="adam",
            loss="categorical_crossentropy",
            metrics=["accuracy"]
        )

        # 3. Directorio del modelo
        model_specific_dir = os.path.join(MODELS_DIR, model_name)
        os.makedirs(model_specific_dir, exist_ok=True)
        model_output_path  = os.path.join(model_specific_dir, "model.h5")
        params_output_path = os.path.join(model_specific_dir, "preproc.npz")

        log(f"[TRAIN] Archivos se guardarán en: {model_specific_dir}")

        # 4. Callbacks
        checkpoint = ModelCheckpoint(
            model_output_path,
            monitor="val_accuracy",
            mode="max",
            save_best_only=True,
            verbose=1
        )

        early_stop = EarlyStopping(
            monitor="val_loss",
            mode="min",
            patience=6,
            restore_best_weights=True,
            verbose=1
        )

        # 5. Entrenamiento
        log("[TRAIN] Iniciando ajuste del modelo...")
        model.fit(
            X_train, y_train,
            epochs=EPOCHS,
            batch_size=BATCH_SIZE,
            validation_data=(X_test, y_test),
            callbacks=[checkpoint, early_stop],
            verbose=2,
            shuffle=True
        )

        # 6. Evaluación final
        test_loss, test_acc = model.evaluate(X_test, y_test, verbose=0)
        log("-" * 50)
        log("[TRAIN] Resultado en conjunto de prueba:")
        log(f"   - Loss: {test_loss:.4f}")
        log(f"   - Accuracy: {test_acc * 100:.2f}%")
        log("-" * 50)

        # 7. Guardar parámetros de preprocesado
        log(f"[TRAIN] Guardando parámetros en: {params_output_path}")
        np.savez(
            params_output_path,
            labels=CLASSES,
            mean=mean,
            std=std,
            input_shape=input_shape
        )

        log("=" * 50)
        log("✅ Entrenamiento completado correctamente.")
        log("=" * 50)

        return {
            "success": True,
            "model_dir": model_specific_dir,
            "model_path": model_output_path,
            "params_path": params_output_path,
            "test_loss": float(test_loss),
            "test_accuracy": float(test_acc),
        }

    except Exception as e:
        log_fn(f"\n❌ ERROR FATAL DURANTE EL ENTRENAMIENTO: {e}")
        return {
            "success": False,
            "error": str(e),
        }

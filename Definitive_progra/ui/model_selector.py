# ui/model_selector.py
import tkinter as tk
from tkinter import ttk, messagebox
import os

from infra.classifier_keras import KerasSoundClassifier
from infra.notifier_telegram import build_default_telegram_notifier
from infra.logging_utils import CsvLogger
from ui.ui_monitoring import MonitoringApp
from config.monitor_config import MODELS_DIR, LOGS_DIR


class ModelSelector:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.models_list = self._scan_models()
        self.selected_model = tk.StringVar()
        self._setup_window()
        self._setup_styles()
        self._build_layout()

    def _setup_window(self) -> None:
        self.root.title("Selector de Modelo")
        self.root.geometry("450x250")
        self.root.configure(bg="#f0f0f0")
        self.root.resizable(False, False)

    def _setup_styles(self) -> None:
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Title.TLabel", font=("Helvetica", 14, "bold"))
        style.configure("Info.TLabel", font=("Helvetica", 10))

    def _build_layout(self) -> None:
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(expand=True, fill=tk.BOTH)

        ttk.Label(
            frame,
            text="Seleccionar Equipo a Monitorear",
            style="Title.TLabel",
            anchor="center",
        ).pack(pady=10)

        if not self.models_list:
            ttk.Label(
                frame,
                text=(
                    "No se encontraron modelos.\n"
                    "Primero entrena un modelo con la herramienta correspondiente."
                ),
                style="Info.TLabel",
                foreground="red",
                justify="center",
                anchor="center",
            ).pack(pady=10)
            return

        combobox = ttk.Combobox(
            frame,
            textvariable=self.selected_model,
            values=self.models_list,
            font=("Helvetica", 12),
            state="readonly",
        )
        combobox.pack(fill=tk.X, pady=20, ipady=5)
        combobox.current(0)

        ttk.Button(
            frame,
            text="Iniciar Monitoreo",
            command=self.launch_monitor,
        ).pack(fill=tk.X, ipady=10, pady=10)

    def _scan_models(self) -> list[str]:
        if not os.path.exists(MODELS_DIR):
            os.makedirs(MODELS_DIR, exist_ok=True)
            return []
        try:
            return [
                f
                for f in os.listdir(MODELS_DIR)
                if os.path.isdir(os.path.join(MODELS_DIR, f))
            ]
        except Exception as e:
            print(f"❌ Error escaneando modelos: {e}")
            return []

    def launch_monitor(self) -> None:
        model_name = self.selected_model.get()
        if not model_name:
            messagebox.showerror("Error", "Por favor selecciona un modelo.")
            return

        model_dir = os.path.join(MODELS_DIR, model_name)
        model_path = os.path.join(model_dir, "model.h5")
        params_path = os.path.join(model_dir, "preproc.npz")
        log_path = os.path.join(LOGS_DIR, f"log_fallas_{model_name}.csv")

        if not os.path.isfile(model_path) or not os.path.isfile(params_path):
            messagebox.showerror(
                "Archivos faltantes",
                f"Faltan 'model.h5' o 'preproc.npz' en:\n{model_dir}",
            )
            return

        classifier = KerasSoundClassifier()
        if not classifier.load(model_path, params_path):
            messagebox.showerror(
                "Error al cargar modelo",
                "No se pudo cargar el modelo. Revisa la consola para más detalles.",
            )
            return

        notifier = build_default_telegram_notifier()
        logger = CsvLogger(log_path)

        self.root.withdraw()
        monitor_root = tk.Toplevel(self.root)
        MonitoringApp(
            monitor_root,
            classifier=classifier,
            notifier=notifier,
            logger=logger,
            model_name=model_name,
        )

        monitor_root.protocol("WM_DELETE_WINDOW", self._close_all)

    def _close_all(self) -> None:
        print("Cerrando aplicación completa...")
        self.root.destroy()

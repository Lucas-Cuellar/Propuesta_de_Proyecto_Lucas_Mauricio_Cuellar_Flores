# ui/model_selector.py
import tkinter as tk
from tkinter import ttk, messagebox
import os

from infra.classifier_keras import KerasSoundClassifier
from infra.Notifiers.notifier_telegram import build_default_telegram_notifier
from infra.Notifiers.notifier_email import GmailNotifier
from infra.Notifiers.notifier_composite import CompositeNotifier

# Loggers
from infra.Loggers.logging_utils import CsvLogger
from infra.Loggers.logger_sqlite import SqliteLogger
from infra.Loggers.logger_composite import CompositeLogger

from ui.ui_monitoring import MonitoringApp
from config.monitor_config import MODELS_DIR, LOGS_DIR

class ModelSelector:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.models_list = self._scan_models()
        self.selected_model = tk.StringVar()
        self._setup_window()
        self._build_layout()

    def _setup_window(self) -> None:
        self.root.title("Selector de Modelo")
        self.root.geometry("450x250")
        ttk.Style().theme_use("clam")

    def _build_layout(self) -> None:
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(expand=True, fill=tk.BOTH)
        ttk.Label(frame, text="Seleccionar Equipo", font=("Helvetica", 12, "bold")).pack(pady=10)

        if not self.models_list:
            ttk.Label(frame, text="No se encontraron modelos.", foreground="red").pack()
            return

        c = ttk.Combobox(frame, textvariable=self.selected_model, values=self.models_list, state="readonly")
        c.pack(fill=tk.X, pady=10)
        c.current(0)
        ttk.Button(frame, text="Iniciar Monitoreo", command=self.launch_monitor).pack(fill=tk.X, pady=10)

    def _scan_models(self) -> list[str]:
        if not os.path.exists(MODELS_DIR): return []
        return [d for d in os.listdir(MODELS_DIR) if os.path.isdir(os.path.join(MODELS_DIR, d))]

    def launch_monitor(self) -> None:
        name = self.selected_model.get()
        if not name: return

        # Rutas de Modelo
        model_dir = os.path.join(MODELS_DIR, name)
        model_path = os.path.join(model_dir, "model.h5")
        params_path = os.path.join(model_dir, "preproc.npz")

        # Rutas de Logs (AMBAS)
        csv_path = os.path.join(LOGS_DIR, f"log_{name}.csv")
        db_path = os.path.join(LOGS_DIR, f"historial_{name}.db")

        # Cargar Modelo
        classifier = KerasSoundClassifier()
        if not classifier.load(model_path, params_path):
            messagebox.showerror("Error", "No se pudo cargar el modelo.")
            return

        # Notificadores
        notifiers = [build_default_telegram_notifier(), GmailNotifier()]
        notifier_system = CompositeNotifier(notifiers)

        # Loggers (AMBOS)
        logger_csv = CsvLogger(csv_path)
        logger_sql = SqliteLogger(db_path)
        # Agrupamos en CompositeLogger
        logger_system = CompositeLogger([logger_csv, logger_sql])

        # Lanzar App
        self.root.withdraw()
        monitor_root = tk.Toplevel(self.root)
        
        # Pasamos logger compuesto Y el diccionario de rutas para los botones
        MonitoringApp(
            monitor_root, 
            classifier, 
            notifier_system, 
            logger_system, 
            name,
            paths={"csv": csv_path, "db": db_path} # <--- RUTAS PARA LOS BOTONES
        )
        monitor_root.protocol("WM_DELETE_WINDOW", lambda: self.root.destroy())
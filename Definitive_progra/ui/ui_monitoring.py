# ui/ui_monitoring.py
import os
import threading
import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser

from core.BaseNotifier import BaseNotifier
from core.BaseClassifier  import BaseClassifier 
from core.BaseLogger import BaseLogger
from core.monitor_controller import MonitoringController
from audio.audio_monitor import AudioMonitor
from config.monitor_config import AudioConfig, ALERT_COOLDOWN_SEC
from ui.theme import configure_dark_theme
from ui.status_panel import StatusPanel
from ui.controls_panel import ControlsPanel

class MonitoringApp:
    def __init__(
        self,
        root: tk.Tk,
        classifier: BaseClassifier,
        notifier: BaseNotifier,
        logger: BaseLogger,
        model_name: str,
        paths: dict,  # <--- Recibimos las rutas aquí {"csv": ..., "db": ...}
    ) -> None:
        self.root = root
        self._logger = logger
        self._paths = paths  # Guardamos las rutas

        self._controller = MonitoringController(
            classifier, notifier, logger, cooldown_sec=ALERT_COOLDOWN_SEC
        )
        self._audio_monitor = AudioMonitor(AudioConfig(), callback=self._on_audio_chunk)
        self._status_panel = None
        self._controls = None

        self._setup_window(model_name)
        self._setup_theme()
        self._build_components()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def _setup_window(self, model_name: str) -> None:
        self.root.title(f"Monitor IA - {model_name.upper()}")
        self.root.geometry("500x600") # Un poco más alto para los botones extra
        self.root.configure(bg="#2E2E2E")
        self.root.resizable(False, False)

    def _setup_theme(self) -> None:
        style = ttk.Style()
        configure_dark_theme(style)

    def _build_components(self) -> None:
        ttk.Label(self.root, text="Monitoreo en tiempo real", style="Title.TLabel").pack(pady=20)
        self._status_panel = StatusPanel(self.root)
        
        # Conectamos los nuevos callbacks
        self._controls = ControlsPanel(
            parent=self.root,
            on_start=self.start_monitoring,
            on_stop=self.stop_monitoring,
            on_open_csv=lambda: self._open_file(self._paths.get("csv")),
            on_open_db=lambda: self._open_file(self._paths.get("db")),
        )

    def _on_audio_chunk(self, audio_data) -> None:
        self.root.after(0, lambda: self._update_ui(*self._controller.process_audio_chunk(audio_data)))

    def _update_ui(self, status: str, confidence: float) -> None:
        self._status_panel.update(status, confidence)

    def start_monitoring(self) -> None:
        self._controller.reset_session()
        print("--- Sesión iniciada ---")
        threading.Thread(target=self._audio_monitor.start, daemon=True).start()
        self._controls.set_running(True)
        self._status_panel.update("INICIANDO...", 0.0)

    def stop_monitoring(self) -> None:
        self._audio_monitor.stop()
        self._controls.set_running(False)
        self._status_panel.update("DETENIDO", 0.0)

    def _open_file(self, path: str | None) -> None:
        """Abre un archivo si existe."""
        if not path or not os.path.isfile(path):
            messagebox.showinfo("Archivo no encontrado", f"Aún no existe el archivo:\n{path}")
            return
        print(f"Abriendo: {path}")
        try:
            webbrowser.open(os.path.realpath(path))
        except Exception as e:
            print(f"❌ Error al abrir: {e}")

    def on_close(self) -> None:
        self.stop_monitoring()
        self.root.destroy()
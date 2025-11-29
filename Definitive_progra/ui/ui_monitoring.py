# ui/ui_monitoring.py
import os
import threading
import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser

from core.interfaces import BaseClassifier, BaseNotifier
from core.logger_interface import BaseLogger
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
    ) -> None:
        self.root = root
        self._logger = logger

        self._controller = MonitoringController(
            classifier=classifier,
            notifier=notifier,
            logger=logger,
            cooldown_sec=ALERT_COOLDOWN_SEC,
        )

        self._audio_monitor = AudioMonitor(
            AudioConfig(),
            callback=self._on_audio_chunk,
        )

        self._current_status = "DETENIDO"
        self._current_confidence = 0.0

        self._setup_window(model_name)
        self._setup_theme()
        self._build_components()

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def _setup_window(self, model_name: str) -> None:
        self.root.title(f"Monitor IA - [ {model_name.upper()} ]")
        self.root.geometry("500x550")
        self.root.configure(bg="#2E2E2E")
        self.root.resizable(False, False)

    def _setup_theme(self) -> None:
        style = ttk.Style()
        configure_dark_theme(style)

    def _build_components(self) -> None:
        title = ttk.Label(
            self.root,
            text="Monitoreo en tiempo real",
            style="Title.TLabel",
        )
        title.pack(pady=20)

        self._status_panel = StatusPanel(self.root)

        self._controls = ControlsPanel(
            parent=self.root,
            on_start=self.start_monitoring,
            on_stop=self.stop_monitoring,
            on_open_log=self.open_log_file,
        )

    def _on_audio_chunk(self, audio_data) -> None:
        def _process():
            status, conf = self._controller.process_audio_chunk(audio_data)
            self._update_status(status, conf)

        self.root.after(0, _process)

    def _update_status(self, status: str, confidence: float) -> None:
        self._current_status = status
        self._current_confidence = confidence
        self._status_panel.update(status, confidence)

    def start_monitoring(self) -> None:
        self._controller.reset_session()
        print("--- Sesión de monitoreo iniciada ---")

        threading.Thread(target=self._audio_monitor.start, daemon=True).start()
        self._controls.set_running(True)
        self._update_status("INICIANDO...", 0.0)

    def stop_monitoring(self) -> None:
        self._audio_monitor.stop()
        self._controls.set_running(False)
        self._update_status("DETENIDO", 0.0)

    def open_log_file(self) -> None:
        path = getattr(self._logger, "filepath", None)
        if not path:
            messagebox.showwarning(
                "Sin archivo de log",
                "El logger actual no expone una ruta de archivo.",
            )
            return

        if not os.path.isfile(path):
            messagebox.showinfo(
                "Historial vacío",
                "Todavía no hay registros de fallas.",
            )
            return

        print(f"Abriendo archivo de log: {path}")
        try:
            webbrowser.open(os.path.realpath(path))
        except Exception as e:
            print(f"❌ No se pudo abrir el log: {e}")

    def on_close(self) -> None:
        print("Cerrando aplicación de monitoreo...")
        self.stop_monitoring()
        self.root.destroy()

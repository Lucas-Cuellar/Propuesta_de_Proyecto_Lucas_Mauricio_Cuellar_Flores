# ui/controls_panel.py
import tkinter as tk
from tkinter import ttk
from typing import Callable


class ControlsPanel:
    def __init__(
        self,
        parent: tk.Widget,
        on_start: Callable[[], None],
        on_stop: Callable[[], None],
        on_open_log: Callable[[], None],
    ) -> None:
        controls_frame = ttk.Frame(parent, style="TFrame", padding=20)
        controls_frame.pack(fill=tk.X, padx=30, pady=10)

        self._start_button = ttk.Button(
            controls_frame,
            text="Iniciar Monitoreo",
            command=on_start,
        )
        self._start_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

        self._stop_button = ttk.Button(
            controls_frame,
            text="Detener",
            command=on_stop,
            state=tk.DISABLED,
        )
        self._stop_button.pack(side=tk.RIGHT, expand=True, fill=tk.X, padx=5)

        utils_frame = ttk.Frame(parent, style="TFrame", padding=20)
        utils_frame.pack(fill=tk.X, padx=30, side=tk.BOTTOM)

        self._log_button = ttk.Button(
            utils_frame,
            text="Abrir Historial de Fallas (CSV)",
            command=on_open_log,
        )
        self._log_button.pack(fill=tk.X)

    def set_running(self, running: bool) -> None:
        if running:
            self._start_button.config(state=tk.DISABLED)
            self._stop_button.config(state=tk.NORMAL)
        else:
            self._start_button.config(state=tk.NORMAL)
            self._stop_button.config(state=tk.DISABLED)

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
        on_open_csv: Callable[[], None],  # <--- Nuevo callback
        on_open_db: Callable[[], None],   # <--- Nuevo callback
    ) -> None:
        self._on_start = on_start
        self._on_stop = on_stop
        self._on_open_csv = on_open_csv
        self._on_open_db = on_open_db
        
        self.frame = ttk.LabelFrame(parent, text="Controles", padding=15)
        self.frame.pack(fill=tk.X, padx=20, pady=10)
        
        self._build_widgets()

    def _build_widgets(self) -> None:
        # Contenedor para botones de Estado
        btn_frame = ttk.Frame(self.frame)
        btn_frame.pack(fill=tk.X, pady=5)

        self.btn_start = ttk.Button(
            btn_frame, text="▶ INICIAR", command=self._on_start, width=15
        )
        self.btn_start.pack(side=tk.LEFT, padx=5)

        self.btn_stop = ttk.Button(
            btn_frame, text="⏹ DETENER", command=self._on_stop, width=15, state="disabled"
        )
        self.btn_stop.pack(side=tk.LEFT, padx=5)

        # Separador visual
        ttk.Separator(self.frame, orient="horizontal").pack(fill=tk.X, pady=10)

        # Contenedor para botones de Historial
        hist_frame = ttk.Frame(self.frame)
        hist_frame.pack(fill=tk.X)

        ttk.Label(hist_frame, text="Abrir Historial:", font=("Arial", 9)).pack(anchor="w")

        # Botón CSV
        ttk.Button(
            hist_frame, text="📄 Ver CSV (Excel)", command=self._on_open_csv
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2, pady=5)

        # Botón SQL
        ttk.Button(
            hist_frame, text="🗄️ Ver Base de Datos", command=self._on_open_db
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2, pady=5)

    def set_running(self, running: bool) -> None:
        if running:
            self.btn_start.config(state="disabled")
            self.btn_stop.config(state="normal")
        else:
            self.btn_start.config(state="normal")
            self.btn_stop.config(state="disabled")
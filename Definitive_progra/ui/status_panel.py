# ui/status_panel.py
import tkinter as tk
from tkinter import ttk

"""
Panel visual de estado:
- Semáforo (canvas)
- Texto de estado
- Texto de confianza

Responsabilidad:
- Mostrar visualmente el resultado del monitoreo.
- NO procesa audio ni notifica ni clasifica.
"""

_STATUS_STYLES = {
    "FUNCIONAL": ("#4CAF50", "Green.TLabel"),
    "AMBIENTE": ("#2196F3", "Blue.TLabel"),
    "DISFUNCIONAL": ("#F44336", "Red.TLabel"),
}

_DEFAULT_COLOR = "#404040"
_DEFAULT_STYLE = "Status.TLabel"


class StatusPanel:
    def __init__(self, parent: tk.Widget) -> None:
        self._frame = ttk.Frame(parent, style="TFrame", padding=20)
        self._frame.pack(fill=tk.X, padx=30)

        self._canvas = tk.Canvas(
            self._frame, width=150, height=150, bg="#2E2E2E", highlightthickness=0
        )
        self._light = self._canvas.create_oval(
            10, 10, 140, 140, fill=_DEFAULT_COLOR, outline="white", width=2
        )
        self._canvas.pack(pady=10)

        self._status_label = ttk.Label(
            self._frame, text="Estado: DETENIDO", style="Status.TLabel"
        )
        self._status_label.pack(pady=10)

        self._conf_label = ttk.Label(
            self._frame, text="Confianza: N/A", style="Conf.TLabel"
        )
        self._conf_label.pack(pady=5)

    def update(self, status: str, confidence: float) -> None:
        color, style = _STATUS_STYLES.get(
            status,
            (_DEFAULT_COLOR, _DEFAULT_STYLE),
        )
        self._canvas.itemconfig(self._light, fill=color)
        self._status_label.config(text=f"Estado: {status}", style=style)
        self._conf_label.config(text=f"Confianza: {confidence * 100:.2f}%")

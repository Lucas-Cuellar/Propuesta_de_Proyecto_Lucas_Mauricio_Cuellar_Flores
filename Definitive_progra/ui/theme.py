# ui/theme.py
from tkinter import ttk

"""
Define tema y estilos de Tkinter/ttk.

Responsabilidad:
- Configurar colores, tipografías y estilos reutilizables.
"""

BG = "#2E2E2E"
FG = "white"
GREEN = "#4CAF50"
RED = "#F44336"
BLUE = "#2196F3"
GRAY = "#555555"


def configure_dark_theme(style: ttk.Style) -> None:
    style.theme_use("clam")

    style.configure(".", background=BG, foreground=FG, font=("Helvetica", 10))
    style.configure("TFrame", background=BG)

    style.configure("Title.TLabel", font=("Helvetica", 18, "bold"))
    style.configure("Status.TLabel", font=("Helvetica", 20, "bold"))
    style.configure("Conf.TLabel", font=("Helvetica", 14))

    style.configure("Red.TLabel", foreground=RED, font=("Helvetica", 20, "bold"))
    style.configure("Green.TLabel", foreground=GREEN, font=("Helvetica", 20, "bold"))
    style.configure("Blue.TLabel", foreground=BLUE, font=("Helvetica", 20, "bold"))

    style.configure("TButton", font=("Helvetica", 12), padding=10, relief="flat")
    style.map(
        "TButton",
        foreground=[("active", "black")],
        background=[("!active", GRAY)],
    )

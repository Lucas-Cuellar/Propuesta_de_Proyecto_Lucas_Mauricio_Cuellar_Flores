# main.py
"""
Punto de entrada de la aplicación.

Responsabilidad:
- Crear la ventana raíz de Tkinter.
- Instanciar el ModelSelector.
- Iniciar el loop principal de la interfaz gráfica."""

import tkinter as tk
from ui.model_selector import ModelSelector


def main() -> None:
    """Inicializa la app gráfica y entra en el loop principal."""
    root = tk.Tk()
    ModelSelector(root)
    root.mainloop()


if __name__ == "__main__":
    main()

# app.py
import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
import queue
import threading
import sys

from config import CLASSES
from trainer import train_model

# --- Redirección de stdout a la GUI ---
class QueueHandler(queue.Queue):
    def write(self, msg):
        self.put(msg)
    def flush(self):
        pass


class TrainingApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Generador de Modelos de Sonido (IA)")
        self.root.geometry("700x750")

        self.audio_paths = {label: tk.StringVar() for label in CLASSES}

        self._setup_styles()
        self._create_widgets()
        self._setup_stdout_redirect()

    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TFrame", background="#f0f0f0")
        style.configure("TLabel", background="#f0f0f0", font=("Helvetica", 10))
        style.configure("Header.TLabel", background="#f0f0f0",
                        font=("Helvetica", 14, "bold"))
        style.configure("TButton", font=("Helvetica", 10, "bold"), padding=5)
        style.configure("TEntry", font=("Helvetica", 10))
        style.configure("Start.TButton", background="#4CAF50", foreground="white")
        style.map("Start.TButton", background=[("active", "#81C784")])
        style.configure("Log.TFrame", background="black")

    def _create_widgets(self):
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Nombre del modelo
        name_frame = ttk.Frame(main_frame)
        name_frame.pack(fill=tk.X, pady=10)
        ttk.Label(name_frame, text="Nombre del Equipo/Modelo:",
                  style="Header.TLabel").pack(side=tk.LEFT, padx=(0, 10))
        self.model_name_entry = ttk.Entry(name_frame, font=("Helvetica", 12), width=40)
        self.model_name_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.model_name_entry.insert(0, "Ejemplo_Motor_Bomba")
        ttk.Separator(main_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=15)

        # Archivos de audio
        files_frame = ttk.Frame(main_frame)
        files_frame.pack(fill=tk.X, pady=10)
        ttk.Label(files_frame, text="Archivos de Audio (Muestras):",
                  style="Header.TLabel").pack(anchor="w")

        for label in CLASSES:
            self._create_file_input(files_frame, label)

        # Botón de entrenamiento
        self.start_button = ttk.Button(
            main_frame,
            text="Comenzar Entrenamiento",
            command=self._start_training_thread,
            style="Start.TButton"
        )
        self.start_button.pack(fill=tk.X, pady=20, ipady=10)

        # Consola de log
        log_frame = ttk.Frame(main_frame, style="Log.TFrame", padding=2)
        log_frame.pack(fill=tk.BOTH, expand=True)
        self.log_widget = scrolledtext.ScrolledText(
            log_frame, wrap=tk.WORD,
            bg="black", fg="white",
            font=("Consolas", 10)
        )
        self.log_widget.pack(fill=tk.BOTH, expand=True)

    def _create_file_input(self, parent_frame, label: str):
        frame = ttk.Frame(parent_frame)
        frame.pack(fill=tk.X, pady=5)

        lbl = ttk.Label(frame, text=f"{label.capitalize()}:",
                        width=12, font=("Helvetica", 11, "bold"))
        lbl.pack(side=tk.LEFT, padx=5)

        entry = ttk.Entry(frame, textvariable=self.audio_paths[label],
                          state="readonly", width=60)
        entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        btn = ttk.Button(frame, text="Buscar...",
                         command=lambda: self._browse_file(label))
        btn.pack(side=tk.LEFT, padx=5)

    def _browse_file(self, label: str):
        file_path = filedialog.askopenfilename(
            title=f"Selecciona el audio para '{label.capitalize()}'",
            filetypes=[("Archivos de Audio", "*.wav *.mp3 *.m4a"),
                       ("Todos los archivos", "*.*")]
        )
        if file_path:
            self.audio_paths[label].set(file_path)
            print(f"[GUI] Archivo '{label}' cargado: {file_path}")

    def _setup_stdout_redirect(self):
        self.log_queue = QueueHandler()
        sys.stdout = self.log_queue
        self.root.after(100, self._poll_log_queue)

    def _poll_log_queue(self):
        while True:
            try:
                msg = self.log_queue.get_nowait()
                self.log_widget.insert(tk.END, msg)
                self.log_widget.see(tk.END)
            except queue.Empty:
                break
        self.root.after(100, self._poll_log_queue)

    def _start_training_thread(self):
        model_name = self.model_name_entry.get().strip()
        if not model_name or " " in model_name:
            print("❌ ERROR: El nombre del equipo no puede estar vacío ni contener espacios.")
            messagebox.showerror(
                "Error",
                "El nombre del equipo no puede estar vacío ni contener espacios. "
                "Usa guiones bajos (_)."
            )
            return

        file_paths = {label: var.get() for label, var in self.audio_paths.items()}
        if any(not path for path in file_paths.values()):
            print("❌ ERROR: Debes seleccionar los 3 archivos de audio.")
            messagebox.showerror(
                "Error",
                "Debes seleccionar los 3 archivos de audio (ambiente, funcional, disfuncional)."
            )
            return

        self.start_button.config(
            text="Entrenando... (Esto puede tardar varios minutos)",
            state=tk.DISABLED
        )

        # Hilo para no congelar la GUI
        threading.Thread(
            target=self._run_training,
            args=(model_name, file_paths),
            daemon=True
        ).start()

    def _run_training(self, model_name: str, file_paths: dict):
        # Usa train_model; los prints ya van al log de la GUI
        result = train_model(model_name, file_paths, log_fn=print)

        if result.get("success"):
            msg = (
                f"Entrenamiento completado.\n"
                f"Modelo guardado en:\n{result['model_path']}\n"
                f"Parámetros en:\n{result['params_path']}\n"
                f"Accuracy en test: {result['test_accuracy'] * 100:.2f}%"
            )
            self.root.after(0, lambda: messagebox.showinfo("Éxito", msg))
        else:
            self.root.after(
                0,
                lambda: messagebox.showerror(
                    "Error de Entrenamiento",
                    f"Ocurrió un error: {result.get('error', 'Desconocido')}"
                )
            )

        self.root.after(0, self._reactivate_button)

    def _reactivate_button(self):
        self.start_button.config(text="Comenzar Entrenamiento", state=tk.NORMAL)


if __name__ == "__main__":
    root = tk.Tk()
    app = TrainingApp(root)
    root.mainloop()


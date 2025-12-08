# infra/logger_sqlite.py
import sqlite3
from datetime import datetime
from core.BaseLogger import BaseLogger

class SqliteLogger(BaseLogger):
    """
    Logger SQL optimizado para coincidir con el formato Excel (CSV).
    Columnas: Fecha | Hora | Estado | Confianza (%)
    """

    def __init__(self, db_path: str) -> None:
        self.db_path = db_path
        self.filepath = db_path # Necesario para que el botón "Abrir" funcione
        self._init_db()

    def _init_db(self) -> None:
        """Crea la tabla con columnas separadas para fecha y hora."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Creamos la tabla exactamente con el orden que pediste
            # (El 'id' se deja por buena práctica en SQL, pero no afecta tus datos)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS fallas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    Fecha TEXT NOT NULL,
                    Hora TEXT NOT NULL,
                    Estado TEXT NOT NULL,
                    Confianza_Porcentaje REAL NOT NULL
                )
            """)
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"❌ Error inicializando SQL: {e}")

    def log_failure(self, status: str, confidence: float, timestamp: datetime) -> None:
        """
        Procesa los datos antes de guardar para igualar al Excel.
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # 1. Separamos Fecha y Hora (Igual que en tu CSV)
            fecha_str = timestamp.strftime("%Y-%m-%d") # Ej: 2025-12-04
            hora_str = timestamp.strftime("%H:%M:%S")  # Ej: 15:30:00

            # 2. Convertimos decimal a porcentaje (0.98 -> 98.0)
            confianza_pct = round(confidence * 100, 2)

            # 3. Insertamos en orden
            cursor.execute(
                """
                INSERT INTO fallas (Fecha, Hora, Estado, Confianza_Porcentaje) 
                VALUES (?, ?, ?, ?)
                """,
                (fecha_str, hora_str, status, confianza_pct)
            )
            
            conn.commit()
            conn.close()
            print(f"✅ Guardado en SQL: {status} ({confianza_pct}%)")

        except Exception as e:
            print(f"❌ Error guardando en SQL: {e}")
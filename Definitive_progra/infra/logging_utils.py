# infra/logging_utils.py
from dataclasses import dataclass
from datetime import datetime
import csv
import os

from core.logger_interface import BaseLogger


@dataclass(frozen=True)
class LogEntry:
    timestamp: datetime
    status: str
    confidence: float

    @property
    def as_row(self) -> list[str]:
        return [
            self.timestamp.strftime("%Y-%m-%d"),
            self.timestamp.strftime("%H:%M:%S"),
            self.status,
            f"{self.confidence * 100:.2f}%",
        ]


class CsvLogger(BaseLogger):
    def __init__(self, filepath: str) -> None:
        self.filepath = filepath
        self.header = ["Fecha", "Hora", "Estado_Detectado", "Confianza"]

    def _ensure_exists(self) -> None:
        if not os.path.isfile(self.filepath):
            try:
                with open(self.filepath, "w", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f, delimiter=";")
                    writer.writerow(self.header)
                print(f"📄 Log creado en: {self.filepath}")
            except Exception as e:
                print(f"❌ Error creando archivo de log: {e}")

    def log_failure(self, status: str, confidence: float, timestamp: datetime) -> None:
        self._ensure_exists()
        entry = LogEntry(timestamp, status, confidence)

        try:
            with open(self.filepath, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f, delimiter=";")
                writer.writerow(entry.as_row)
            print(f"✅ Falla registrada en {self.filepath}")
        except Exception as e:
            print(f"❌ Error escribiendo en el log: {e}")

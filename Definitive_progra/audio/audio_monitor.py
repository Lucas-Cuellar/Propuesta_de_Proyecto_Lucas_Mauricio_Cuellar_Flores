# audio/audio_monitor.py
import numpy as np
import pyaudio
from typing import Callable

from config.monitor_config import AudioConfig


class AudioMonitor:
    def __init__(
        self,
        audio_config: AudioConfig,
        callback: Callable[[np.ndarray], None] | None,
    ) -> None:
        self._rate = audio_config.rate
        self._chunk_size = audio_config.chunk_size
        self._callback = callback

        self._p = pyaudio.PyAudio()
        self._stream: pyaudio.Stream | None = None
        self.is_running: bool = False
        self._audio_buffer = np.array([], dtype=np.float32)

    def _stream_callback(self, in_data, frame_count, time_info, status):
        audio_chunk = np.frombuffer(in_data, dtype=np.float32).astype(np.float32)
        self._audio_buffer = np.concatenate([self._audio_buffer, audio_chunk])

        if len(self._audio_buffer) >= self._chunk_size:
            audio_to_process = self._audio_buffer[: self._chunk_size]
            self._audio_buffer = self._audio_buffer[self._chunk_size :]

            if self._callback:
                self._callback(audio_to_process)

        return (in_data, pyaudio.paContinue)

    def start(self) -> None:
        if self.is_running:
            return
        try:
            self._stream = self._p.open(
                format=pyaudio.paFloat32,
                channels=1,
                rate=self._rate,
                input=True,
                frames_per_buffer=1024,
                stream_callback=self._stream_callback,
            )
            self._stream.start_stream()
            self.is_running = True
            print("🎤 Monitoreo de audio iniciado...")
        except Exception as e:
            print(f"❌ Error al iniciar el stream de PyAudio: {e}")

    def stop(self) -> None:
        if not self.is_running or self._stream is None:
            return
        try:
            self.is_running = False
            self._stream.stop_stream()
            self._stream.close()
            self._p.terminate()
            print("🛑 Monitoreo de audio detenido.")
        except Exception as e:
            print(f"⚠️ Error al detener el stream: {e}")

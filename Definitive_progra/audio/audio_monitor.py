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

        # NO inicializamos PyAudio aquí. Lo haremos en start()
        # para asegurar una conexión fresca cada vez.
        self._p: pyaudio.PyAudio | None = None
        self._stream: pyaudio.Stream | None = None
        self.is_running: bool = False
        
        self._audio_buffer = np.array([], dtype=np.float32)

    def _stream_callback(self, in_data, frame_count, time_info, status):
        """Callback interno que PyAudio llama cuando tiene datos."""
        if not self.is_running:
            return (None, pyaudio.paComplete)

        # Convertir bytes a float32
        audio_chunk = np.frombuffer(in_data, dtype=np.float32).astype(np.float32)
        self._audio_buffer = np.concatenate([self._audio_buffer, audio_chunk])

        # Si llenamos el buffer del tamaño requerido por la IA, enviamos
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
            print("🎤 Iniciando motor de audio...")
            # 1. Creamos la instancia de PyAudio AQUÍ (nueva cada vez)
            self._p = pyaudio.PyAudio()
            
            # 2. Abrimos el stream
            self._stream = self._p.open(
                format=pyaudio.paFloat32,
                channels=1,
                rate=self._rate,
                input=True,
                frames_per_buffer=1024,
                stream_callback=self._stream_callback,
            )
            
            # 3. Iniciamos el flujo
            self._stream.start_stream()
            self.is_running = True
            print("✅ Monitoreo de audio activo.")
            
        except Exception as e:
            print(f"❌ Error crítico al iniciar micrófono: {e}")
            # Limpieza de emergencia si falla el inicio
            self.stop()

    def stop(self) -> None:
        """Detiene el stream y libera los recursos completamente."""
        self.is_running = False
        
        # Limpieza segura del Stream
        if self._stream is not None:
            try:
                if self._stream.is_active():
                    self._stream.stop_stream()
                self._stream.close()
            except Exception as e:
                print(f"⚠️ Error cerrando stream: {e}")
            finally:
                self._stream = None

        # Limpieza segura de PyAudio
        if self._p is not None:
            try:
                self._p.terminate()
            except Exception as e:
                print(f"⚠️ Error terminando PyAudio: {e}")
            finally:
                self._p = None # Importante: lo volvemos None para el próximo start
                
        # Limpiar buffer residual
        self._audio_buffer = np.array([], dtype=np.float32)
        print("🛑 Monitoreo detenido y recursos liberados.")
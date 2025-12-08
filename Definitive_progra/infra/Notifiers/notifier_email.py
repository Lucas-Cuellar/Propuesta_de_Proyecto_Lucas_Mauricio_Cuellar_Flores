# infra/notifier_email.py
import smtplib
from email.message import EmailMessage
from core.BaseNotifier import BaseNotifier
from config.monitor_config import EmailConfig

class GmailNotifier(BaseNotifier):
    def __init__(self, config: EmailConfig = None) -> None:
        self._config = config or EmailConfig()

    def notify(self, status: str, confidence: float) -> None:
        cfg = self._config
        if not cfg.sender or not cfg.password or not cfg.recipient:
            print("⚠️ [Email] Faltan credenciales. Revisa monitor_settings.yaml")
            return

        msg = EmailMessage()
        msg["Subject"] = f"🚨 ALERTA: Falla detectada - {status}"
        # Truco: "Nombre <correo>"
        msg["From"] = f"🤖 Monitor IA <{cfg.sender}>"
        msg["To"] = cfg.recipient

        body = (
            f"⚠️ ALERTA DE SISTEMA ⚠️\n\n"
            f"Se ha detectado un comportamiento anómalo.\n"
            f"🔹 Estado: {status}\n"
            f"🔹 Confianza: {confidence * 100:.2f}%\n\n"
            "Por favor, verifique el equipo inmediatamente."
        )
        msg.set_content(body)

        print(f"📧 Enviando correo a {cfg.recipient}...")
        try:
            # Gmail usa puerto 587 con TLS
            with smtplib.SMTP("smtp.gmail.com", 587, cfg.timeout) as server:
                server.starttls()
                server.login(cfg.sender, cfg.password)
                server.send_message(msg)
            print("✅ Correo enviado correctamente.")
        except TimeoutError:
            print("❌ Error: El servidor de Gmail tardó demasiado en responder.")
        except Exception as e:
            print(f"❌ Error enviando correo: {e}")
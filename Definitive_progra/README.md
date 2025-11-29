# 📘 Sistema Inteligente de Monitoreo Acústico
### Monitoreo en tiempo real con IA, Telegram y registro automático de fallas

Este proyecto implementa un sistema capaz de **escuchar**, **analizar** y **detectar anomalías acústicas** en un equipo o mecanismo, utilizando redes neuronales (Keras), audio en tiempo real, notificaciones automáticas y registro estructurado de fallas en CSV.

---

# 📂 Arquitectura General del Proyecto

```
Definitive_progra/
│
├── main.py
│
├── config/
│   ├── monitor_config.py
│   └── monitor_settings.yaml
│
├── audio/
│   └── audio_monitor.py
│
├── core/
│   ├── interfaces.py
│   ├─── monitor_controller.py
│   └── logger_interface.py
│
├── infra/
│   ├── classifier_keras.py
│   ├── audio_features.py
│   ├── logging_utils.py
│   └── notifier_telegram.py
│
├── ui/
│   ├── model_selector.py
│   ├── ui_monitoring.py
│   ├── status_panel.py
│   ├─── controls_panel.py
│   └── theme.py
├──Logs/
└──Muestras/
```

---

# 🔄 Flujo del Sistema

```
Micrófono
   ↓
AudioMonitor  (captura chunk)
   ↓
MonitoringController  (lógica central)
   ↓
KerasSoundClassifier  (predicción)
   ↓
Reglas / cooldown
   ↓
┌─────────────┬──────────────┐
│ TelegramNotifier            │
│ CsvLogger (CSV)             │
└─────────────┴──────────────┘
   ↓
UI (semaforo + confianza)
```

---

# ⚙️ Configuración (YAML)

Archivo: `config/monitor_settings.yaml`

```yaml
audio:
  rate: 44100
  chunk_duration_sec: 2

monitoring:
  alert_cooldown_sec: 10

telegram:
  token: "TU_TOKEN_REAL"
  chat_id: "TU_CHAT_ID"
  timeout: 10

paths:
  models_dir: null
  logs_dir: null
```

---

# 🧩 Componentes Principales

## 🎤 AudioMonitor (`audio/audio_monitor.py`)
- Captura audio en tiempo real con PyAudio.
- Entrega bloques (chunks) al controlador.

## 🧠 KerasSoundClassifier (`infra/classifier_keras.py`)
- Cargar modelo `.h5`
- Leer parámetros `preproc.npz`
- Extraer MFCC
- Normalizar
- Predecir clase + confianza

## 🧾 CsvLogger (`infra/logging_utils.py`)
- Crear archivo CSV si no existe
- Registrar fallas con fecha/hora/confianza

## 📲 TelegramNotifier (`infra/notifier_telegram.py`)
- Construcción de mensaje de alerta
- Envío mediante Telegram Bot API

## 🧭 MonitoringController (`core/monitor_controller.py`)
- Control del monitoreo
- Ejecución del clasificador
- Aplicación de reglas + cooldown
- Disparo de alertas/logs
- Comunicación con la UI

## 🖥️ UI Monitoring (`ui/ui_monitoring.py`)
- Ventana principal
- Semáforo visual
- Controles de inicio/detención
- Acceso al CSV

---

# 🧱 Arquitectura (UML Simplificado)

```
                UI (Tkinter)
                     │
                     ▼
          MonitoringController
     ┌──────────────┼─────────────────┐
     ▼              ▼                 ▼
Classifier     Notifier           Logger
(Keras)       (Telegram)          (CSV)

AudioMonitor → MonitoringController
```

---

# 🧪 Aplicación de SOLID

## S — Single Responsibility  
- `AudioMonitor`: solo captura audio  
- `CsvLogger`: solo registra fallas  

## O — Open/Closed  
- Puedes agregar `WhatsAppNotifier`, `EmailNotifier`, `DummyClassifier` sin alterar el controller.

## L — Liskov Substitution  
- `KerasSoundClassifier` funciona donde se espera un `BaseClassifier`.

## I — Interface Segregation  
- Interfaces pequeñas y claras: `BaseClassifier`, `BaseNotifier`, `BaseLogger`.

## D — Dependency Inversion  
- El controller depende de interfaces, no implementaciones.

---

# 🔁 Buenas Prácticas Aplicadas

## 1. SRP  
Cada módulo tiene una responsabilidad clara.

## 2. Encapsulamiento  
Atributos internos protegidos (`_model`, `_params`, `_config`).

## 3. Loose Coupling  
UI → Controller → Interfaces → Implementaciones.

## 4. Extensibilidad / Reutilización  
Fácil cambiar o agregar clasificadores/notificadores.

## 5. Portabilidad  
YAML asegura que las rutas y parámetros no estén quemados en el código.

## 6. Defensibilidad  
- Manejo de errores al cargar modelo  
- Verificación de credenciales Telegram

## 7. Testabilidad  
- Se pueden usar mocks (`FakeNotifier`, `DummyClassifier`)  
- `AudioMonitor` usa callback inyectable  

## 8. KISS / DRY / YAGNI  
- Código simple  
- Sin duplicación  
- Sin funciones que no se usen

---

# ✔ Checklist Final

- [x] Captura de audio en tiempo real  
- [x] Clasificación por IA  
- [x] Extracción MFCC  
- [x] Notificaciones por Telegram  
- [x] Registro CSV automatizado  
- [x] UI con semáforo  
- [x] YAML configurable  
- [x] Arquitectura modular  
- [x] Principios SOLID  
- [x] Polimorfismo funcional  

---

# 📎 Recomendaciones Futuras

- Agregar `WhatsAppNotifier`  
- Incluir `DummySoundClassifier` para pruebas  
- Crear pruebas unitarias con `pytest`  
- Documentación extendida con docstrings  

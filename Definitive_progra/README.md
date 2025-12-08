📘 Sistema Inteligente de Monitoreo Acústico (v2.0)
Monitoreo en tiempo real con IA, Alertas Multicanal y Registro Híbrido
Este proyecto implementa una solución de Mantenimiento Predictivo capaz de escuchar, analizar y detectar anomalías en maquinaria industrial. Utiliza Deep Learning (Keras/CNN), procesamiento de audio asíncrono, y un robusto sistema de notificaciones y persistencia.

📂 Arquitectura General del Proyecto (Refactorizada)
La estructura ha evolucionado para separar mejor las responsabilidades (infra dividida en módulos y core con interfaces segregadas).

Plaintext

Definitive_progra/
│
├── main.py                     # Launcher
│
├── config/                     # Configuración Segura
│   ├── monitor_config.py       # Lector de Variables de Entorno
│   └── monitor_settings.yaml   # Parámetros de usuario
│
├── audio/                      # Hardware
│   └── audio_monitor.py        # Captura asíncrona con reinicio seguro
│
├── core/                       # Lógica de Negocio (Abstracciones)
│   ├── monitor_controller.py   # Cerebro: Orquesta lógica y tiempos
│   ├── BaseClassifier.py      # Contrato IA
│   ├── BaseNotifier.py        # Contrato Notificaciones
│   └── BaseLogger.py          # Contrato Logs
│
├── infra/                      # Implementaciones (Obreros)
│   ├── classifier_keras.py     # Implementación IA
│   ├── audio_features.py       # Matemáticas (MFCC)
│   │
│   ├── Loggers/                # Persistencia
│   │   ├── logger_sqlite.py    # SQL Estructurado
│   │   ├── logger_csv.py       # Texto plano
│   │   └── logger_composite.py # Patrón Composite
│   │
│   └── Notifiers/              # Comunicación
│       ├── notifier_telegram.py
│       ├── notifier_email.py   # Gmail SMTP Seguro
│       └── notifier_composite.py # Patrón Composite
│
├── ui/                         # Interfaz Gráfica
│   ├── model_selector.py       # Inyección de Dependencias (Fábrica)
│   ├── ui_monitoring.py        # Panel de Control
│   ├── controls_panel.py       # Botones y accesos a reportes
│   └── ...
│
└── logs/                       # Almacenamiento de Datos (.db, .csv)
🔄 Flujo del Sistema (Patrón Composite)
El sistema ahora utiliza el Patrón Composite para manejar múltiples salidas simultáneas sin complicar el controlador.

Plaintext

Micrófono
   ↓
AudioMonitor (Chunk)
   ↓
MonitoringController (Cerebro)
   ↓
KerasSoundClassifier (Predicción)
   ↓
[Filtro 1] Umbral de Confianza (>85%)
   ↓
[Filtro 2] Lógica de Tiempos (Cooldown vs Continuo)
   ↓
┌───────────────────────────────┐
│     CompositeNotifier         │──► Telegram
│ (Alertas Continuas/Inmediatas)│──► Gmail (con Timeout)
└───────────────────────────────┘
   ↓
┌───────────────────────────────┐
│      CompositeLogger          │──► SQLite (.db)
│ (Registro Periódico/Cooldown) │──► CSV (.csv)
└───────────────────────────────┘
   ↓
UI (Semáforo + Gráficos)
⚙️ Configuración (YAML + Env Vars)
Archivo: config/monitor_settings.yaml (Limpio de credenciales)

YAML

audio:
  rate: 44100
  chunk_duration_sec: 2

monitoring:
  alert_cooldown_sec: 60          # Tiempo entre registros en BD
  min_confidence_threshold: 0.85  # Sensibilidad mínima de la IA

telegram:
  timeout: 10  # Seguridad ante fallos de red

email:
  timeout: 10  # Seguridad ante fallos de SMTP
Nota de Seguridad: Las credenciales (TOKEN, PASSWORD, CHAT_ID) se inyectan mediante Variables de Entorno del sistema operativo, no en el archivo de texto.

🧩 Componentes y Mejoras
🧠 Core & Lógica (core/monitor_controller.py)
Filtro de Confianza: Ignora predicciones débiles (<85%).

Doble Temporizador:

Alertas: Se envían continuamente mientras persista la falla.

Logs: Se guardan respetando el cooldown para no saturar el disco.

📡 Notifiers (infra/notifiers/)
GmailNotifier: Nuevo. Envía correos formales usando "Display Name" enmascarado y protección timeout.

CompositeNotifier: Agrupa Telegram y Email. Si uno falla (ej. sin internet), el error se captura para no detener el sistema.

💾 Loggers (infra/loggers/)
SqliteLogger: Nuevo. Crea bases de datos .db optimizadas con columnas separadas (Fecha, Hora, Estado, Confianza %).

CompositeLogger: Escribe en SQL y CSV al mismo tiempo.

🖥️ UI (ui/)
ModelSelector: Actúa como fábrica de objetos, inyectando las dependencias compuestas.

Nuevos Controles: Botones directos para abrir el historial en Excel o DB Browser.

🧪 Aplicación de SOLID y Patrones
S — Single Responsibility
Se separaron los Notifiers y Loggers en carpetas propias.

monitor_config.py solo se encarga de leer variables.

O — Open/Closed
Se agregó GmailNotifier y SqliteLogger sin tocar ni una línea de monitor_controller.py.

L — Liskov Substitution
CompositeNotifier se comporta exactamente igual que un BaseNotifier. El controlador no sabe la diferencia.

I — Interface Segregation
Interfaces divididas en archivos propios: base_classifier.py, base_notifier.py, abstract_logger.py.

D — Dependency Inversion
La UI inyecta las dependencias. El Core depende puramente de abstracciones.

🏗️ Patrón Composite
Permite tratar a un grupo de objetos (Telegram + Email) como si fuera uno solo. Simplifica enormemente la lógica del controlador.

✔ Checklist de Funcionalidades (v2.0)
[x] Captura de audio asíncrona robusta (PyAudio)

[x] Clasificación IA con umbral de confianza configurable

[x] Persistencia Híbrida: SQL (Estructurado) + CSV (Rápido)

[x] Alertas Multicanal: Telegram + Gmail (SMTP Seguro)

[x] Seguridad: Manejo de credenciales por Variables de Entorno

[x] UX: Apertura de reportes desde la interfaz

[x] Resiliencia: Manejo de Timeouts y reconexión de micrófono

📎 Guía Rápida de Uso
Configurar Variables de Entorno:

TELEGRAM_BOT_TOKEN, EMAIL_PASSWORD, etc.

Entrenar Modelo (Opcional):

Usar audio_trainer con HOP_DURATION=2.0 para audios largos.

Ejecutar:

python main.py

Visualizar Datos:

Usar DB Browser for SQLite para abrir los archivos .db generados en logs/.
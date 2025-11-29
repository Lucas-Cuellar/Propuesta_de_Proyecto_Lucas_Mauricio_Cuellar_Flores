# Propuesta Inicial de Proyecto 

**Carrera:** Ing. Mecatronica  
**Materia:** Programacion Superior  
**Periodo:** Segundo Parcial / Proyecto Final  
**Estudiante(s):** Lucas Mauricio Cuellar Flores  
**Fecha de entrega:** 2025-10-20 

---

## 1. Datos Generales del Proyecto

| Campo | Descripción |
|--------|-------------|
| **Nombre del proyecto:** | HEARING GUARDIAN: Sistema de deteccion de fallas mediante sonido|
| **Tipo de aplicación:** | ✅ Escritorio ☐ Web ☐ Móvil ☐ Otro: __________ |
| **Lenguaje / entorno de desarrollo:** | Python 3.11, SoundDevice, Tkinter|
| **Repositorio Git (opcional):** | https://github.com/Lucas-Cuellar/Propuesta_de_Proyecto_Lucas_Mauricio_Cuellar_Flores.git |
| **Uso de Inteligencia Artificial:** | ☐ No ✅ Sí |

**Si usas IA, explica brevemente cómo y en qué etapa contribuye:**  
> Se utiliza IA (TensorFlow/Keras) para entrenar una red neuronal capaz de reconocer patrones acusticos de fallas. El modelo se entrena con un ruido ambiente, sonido de el mecanismo funcionando correctamente y el sonido de cuando el mecanismo presenta alguna falla.

## 2. Descripción del Proyecto

### Resumen breve
HEARING GUARDIAN es una aplicación de escritorio desarrollada en Python con Tkinter que permite detectar fallas mecánicas a partir del sonido que emiten los equipos o mecanismos.
Utiliza una red neuronal convolucional (CNN) entrenada para distinguir entre sonidos funcionales y disfuncionales, analizando tanto grabaciones como audio en tiempo real desde un micrófono.
Está dirigida a estudiantes e ingenieros en el área de mecatrónica e industrial, que buscan una herramienta de diagnóstico preventivo accesible y adaptable.
El proyecto resuelve el problema del diagnóstico tardío de fallas, proporcionando una alerta temprana que reduce tiempos de parada y costos de mantenimiento.
Su arquitectura orientada a objetos permite extender fácilmente nuevas clases de detectores, fuentes de sonido o modelos de IA sin reescribir el sistema.

### Objetivos principales
1. Lograr el correcto monitoreo y comparacion con un microfono en vivo
2. Lograr el correcto envio de alerta cuando se obtenga un sonido defectuoso.
3. Lograr el correcto guardado y ordenamiento de los errores en un csv

---

## 3. Diseño Técnico y Aplicación de POO

### Principios de POO aplicados
Marca los que planeas usar:
- ✅ Encapsulamiento (atributos privados y métodos públicos)
- ✅ Uso de constructores
- ✅ Herencia
- ✅ Polimorfismo
- ✅ Interfaces o clases abstractas

### Clases estimadas
- **Cantidad inicial de clases:** __11___  
- **Ejemplo de posibles clases:** *(Usuario, Producto, Pedido, etc.)*
1. AudioMonitor

Se encarga de capturar audio en tiempo real desde el micrófono usando PyAudio.

Entrega bloques de audio (ndarray) al resto del sistema mediante un callback.

2. AudioConfig

Define los parámetros de captura de audio (frecuencia de muestreo, tamaño de chunk).

Centraliza esta configuración para que toda la app use valores coherentes.

3. BaseClassifier 

BaseClassifier: interfaz abstracta que define cómo debe comportarse cualquier clasificador de audio.

4. KerasSoundClassifier: implementación concreta que usa un modelo Keras (.h5 + .npz) para predecir el estado del equipo. (Ejemplo directo de herencia + polimorfismo.)

5. BaseNotifier 

BaseNotifier: interfaz para canales de notificación (Telegram, WhatsApp, etc.).

6. TelegramNotifier: implementación que envía alertas al técnico mediante Telegram Bot API.

BaseLogger 

7. BaseLogger: interfaz para el sistema de registro de fallas.

CsvLogger: implementación que guarda cada falla en un archivo .csv con fecha, hora, estado y confianza.

8. MonitoringController

Es el “cerebro” del monitoreo: recibe audio ya capturado, llama al clasificador, aplica el cooldown de alertas y decide cuándo notificar y cuándo registrar en el log.

No sabe nada de UI ni de detalles de Telegram o CSV; solo trabaja con interfaces.

9. MonitoringApp

Ventana principal de monitoreo.

Coordina MonitoringController, AudioMonitor, StatusPanel y ControlsPanel; actualiza la interfaz según los resultados del clasificador.

10. StatusPanel

Panel gráfico que muestra el estado actual del equipo (AMBIENTE, FUNCIONAL, DISFUNCIONAL) y la confianza, usando un “semáforo” de colores y etiquetas.

11. ModelSelector

Pantalla inicial de la aplicación.

Escanea la carpeta de modelos, permite elegir el modelo de IA a usar y, tras la selección, construye todos los componentes necesarios y abre la MonitoringApp.
### Persistencia de datos
- ✅ Archivos locales  
- [ ] Base de datos  
- ✅ En memoria (temporal)  
- [ ] Otro: __________

## 4. Funcionalidades Principales

| Nº | Nombre de la funcionalidad | Descripción breve | Estado actual |
|----|-----------------------------|-------------------|----------------|
| 1 | Detección en tiempo real (micrófono) |Captura audio del micrófono en ventanas de 1 s, extrae log-mel y muestra la predicción continua | ☐ Planeada ✅ En desarrollo |
| 2 | Envio de alertas | Si detecta un sonido disfuncional manda una alerta a telegram | ☐ Planeada ✅ | En desarrollo |
| 3 | Guardado | Guarda los reportes de error en una csv| ☐ Planeada ✅ En desarrollo |

## 5. Compromiso del Estudiante

Declaro que:
- Entiendo los criterios de evaluación establecidos en las rúbricas.
- Presentaré una demostración funcional del proyecto.
- Defenderé el código que yo mismo implementé y explicaré las clases y métodos principales.
- Si usé herramientas de IA, comprendo su funcionamiento y las adapté al contexto del proyecto.

**Firma (nombre completo):** ____Lucas_Mauricio_Cuellar_Flores____  

---

## 6. Validación del Docente *(completa el profesor)*

| Campo | Detalle |
|--------|---------|
| **Visto bueno del docente:** | ☐ Aprobado para desarrollar ☐ Requiere ajustes ☐ Rechazado |
| **Comentarios / Observaciones:** |  |
| **Firma docente:** |  |
| **Fecha de revisión:** |  |

---

> **Instrucciones para entrega:**

> - Completa todas las secciones antes de tu presentación inicial.  
> - No borres las casillas ni el formato para garantizar uniformidad del curso.  
> - El docente revisará y aprobará esta propuesta antes del desarrollo completo.

---

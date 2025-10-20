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
1. Desarrollar una aplicación de escritorio modular basada en principios de Programación Orientada a Objetos (POO), que integre herencia, encapsulamiento, abstracción y polimorfismo de forma clara y eficiente. 
2.  Entrenar e implementar una red neuronal CNN 2D que clasifique sonidos funcionales y disfuncionales de mecanismos mediante análisis espectral (log-mel o MFCC).
3.  Integrar la red neuronal con una interfaz grafica entendible y optima

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
- **Cantidad inicial de clases:** __9___  
- **Ejemplo de posibles clases:** *(Usuario, Producto, Pedido, etc.)*

1. AudioSource 

2. FileAudioSource

3. MicrophoneAudioSource

4. FeatureExtractor 

5. LogMelExtractor

6. MFCCExtractor

7. AudioClassifier 

8. KerasModel

9. DetectionPipeline 

### Persistencia de datos
- ✅ Archivos locales  
- [ ] Base de datos  
- ✅ En memoria (temporal)  
- [ ] Otro: __________

## 4. Funcionalidades Principales

| Nº | Nombre de la funcionalidad | Descripción breve | Estado actual |
|----|-----------------------------|-------------------|----------------|
| 1 | Clasificación de archivos de audio | Carga un modelo .keras, permite seleccionar uno o varios audios (.wav) y devuelve la clase (funcional/disfuncional) con su confianza. | ☐ Planeada ✅ En desarrollo |
| 2 | Detección en tiempo real (micrófono) | Captura audio del micrófono en ventanas de 1 s, extrae log-mel y muestra la predicción continua; emite alerta si supera el umbral. | ☐ Planeada ✅ En desarrollo |
| 3 | Entrenamiento y evaluación del modelo | Script train_audio.py que genera el modelo CNN a partir de un dataset por carpetas, e imprime métricas (reporte y matriz de confusión). | ☐ Planeada ✅ En desarrollo |

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
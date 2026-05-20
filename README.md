# ⏰ Premium Time Dashboard

Un panel de control de tiempo interactivo, avanzado y de alto rendimiento desarrollado en **Python** utilizando **CustomTkinter**. Este proyecto combina la ingeniería de software con un diseño de interfaz de usuario (UI/UX) moderno y minimalista, ofreciendo una experiencia fluida y multifuncional.

---

## ✨ Características Principales

*   **Reloj Análogo de Alta Relojería:** Movimiento continuo del segundero (*Smooth Sweep*) calculado mediante física matemática a tiempo real (100Hz), eliminando los saltos toscos de segundo a segundo.
*   **Indicador Smart Día/Noche:** El cuadrante del reloj detecta automáticamente si la zona horaria seleccionada se encuentra en horario AM o PM y adapta su iluminación de fondo.
*   **Reloj Digital Conmutable:** Alterna instantáneamente entre formato de 12 horas (con indicador AM/PM) y formato militar de 24 horas.
*   **Selector de Zona Horaria Mundial:** Consulta el tiempo exacto en ciudades estratégicas globales (`Londres`, `Nueva York`, `Tokio`, etc.) de forma sincronizada.
*   **Suite de Productividad Integrada (Pestañas):**
    *   **Cronómetro Pro:** Medidor de alta precisión para capturar tiempos con centésimas de segundo.
    *   **Enfoque Pomodoro:** Temporizador de productividad preconfigurado para bloques de trabajo y descansos (*Short/Long Breaks*).
*   **Diseño Adaptativo Premium:** Soporte nativo para cambio de tema (Modo Oscuro Profundo / Modo Claro) con esquinas redondeadas y estética neumórfica.

---

## 🛠️ Tecnologías y Librerías Utilizadas

El núcleo del proyecto está construido sobre el ecosistema nativo de Python, potenciado por las siguientes dependencias de terceros:

| Librería | Propósito | Vínculo oficial |
| :--- | :--- | :--- |
| **CustomTkinter** | Framework de UI moderno con soporte nativo de widgets premium y manejo de temas (*Dark/Light*). | [GitHub](https://github.com/TomSchimansky/CustomTkinter) |
| **Pillow (PIL)** | Procesamiento y renderizado optimizado de interfaces gráficas. | [PyPI](https://pypi.org/project/pillow/) |
| **Pytz** | Motor de base de datos de zonas horarias mundiales Olson para cálculos cronológicos precisos. | [PyPI](https://pypi.org/project/pytz/) |
| **Math & Datetime** | Módulos nativos de Python para el cálculo vectorial (senos/cosenos) de las manecillas y manejo del tiempo. | *(Nativo)* |

---

## 🚀 Instalación y Despliegue

Sigue estos sencillos pasos para clonar y ejecutar el panel en tu entorno local:

### 1. Clonar el repositorio (u obtener los archivos)
Si utilizas Git, clona el proyecto en tu máquina de la siguiente manera:
```bash
git clone [https://github.com/TU_USUARIO/premium-time-dashboard.git](https://github.com/TU_USUARIO/premium-time-dashboard.git)
cd premium-time-dashboard

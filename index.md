---
layout: post
title: "Reloj Inteligente ESP32-S3: Sincronización NTP y Control BLE"
description: "Sistema de tiempo real con MicroPython, gestión de RAM y coexistencia WiFi/Bluetooth."
---
🕒 ESP32-S3: Reloj Inteligente Dual (WiFi + BLE)
Proyecto de reloj sincronizado por WiFi (NTP) con control remoto Bluetooth LE y visualización en LCD I2C.

Este proyecto demuestra la implementación de un sistema embebido robusto capaz de gestionar conectividad inalámbrica dual, sincronización de tiempo real y una interfaz de usuario física mediante MicroPython.
¿Qué hemos mejorado en esta versión?

Para tu sitio web, puedes añadir este pequeño párrafo de "Estado del Proyecto":

    Estado actual: El proyecto ha alcanzado la v1.1, resolviendo los desafíos críticos de coexistencia de radio. Gracias a una gestión optimizada de la memoria RAM y pausas de CPU fragmentadas, el dispositivo mantiene una conexión Bluetooth estable mientras el WiFi opera en segundo plano.

## 🚀 Características (v1.1)

* **Sincronización NTP de Alta Precisión:** Obtiene la hora exacta vía WiFi al arrancar, garantizando que el reloj nunca se desvíe.
* **Control Remoto BLE (Bluetooth Low Energy):** Interfaz inalámbrica que permite controlar el LCD (encender/apagar luz) y consultar el estado del sistema desde el móvil.
* **Coexistencia Radio Optimizada:** Configuración avanzada (`PM_NONE`) que permite al WiFi y al Bluetooth trabajar simultáneamente sin interferencias.
* **Gestión de Memoria Proactiva:** Implementación de `Garbage Collection` en tiempo real para asegurar estabilidad operativa 24/7.
* **Respuesta Instantánea:** Bucle principal fragmentado para atender comandos Bluetooth sin interrumpir la fluidez del reloj.
* **Arquitectura Segura:** Separación de credenciales (WiFi/TZ) en archivos independientes para mayor privacidad.

## 🛠️ Requisitos de Hardware
* Placa **ESP32-S3**.
* Pantalla **LCD 16x2** con adaptador **I2C PCF8574**.
* Cables de conexión.

## 🔌 Esquema de Conexiones

| LCD (I2C) | ESP32-S3 |
| :--- | :--- |
| **GND** | GND |
| **VCC** | 3V |
| **SDA** | GPIO 4 |
| **SCL** | GPIO 5 |

## 💻 Instalación y Configuración

1.  **Preparar el entorno:** Asegúrate de tener MicroPython instalado en tu ESP32-S3.
2.  **Configurar WiFi:** * Renombra el archivo `config.example.py` a `config.py`.
    * Introduce el nombre de tu red y contraseña.
3.  **Subir los archivos:** Utiliza una herramienta como `ampy` o `Thonny` para subir estos archivos a la raíz de la placa:
    * `LcdApi.py`
    * `i2c_lcd.py`
    * `config.py`
    * `main.py`
4.  **Reiniciar:** Pulsa el botón RESET de la placa y el reloj comenzará a funcionar.
   
🕒 Actualización: Estabilizando el Reloj Bluetooth (v1.1)

En esta etapa del proyecto, me enfrenté a un reto clásico del ESP32-S3: la inestabilidad de la conexión Bluetooth cuando el WiFi está activo. Aquí explico cómo lo solucioné.
🛠 El Problema

Al conectar el móvil mediante Serial Bluetooth Terminal, la conexión se caía a los pocos segundos. Esto ocurría por dos razones:

    Conflicto de Antena: El WiFi y el Bluetooth comparten la radiofrecuencia y se "pisaban" entre sí.

    Bloqueo del Procesador: El uso de time.sleep(1) dejaba al ESP32 "sordo" ante las peticiones del Bluetooth.

💡 Las 4 Claves de la Solución

    Prioridad de Radio: Desactivé el modo de ahorro de energía del WiFi para que la antena estuviera siempre disponible para el Bluetooth.
    Python

    wlan.config(pm=network.WLAN.PM_NONE)

    Flags de Comunicación: Actualicé los permisos del servicio BLE a FLAG_WRITE_NO_RESPONSE. Esto permite que el móvil envíe comandos sin esperar confirmación, eliminando latencias y desconexiones.

    Pausas Inteligentes: Sustituí el sleep(1) por un bucle fragmentado de 10 ciclos de 100ms. Esto permite que el ESP32 revise el canal Bluetooth 10 veces por segundo sin afectar la precisión del reloj.

    Higiene de RAM: Introduje gc.collect() para limpiar la memoria dinámica en cada ciclo, evitando que el stack de Bluetooth se quede sin espacio tras un uso prolongado.

📺 Resultado Final

Ahora el reloj sincroniza la hora por internet al arrancar y mantiene una conexión Bluetooth sólida como una roca. Esto permite encender/apagar la luz del LCD y consultar el estado desde el móvil de forma instantánea y sin desconexiones accidentales.

---
*Proyecto desarrollado por [Sartaza](https://github.com/sartaza).*

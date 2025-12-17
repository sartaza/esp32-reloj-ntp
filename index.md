---
layout: default
title: Inicio
---
# 🕰️ Reloj NTP con ESP32-S3 y LCD I2C

Este proyecto convierte un **ESP32-S3** en un reloj digital de alta precisión que se sincroniza automáticamente por Internet mediante el protocolo **NTP**. Utiliza **MicroPython** para una ejecución eficiente y una pantalla LCD 16x2 para la visualización.

## 🚀 Características
* **Sincronización Automática:** Obtiene la hora exacta vía WiFi.
* **Ajuste de Zona Horaria:** Configurable fácilmente para cualquier país.
* **Librería Optimizada:** Incluye un controlador I2C corregido para evitar caracteres corruptos.
* **Seguridad:** Separación de credenciales WiFi mediante un archivo de configuración.

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

    Prioridad de Radio: Desactivé el modo de ahorro de energía del WiFi para que la antena estuviera siempre lista.
    Python

    wlan.config(pm=network.WLAN.PM_NONE)

    Flags de Comunicación: Cambié los permisos del servicio BLE para aceptar escrituras sin respuesta, lo que aligera la carga de datos.

    Pausas Inteligentes: Dividí el segundo de espera en 10 partes de 100ms. Así, el reloj sigue funcionando pero el Bluetooth se revisa 10 veces más rápido.

    Higiene de RAM: Introduje gc.collect() para limpiar la basura de la memoria en cada vuelta del reloj, evitando cuelgues por saturación.

📺 Resultado Final

Ahora el reloj sincroniza la hora por internet al arrancar y mantiene una conexión Bluetooth sólida como una roca, permitiendo encender/apagar la luz del LCD y consultar el estado desde el móvil sin desconexiones.

---
*Proyecto desarrollado por [Sartaza](https://github.com/sartaza).*

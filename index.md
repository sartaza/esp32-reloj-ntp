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

---
*Proyecto desarrollado por [Sartaza](https://github.com/sartaza).*

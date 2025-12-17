ESP32-S3 Reloj NTP con LCD I2C

Reloj sincronizado por internet (NTP) usando MicroPython y una pantalla LCD 16x2.
Requisitos

    ESP32-S3

    LCD 16x2 con adaptador I2C PCF8574

    MicroPython v1.20+
# esp32-reloj-ntp

## 🛠️ Esquema de Conexión

Para que el reloj funcione, conecta los pines del LCD al ESP32-S3 de la siguiente forma:

| LCD (I2C) | ESP32-S3 |
| :--- | :--- |
| **GND** | GND |
| **VCC** | 5V |
| **SDA** | GPIO 4 |
| **SCL** | GPIO 5 |

> **Nota:** Si la pantalla brilla pero no se ven las letras, recuerda ajustar el potenciómetro (el tornillo azul) que está detrás del módulo I2C del LCD.

from machine import Pin, I2C
import time
import network
import ntptime 
import bluetooth
from i2c_lcd import I2cLcd
from config import WIFI_SSID, WIFI_PASSWORD, TZ_OFFSET

# --- CONFIGURACIÓN LCD E I2C ---
I2C_SCL_PIN = 5
I2C_SDA_PIN = 4
LCD_ADDR = 0x27 
lcd = None

# --- CONFIGURACIÓN BLUETOOTH BLE ---
ble = bluetooth.BLE()
ble.active(True)

# UUIDs para servicio UART
UART_UUID = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
RX_UUID = bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E")
UART_SERV = (UART_UUID, ((RX_UUID, bluetooth.FLAG_WRITE | bluetooth.FLAG_WRITE_NO_RESPONSE),),)
((rx_handle,),) = ble.gatts_register_services((UART_SERV,))

# --- FUNCIONES BLUETOOTH ---

def advertise():
    """Inicia la publicidad del Bluetooth"""
    name = b'Reloj-Salva'
    # Estructura del paquete de publicidad (GAP)
    adv_data = bytearray([0x02, 0x01, 0x06, len(name) + 1, 0x09]) + name
    ble.gap_advertise(200000, adv_data, connectable=True) # 200ms en microsegundos
    print("BLE: Publicitando como Reloj-Salva...")

def ble_irq(event, data):
    """Manejador de eventos Bluetooth"""
    if event == 1: # _IRQ_CENTRAL_CONNECT
        print("\n[BLE] ¡Móvil conectado!")
    
    elif event == 2: # _IRQ_CENTRAL_DISCONNECT
        print("\n[BLE] Móvil desconectado.")
        advertise() # Volver a publicitar al desconectar
    
    elif event == 3: # _IRQ_CENTRAL_WRITE
        conn_handle, value_handle = data
        if value_handle == rx_handle:
            msg = ble.gatts_read(rx_handle).decode('utf-8').strip().lower()
            print(f"[BLE] Comando recibido: {msg}")
            
            if msg == "on":
                lcd.backlight_on()
                ble.gatts_write(rx_handle, b"Luz ENCENDIDA\n")
            elif msg == "off":
                lcd.backlight_off()
                ble.gatts_write(rx_handle, b"Luz APAGADA\n")
            elif msg == "status":
                t = time.time() + (TZ_OFFSET * 3600)
                tm = time.localtime(t)
                res = "Hora: {:02d}:{:02d}:{:02d}\n".format(tm[3], tm[4], tm[5])
                ble.gatts_write(rx_handle, res.encode())

# Registrar la función de eventos
ble.irq(ble_irq)

# --- FUNCIONES DEL RELOJ ---

def init_lcd():
    global lcd
    i2c = I2C(0, scl=Pin(I2C_SCL_PIN), sda=Pin(I2C_SDA_PIN), freq=100000)
    try:
        lcd = I2cLcd(i2c, LCD_ADDR, 2, 16)
        return True
    except:
        return False

def main():
    if not init_lcd(): 
        print("Error: No se encontró el LCD")
        return
    
    lcd.clear()
    lcd.putstr("Conectando WiFi")
    
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)
    
    # Desactivar ahorro de energía para evitar que el WiFi "pise" al Bluetooth
    try:
        wlan.config(pm=network.WLAN.PM_NONE)
    except:
        pass

    # Esperar conexión WiFi
    intentos = 0
    while not wlan.isconnected() and intentos < 15:
        time.sleep(1)
        intentos += 1
        print(".", end="")
        
    if wlan.isconnected():
        try:
            ntptime.settime()
            print("\nWiFi: Conectado y Hora sincronizada")
            advertise() # Encendemos Bluetooth
            lcd.clear()
            
# --- BUCLE PRINCIPAL BLINDADO (Versión Estabilidad Total) ---
            import gc
            
            while True:
                try:
                    # 1. Liberar memoria RAM (Vital para que el Bluetooth no se ahogue)
                    gc.collect()
                    
                    # 2. Calcular hora actual con el ajuste de zona
                    t = time.time() + (TZ_OFFSET * 3600)
                    tm = time.localtime(t)
                    
                    fecha = "{:02d}/{:02d}/{:04d}".format(tm[2], tm[1], tm[0])
                    hora = "{:02d}:{:02d}:{:02d}".format(tm[3], tm[4], tm[5])
                    
                    # 3. Actualizar LCD 
                    # Usamos move_to para no borrar toda la pantalla y evitar parpadeos
                    lcd.move_to(0, 0)
                    lcd.putstr("F: " + fecha)
                    lcd.move_to(0, 1)
                    lcd.putstr("H: " + hora)
                    
                    # 4. PAUSA FRAGMENTADA: 
                    # En lugar de dormir 1 segundo de golpe, dormimos 10 veces 0.1s.
                    # Esto permite que el ESP32 atienda las interrupciones del Bluetooth
                    # con muchísima más fluidez y evita desconexiones por timeout.
                    for _ in range(10):
                        time.sleep(0.1)
                        
                except Exception as e:
                    # Si hay un error de I2C o de cálculo, el reloj no se detiene
                    print(f"Aviso: Reintentando bucle... ({e})")
                    time.sleep(0.5)
                
        except Exception as e:
            lcd.clear()
            lcd.putstr("Error General")
            print("Error crítico:", e)
    else:
        lcd.clear()
        lcd.putstr("Sin WiFi")
        print("Error: No se pudo conectar al WiFi")

if __name__ == "__main__":
    main()
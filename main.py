from machine import Pin, I2C
import time
import network
import ntptime 
from i2c_lcd import I2cLcd
from config import WIFI_SSID, WIFI_PASSWORD, NTP_SERVER, TZ_OFFSET

I2C_SCL_PIN = 5
I2C_SDA_PIN = 4
LCD_ADDR = 0x27 
lcd = None

def init_lcd():
    global lcd
    i2c = I2C(0, scl=Pin(I2C_SCL_PIN), sda=Pin(I2C_SDA_PIN), freq=100000)
    try:
        # Nota: I2cLcd(i2c, direccion, filas, columnas)
        lcd = I2cLcd(i2c, LCD_ADDR, 2, 16)
        return True
    except:
        return False

def main():
    if not init_lcd(): return
    
    lcd.clear()
    lcd.putstr("Conectando...")
    
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)
    
    for _ in range(10):
        if wlan.isconnected(): break
        time.sleep(1)
        
    if wlan.isconnected():
        try:
            ntptime.settime()
            lcd.clear()
            while True:
                t = time.time() + (TZ_OFFSET * 3600)
                tm = time.localtime(t)
                
                # Formatear
                fecha = "{:02d}/{:02d}/{:04d}".format(tm[2], tm[1], tm[0])
                hora = "{:02d}:{:02d}:{:02d}".format(tm[3], tm[4], tm[5])
                
                lcd.move_to(0,0)
                lcd.putstr("F: " + fecha)
                lcd.move_to(0,1)
                lcd.putstr("H: " + hora)
                time.sleep(1)
        except:
            lcd.putstr("Error NTP")
    else:
        lcd.putstr("Sin WiFi")

main()

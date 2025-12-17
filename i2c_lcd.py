import time
from LcdApi import LcdApi

class I2cLcd(LcdApi):
    def __init__(self, i2c, i2c_addr, num_lines, num_columns):
        self.i2c = i2c
        self.i2c_addr = i2c_addr
        self.i2c.writeto(self.i2c_addr, bytes([0]))
        time.sleep_ms(20)
        self.hal_write_init_nibble(0x30)
        time.sleep_ms(5)
        self.hal_write_init_nibble(0x30)
        time.sleep_ms(1)
        self.hal_write_init_nibble(0x30)
        time.sleep_ms(1)
        self.hal_write_init_nibble(0x20)
        time.sleep_ms(1)
        super().__init__(num_lines, num_columns)

    def hal_write_init_nibble(self, nibble):
        byte = ((nibble >> 4) & 0x0f) << 4
        self.i2c.writeto(self.i2c_addr, bytes([byte | 0x04]))
        self.i2c.writeto(self.i2c_addr, bytes([byte]))

    def hal_backlight_on(self):
        self.i2c.writeto(self.i2c_addr, bytes([0x08]))

    def hal_backlight_off(self):
        self.i2c.writeto(self.i2c_addr, bytes([0x00]))

    def hal_write_command(self, cmd):
        self.hal_write_8bits(cmd, 0)

    def hal_write_data(self, data):
        self.hal_write_8bits(data, 1)

    def hal_write_8bits(self, value, rs):
        partial = (value & 0xF0) | (0x08 if self.backlight else 0x00) | rs
        self.i2c.writeto(self.i2c_addr, bytes([partial | 0x04]))
        self.i2c.writeto(self.i2c_addr, bytes([partial]))
        
        partial = ((value << 4) & 0xF0) | (0x08 if self.backlight else 0x00) | rs
        self.i2c.writeto(self.i2c_addr, bytes([partial | 0x04]))
        self.i2c.writeto(self.i2c_addr, bytes([partial]))

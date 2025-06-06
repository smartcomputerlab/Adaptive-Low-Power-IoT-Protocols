from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import time

def display_sensors(sda, scl, luminosity, temperature, humidity, duration):
    # Initialize I2C bus
    i2c = I2C(scl=Pin(scl), sda=Pin(sda), freq=400000)
    # Assuming a 128x64 display:
    width = 128; height = 64
    # Initialize the OLED display
    oled = SSD1306_I2C(width, height, i2c)
    
    oled.fill(0)
    # Write text to display
    oled.text("Sensor readings", 0, 0)
    oled.text("Lux: {:.2f}".format(luminosity), 0, 16)
    oled.text("Temp: {:.2f}".format(temperature), 0, 32)
    oled.text("Humi: {:.2f}".format(humidity), 0, 48)
    oled.show()
    if duration!=0:
        time.sleep(duration)
        oled.poweroff()
        
from machine import Pin, I2C
import sh1106

ID = 1
SCL = 8
SDA = 3

# Initialize I2C
def init_oled():
    i2c = I2C(ID, scl=Pin(SCL), sda=Pin(SDA))

    # Initialize the OLED display
    oled_width = 128
    oled_height = 64
    oled = sh1106.SH1106_I2C(oled_width, oled_height, i2c, rotate=180)

    oled.invert(False)
    oled.contrast = int(10)  # 0 - 255 contrast
    
    return oled, oled_width, oled_height


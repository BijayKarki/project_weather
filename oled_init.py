from machine import Pin, I2C
import sh1106

OLED_WIDTH = 128
OLED_HEIGHT = 64
CONTRAST = 1 #(0 - 255)
ROTATION = 180# current setup requires to be upside down

def init_oled(i2c):
    """
    Initialize and return the SH1106 OLED display.

    Parameters
    ----------
    i2c : machine.I2C
        Already initialized I2C bus for the OLED

    Returns
    -------
    oled : SH1106_I2C object
    width : int
    height : int
    """
    oled = sh1106.SH1106_I2C(OLED_WIDTH, OLED_HEIGHT, i2c, rotate=ROTATION)
    oled.contrast(CONTRAST)
    oled.invert(False)
    return oled, OLED_WIDTH, OLED_HEIGHT


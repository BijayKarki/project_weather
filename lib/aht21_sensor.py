"""
AHT21B Temperature and Humidity Sensor Driver (MicroPython)

This module provides a minimal class-based driver for the AHT21B
temperature and humidity sensor using the I2C interface.

Target platform: RP2040 (and compatible MicroPython boards)
"""

from machine import Pin, I2C
import time


# ---------------------------------------------------------------------------
# I2C CONFIGURATION
# ---------------------------------------------------------------------------

BUS_ID  =   0
SCL_PIN =   5
SDA_PIN =   4

AHT21B_ADDR = 0x38  # Fixed I2C address per AHT21 datasheet


# ---------------------------------------------------------------------------
# SENSOR DRIVER
# ---------------------------------------------------------------------------

class AHT21B:
    """
    Driver class for the AHT21B temperature and humidity sensor.

    Parameters
    ----------
    i2c : machine.I2C
        Initialized I2C bus instance.
    address : int, optional
        I2C address of the sensor (default: 0x38).
    """

    def __init__(self, i2c: I2C, address: int = AHT21B_ADDR) -> None:
        self.i2c = i2c
        self.address = address
        self._initialize()

    def _initialize(self) -> None:
        """
        Perform a soft reset of the sensor.

        According to the AHT21 datasheet, a soft reset is sufficient
        for initialization. No calibration command is required.
        """
        self.i2c.writeto(self.address, b'\xBA')  # Soft reset command
        time.sleep_ms(20)

    def read(self):
        """
        Read temperature and humidity from the sensor.

        Returns
        -------
        tuple(float | None, float | None)
            Temperature in degrees Celsius and relative humidity in percent.
            Returns (None, None) if the sensor is busy.
        """
        # Trigger measurement
        self.i2c.writeto(self.address, b'\xAC\x33\x00')
        time.sleep_ms(80)

        data = self.i2c.readfrom(self.address, 7)

        # Status byte: bit 7 indicates sensor busy
        if data[0] & 0x80:
            return None, None

        # Extract 20-bit humidity value
        hum_raw = ((data[1] << 16) | (data[2] << 8) | data[3]) >> 4
        humidity = hum_raw * 100.0 / 1048576.0  # 2^20

        # Extract 20-bit temperature value
        temp_raw = ((data[3] & 0x0F) << 16) | (data[4] << 8) | data[5]
        temperature = (temp_raw * 200.0 / 1048576.0) - 50.0

        return round(temperature), round(humidity)


# ---------------------------------------------------------------------------
# EXAMPLE USAGE
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    i2c = I2C(BUS_ID, scl=Pin(SCL_PIN),sda=Pin(SDA_PIN))

    aht21_sensor = AHT21B(i2c)

    try:
        while True:
            temp, hum = aht21_sensor.read()

            if temp is not None:
                print(f"Temperature: {temp:.2f} °C | Humidity: {hum:.2f} %")

            time.sleep(5)

    except KeyboardInterrupt:
        print("Measurement stopped by user.")



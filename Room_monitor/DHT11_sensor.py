"""
DHT11 Sensor Reader Script

This script interfaces with a DHT11 sensor using the Raspberry Pi Pico or similar MicroPython-compatible board. 
It reads temperature (in °C) and humidity (in %) from the sensor and prints the results to the console. 

"""

from machine import Pin
import dht
from time import sleep

# Set up the DHT11 sensor
dht_pin = Pin(4)
dht_sensor = dht.DHT11(dht_pin)

def read_dht11():
    """
    Reads temperature and humidity from the DHT11 sensor.

    Returns:
        tuple: (temperature, humidity)  as int if the reading is successful.
        (None, None) if the reading fails due to a sensor error.
    """
    sleep(1)  # Sampling rate for DHT11 = 1 Hz
    
    try:
        dht_sensor.measure()
        temp = dht_sensor.temperature()
        humidity = dht_sensor.humidity()
        return temp, humidity
    except OSError as e:
        print(f"Failed to read from DHT11 sensor: {e}")
        return None, None

# test 
if __name__ == "__main__":
    try:
        while True:
            temp, humidity = read_dht11()
            if temp is not None and humidity is not None:
                print(f"Temperature: {temp}°C, Humidity: {humidity}%")
            else:
                print("Error reading DHT11 sensor.")
    except KeyboardInterrupt:
        print("Interrupted by the user")

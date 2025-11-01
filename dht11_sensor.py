"""
DHT11 Sensor Reader Script

This script interfaces with a DHT11 sensor using the Raspberry Pi Pico or similar MicroPython-compatible board. 
It reads temperature (in °C) and humidity (in %) from the sensor and prints the results to the console. 
"""

from machine import Pin
import dht
from time import sleep

# Lazy initialization
dht_sensor = None

def read_dht11():
    global dht_sensor

    if dht_sensor is None:
        #print("Initializing DHT11...")
        dht_pin = Pin(4)
        dht_sensor = dht.DHT11(dht_pin)
        sleep(1)  # allow sensor to stabilize

    try:
        sleep(2)
        dht_sensor.measure()
        temp = dht_sensor.temperature()
        humidity = dht_sensor.humidity()
        return temp, humidity
    except OSError as e:
        print(f"Failed to read from DHT11 sensor: {e}")
        return None, None

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

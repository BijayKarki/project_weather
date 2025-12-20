from time import sleep, time
import gc
from machine import I2C, Pin, WDT

import config
from Intro_text import scene_first, scene_second, scene_interrupt, display_weather_n_time
from oled_init import init_oled
from open_weather_api import fetch_weather_data
from connect_wifi import connect_wifi, is_connected
from set_time import sync_time
from thingspeak import upload_to_thingspeak
from aht21_sensor import AHT21B
from screen_control import get_screen_status

def initialize_system():
    """Initialize WiFi, NTP, watchdog, I2C buses, OLED, and AHT21B sensor."""
    connect_wifi(config.WIFI_SSID, config.WIFI_PASSWORD)
    sleep(2)
    sync_time()

    wdt = WDT(timeout=60000)

    # --- I2C buses ---
    i2c_oled = I2C(1, scl=Pin(8), sda=Pin(3))
    i2c_sensor = I2C(0, scl=Pin(5), sda=Pin(4))

    # --- Devices ---
    oled, OLED_W, OLED_H = init_oled(i2c_oled)
    sensor = AHT21B(i2c_sensor)

    # Debug scan
    print("OLED bus scan:", [hex(a) for a in i2c_oled.scan()])
    print("AHT21 bus scan:", [hex(a) for a in i2c_sensor.scan()])

    return wdt, oled, OLED_W, OLED_H, sensor

def main_loop():
    wdt, oled, OLED_W, OLED_H, sensor = initialize_system()

    # Startup animation
    scene_first(oled, OLED_W)
    sleep(2)
    scene_second(oled)

    # Initial readings
    room_temp, room_humidity = sensor.read()
    out_temp, out_humidity, wind_speed = None, None, None

    last_time_update = 0
    last_weather_update = 0
    screen_was_on = True

    while True:
        try:
            now = time()
            screen_is_on = get_screen_status()
            sensor_due = now - last_time_update >= 60 or last_time_update == 0
            screen_needs_refresh = screen_is_on != screen_was_on or (screen_is_on and sensor_due)

            if sensor_due:
                try:
                    room_temp, room_humidity = sensor.read()
                except Exception as e:
                    print("[ERROR] AHT21 read failed:", e)
                last_time_update = now

            if screen_is_on and screen_needs_refresh:
                display_weather_n_time(oled, OLED_W, room_temp, room_humidity, out_temp, out_humidity, wind_speed)
            elif not screen_is_on:
                oled.fill(0)
                oled.show()

            screen_was_on = screen_is_on

            # First-time weather fetch
            if last_weather_update == 0:
                try:
                    if is_connected():
                        out_temp, out_humidity, wind_speed = fetch_weather_data()
                        print(f"[{now}] Initial weather fetched")
                    else:
                        print(f"[{now}] WiFi disconnected, skipping initial fetch")
                except Exception as e:
                    print("[ERROR] Initial weather fetch failed:", e)
                last_weather_update = now
 
            # --- Subsequent updates every 15 minutes ---
            
            elif now - last_weather_update >= 900:
                try:
                    if is_connected():
                        out_temp, out_humidity, wind_speed = fetch_weather_data()
                        upload_to_thingspeak(
                            config.THINGSPEAK_API_KEY,
                            room_temp, room_humidity,
                            out_temp, out_humidity, wind_speed,
                            gc.mem_free()
                        )
                        print(f"[{now}] Weather update pushed to ThingSpeak")
                    else:
                        print(f"[{now}] WiFi disconnected, skipping ThingSpeak")
                except Exception as e:
                    print("[ERROR] Weather/ThingSpeak failed:", e)
                last_weather_update = now  # reset timer

            # Periodic GC and watchdog
            if now % 600 < 2:
                gc.collect()
                print(f"[{now}] Forced gc.collect(), free mem: {gc.mem_free()}")
            wdt.feed()
            sleep(0.05)

        except KeyboardInterrupt:
            scene_interrupt(oled)
            break

if __name__ == "__main__":
    main_loop()
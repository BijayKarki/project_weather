from time import sleep, time
import gc
from machine import WDT

import config
from dht11_sensor import read_dht11
from Intro_text import scene_first, scene_second, scene_interrupt, display_weather_n_time
from oled_init import init_oled
from open_weather_api import fetch_weather_data
from connect_wifi import connect_wifi, is_connected
from set_time import sync_time
from thingspeak import upload_to_thingspeak

# --- Setup WiFi + NTP once ---
ssid = config.WIFI_SSID
passphrase = config.WIFI_PASSWORD
connect_wifi(ssid, passphrase)
sync_time()

# --- Startup animation ---
scene_first()  # Welcome animation
scene_second() # Fake mesurement start info

# Display tabular weather and time info 

# --- Watchdog (20s timeout) ---
wdt = WDT(timeout=60000)

try:
    last_weather_update = 0
    last_time_update = 0

    # initial values (safe defaults)
    room_temp, room_humidity = None, None
    out_temp, out_humidity, wind_speed = None, None, None

    while True:
        now = time()
        Memory_count = gc.mem_free()

        # --- Indoor weather + clock update every 60s ---
        if now - last_time_update >= 60 or last_time_update == 0:
            try:
                room_temp, room_humidity = read_dht11()
            except Exception as e:
                print("[ERROR] DHT11 read failed:", e)
                # keep last known values
            print(f"[{now}] Indoor update: {room_temp}°C, {room_humidity}%")

            display_weather_n_time(room_temp, room_humidity, out_temp, out_humidity, wind_speed)
            last_time_update = now

        # --- Outdoor + ThingSpeak every 900s (15 min) ---
        if now - last_weather_update >= 900 or last_weather_update == 0:
            try:
                if is_connected():
                    out_temp, out_humidity, wind_speed = fetch_weather_data()
                    upload_to_thingspeak(
                        config.THINGSPEAK_API_KEY,
                        room_temp, room_humidity,
                        out_temp, out_humidity, wind_speed,
                        Memory_count
                    )
                    print(f"[{now}] Weather update pushed to ThingSpeak")
                else:
                    print(f"[{now}] WiFi disconnected, skipping ThingSpeak")
            except Exception as e:
                print("[ERROR] Weather/ThingSpeak failed:", e)

            display_weather_n_time(room_temp, room_humidity, out_temp, out_humidity, wind_speed)
            last_weather_update = now 

        # --- Periodic GC cleanup every 10 minutes ---
        if now % 600 < 5:  # within 5s window
            gc.collect()
            print(f"[{now}] Forced gc.collect(), free mem: {gc.mem_free()}")

        # --- Reset watchdog each loop ---
        wdt.feed()

        sleep(5)

except KeyboardInterrupt:
    try:
        scene_interrupt()
    except:
        print("OLED did not work. Exiting the program")
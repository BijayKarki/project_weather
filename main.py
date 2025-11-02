from time import sleep, time
import gc
from machine import WDT

import config
from Intro_text import scene_first, scene_second, scene_interrupt, display_weather_n_time
from oled_init import init_oled
from open_weather_api import fetch_weather_data
from connect_wifi import connect_wifi, is_connected
from set_time import sync_time
from thingspeak import upload_to_thingspeak
from dht11_sensor import read_dht11
from screen_control import get_screen_status


def initialize_system():
    """Initialize WiFi, NTP, OLED, watchdog and return initialized objects."""
    # --- WiFi + NTP ---
    connect_wifi(config.WIFI_SSID, config.WIFI_PASSWORD)
    sleep(2)
    sync_time()

    # --- Watchdog (60s timeout) ---
    wdt = WDT(timeout=60000)

    # --- OLED ---
    oled = init_oled()[0]

    return wdt, oled


def main_loop():
    """Main application loop."""
    wdt, oled = initialize_system()
    
    # --- Statup animation ---
    scene_first()
    sleep(1)
    scene_second()

    # --- State trackers ---
    screen_was_on = True
    last_time_update = 0
    last_weather_update = 0

    room_temp, room_humidity = None, None
    out_temp, out_humidity, wind_speed = None, None, None

    while True:
        try:
            now = time()
            screen_is_on = get_screen_status()

            # --- Sensor update every 60s ---
            sensor_due = now - last_time_update >= 60 or last_time_update == 0
            screen_needs_refresh = screen_is_on != screen_was_on or (screen_is_on and sensor_due)

            if sensor_due:
                try:
                    room_temp, room_humidity = read_dht11()
                except Exception as e:
                    print("[ERROR] DHT11 read failed:", e)
                last_time_update = now

            # --- Update OLED display safely ---
            if screen_is_on and screen_needs_refresh:
                display_weather_n_time(room_temp, room_humidity, out_temp, out_humidity, wind_speed)
            elif not screen_is_on:
                oled.fill(0)
                oled.show()

            screen_was_on = screen_is_on

            if last_weather_update == 0:
                # First-time fetch (do NOT push yet)
                try:
                    if is_connected():
                        out_temp, out_humidity, wind_speed = fetch_weather_data()
                        print(f"[{now}] Initial weather fetched (ThingSpeak push will happen after 15 min)")
                    else:
                        print(f"[{now}] WiFi disconnected, skipping initial fetch")
                except Exception as e:
                    print("[ERROR] Initial weather fetch failed:", e)
                last_weather_update = now  # start 15-min timer

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

            # --- Periodic GC cleanup every 10 minutes ---
            if now % 600 < 2:
                gc.collect()
                print(f"[{now}] Forced gc.collect(), free mem: {gc.mem_free()}")

            # --- Feed watchdog ---
            wdt.feed()
            sleep(0.05)  # fast loop for responsive button toggle

        except KeyboardInterrupt:
            try:
                scene_interrupt()
            except Exception:
                print("OLED did not work. Exiting the program")
            break


if __name__ == "__main__":
    main_loop()
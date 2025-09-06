from time import sleep, time
import gc

import config

from dht11_sensor import read_dht11
from Intro_text import scene_first, scene_second, display_weather_n_time
from oled_init import init_oled
from open_weather_api import fetch_weather_data
from connect_wifi import connect_wifi, is_connected
from ntp_sync import sync_time_finland, get_Finnish_time
from thingspeak import upload_to_thingspeak
    

# Connect to WIFI
ssid = config.WIFI_SSID
passphrase = config.WIFI_PASSWORD
connect_wifi(ssid, passphrase)

# Sync time once at the beginning
sync_time_finland()

# Start up OLED display with animated text
scene_first()
scene_second()

# Display tabular weather and time info 

try:
    last_weather_update = 0
    last_time_update = 0

    while True:
        now = time()
        
        # Memory counting 
        Memory_count = gc.mem_free()

        # Update and show current time every 60 seconds
        if now - last_time_update >= 60 or last_time_update == 0:
            
            if now - last_weather_update >= 15 or last_weather_update == 0:
                room_temp, room_humidity = read_dht11()
                out_temp, out_humidity, wind_speed = fetch_weather_data()
                
                # Update weather every 10 minutes
                upload_to_thingspeak(config.THINGSPEAK_API_KEY, room_temp, room_humidity, out_temp, out_humidity, wind_speed, Memory_count)

                display_weather_n_time(room_temp, room_humidity, out_temp, out_humidity, wind_speed)
                
                last_weather_update = now
          
            last_time_update = now
        
        sleep(5)  # Light sleep to avoid busy loop
        
        #print("Free memory: ", gc.mem_free())

except KeyboardInterrupt:
    # Handle program termination (Ctrl+C)
    oled.fill(0)
    oled.text("Terminating", 0, 0)
    oled.text("See you again!", 0, 20)
    oled.show()
    sleep(2)
    oled.fill(0)



import urequests
from time import sleep
import config

from connect_wifi import connect_wifi, is_connected
from set_time import get_local_time


# Fetch weather data
def get_weather():
    api_key = config.WEATHER_API_KEY
    city = 'Espoo'
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    
    try:
        response = urequests.get(url)
        weather_data = response.json()
        response.close()
        
        print(f"City: {weather_data['name']}")
        print(f"Temperature: {weather_data['main']['temp']} °C")
        print(f"Weather: {weather_data['weather'][0]['description']}")
    
    except Exception as e:
        print("Network error:", e)



if __name__ == "__main__":
    import config
    from connect_wifi import connect_wifi, is_connected
    
            
    if not is_connected:
        connect_wifi(config.WIFI_SSID, config.WIFI_PASSWORD)
    
    try:
        # Get and display weather
        while True:
                
            local_time = get_local_time()
            # formatted time printing 
            print(f"\nLocal Time: {local_time[0]}-{local_time[1]:02d}-{local_time[2]:02d} {local_time[3]:02d}:{local_time[4]:02d}:{local_time[5]:02d}")

            get_weather()
            sleep(15)
            
    except KeyboardInterrupt:
        print("Interrupted by the user")
    


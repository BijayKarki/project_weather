import network
import urequests
import ujson
import time

import config



# OpenWeather API details
API_KEY = config.WEATHER_API_KEY  # Replace with your OpenWeather API Key
CITY = config.CITY
URL = f'https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric'

def fetch_weather_data():
    try:
        response = urequests.get(URL)
        if response.status_code == 200:
            data = ujson.loads(response.text)

            # Extract the required weather information
            #print(data)
            temperature = data['main']['temp']
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']

            return temperature, humidity, wind_speed
        else:
            print("Failed to fetch weather data. HTTP Status code:", response.status_code)
    except Exception as e:
        print("An error occurred:", e)
        
if __name__== "__main__":
    
    import config
    from connect_wifi import connect_wifi
    
    ssid = config.WIFI_SSID
    passphrase = config.WIFI_PASSWORD
    connect_wifi(ssid, passphrase)

    
    temperature, humidity, wind_speed = fetch_weather_data()
    # Print the data
    print("Temperature: {:.2f} °C".format(temperature))
    print("Humidity: {} %".format(humidity))
    print("Wind Speed: {:.2f} m/s".format(wind_speed))
            

    
    
    


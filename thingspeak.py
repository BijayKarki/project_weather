from open_weather_api import fetch_weather_data 
from dht11_sensor import read_dht11 
import urequests
import time 

def upload_to_thingspeak(api_key, temp_indoor, humidity_indoor, temp_outdoor, humidity_outdoor, windspeed_outdoor, Memory_count):
    """
    Uploads temperature, humidity, and windspeed data to ThingSpeak.
    Arguments:
        api_key: Your ThingSpeak write API key
        temp: Temperature in °C
        humidity: Relative humidity in %
        windspeed: in km/s
    """
    
    url = "http://api.thingspeak.com/update"
    data = {
        "api_key": api_key,
        "field1": temp_indoor,
        "field2": humidity_indoor,
        "field3": temp_outdoor,
        "field4": humidity_outdoor,
        "field5": windspeed_outdoor,
        "field5": Memory_count
    }
    
    try:
        response = urequests.post(url, json=data)
        print("ThingSpeak response:", response.text)
        response.close()
    except Exception as e:
        print("Failed to upload to ThingSpeak:", e)
        


if __name__ == "__main__":
    import config
    api_key = config.THINGSPEAK_API_KEY
    temp = 10
    humidity= 10
    for i in range(10):
        print("mock test", i)
    
        upload_to_thingspeak(api_key, temp, humidity)
        temp += 5
        humidity += 5
        time.sleep(60)

# config.py

# Instructions: Copy this file to 'config.py' and fill in your actual credentials.
# Do NOT commit 'config.py' to GitHub.

# Wi-Fi credentials
WIFI_SSID = ""
WIFI_PASSWORD = ""

# ThingSpeak
THINGSPEAK_API_KEY = ""

# Weather API (optional, if using a token or custom service)
WEATHER_API_KEY = ""
CITY = ""


# MQTT
MQTT_BROKER = "0.0.0.0"            # Your Mosquitto or Home Assistant IP
MQTT_PORT = 1883                   # Default is 1883 (non-TLS) or 8883 (TLS)
MQTT_CLIENT_ID = "my_device_id"
MQTT_USERNAME = "your_username"
MQTT_PASSWORD = "your_password"

MQTT_STATE_TOPIC = b"home/sensor/state"
MQTT_AVAIL_TOPIC = b"home/sensor/availability"
MQTT_PUBLISH_INTERVAL = 60         # Interval in seconds
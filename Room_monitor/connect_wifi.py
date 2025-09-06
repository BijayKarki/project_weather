import network
from time import time, sleep

wlan = network.WLAN(network.STA_IF)

def connect_wifi(SSID, password, timeout=30):
    """
    Establishes connection to a wireless network for the given credentials.
    The function is limited to be timeouted in ~30 sec by default.
    
    Input - SSID, password (and timeout = 30 secs by default)
    
    Output- print statement
    """
        
    try :
        
        # connect to wifi
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(SSID, password)
        
        # start time
        start_time = time()
        
        # wait until connected or timeout limit 
        while not wlan.isconnected() and (time() - start_time) < timeout:
            print("Waiting for connection...")
            sleep(1)
        
        if wlan.isconnected():
            print('\nConnected to Wi-Fi')
            print('IP Address:', wlan.ifconfig()[0])
        else:
            print(f"\nConnection attemp timed out ~{timeout} secs.")
        
    except Exception as e:
        print("An unexpected error occurred:", e)
        

def is_connected():
    return wlan.isconnected()


# Not sure if the following function is needed" 
def ensure_connection():
    if not is_connected():
        print('Wi-Fi disconnected. Attempting reconnect...')
        return connect()
    return True


if __name__ == "__main__":
    import config
    ssid = config.WIFI_SSID
    passphrase = config.WIFI_PASSWORD
    connect_wifi(ssid, passphrase)
    print(is_connected())

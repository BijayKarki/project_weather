import ntptime
import time

# Function to calculate if a given date is during DST in Finland
def is_dst(year, month, day):
    """ Returns True if the date is within DST for Finland, otherwise False """
    # DST starts last Sunday of March and ends last Sunday of October
    def last_sunday(year, month):
        # Find the last day of the month
        last_day = time.mktime((year, month + 1, 1, 0, 0, 0, 0, 0)) - 24*3600 if month != 12 else time.mktime((year + 1, 1, 1, 0, 0, 0, 0, 0)) - 24*3600
        last_day_tuple = time.localtime(last_day)
        # Go back to the previous Sunday
        return last_day_tuple[2] - last_day_tuple[6]

    last_sunday_march = last_sunday(year, 3)
    last_sunday_october = last_sunday(year, 10)

    # If between the last Sunday of March and the last Sunday of October, DST is active
    if (month > 3 and month < 10) or (month == 3 and day >= last_sunday_march) or (month == 10 and day < last_sunday_october):
        return True
    return False

# Function to adjust the time for Finland's timezone
def get_Finnish_time():
    try:
        # Get the current UTC time from the microcontroller's internal clock
        current_time = time.localtime()

        # Adjust for Finland's standard timezone (UTC + 2 hours)
        finland_offset = 2 * 3600  # +2 hours in seconds

        # Check if DST is in effect
        if is_dst(current_time[0], current_time[1], current_time[2]):
            finland_offset += 3600  # Add an additional +1 hour for DST

        # Adjust the current time for Finland
        finland_time = time.localtime(time.mktime(current_time) + finland_offset)

        return finland_time

    except Exception as e:
        print('Error adjusting time for Finland:', str(e))

# Sync time using NTP and set the internal clock
def sync_time_finland():
    try:
        #print('Syncing time with NTP...')
        ntptime.settime()  # Sync with NTP server (UTC time)
        #print('\nTime synced successfully!')

    except Exception as e:
        print('Error syncing time:', str(e))


if __name__ == "__main__":
    
    import config
    from connect_wifi import connect_wifi
    
    ssid = config.WIFI_SSID
    passphrase = config.WIFI_PASSWORD
    connect_wifi(ssid, passphrase)

    # Sync time once at the beginning
    sync_time_finland()

    # Continuously update the time in Finland and print every 10 seconds
    for i in range(5):
        real_time = get_Finnish_time()
        # Format the time for printing
        formatted_time = "{:02d}:{:02d}:{:02d} {:02d}-{:02d}-{:04d}".format(
            real_time[3], real_time[4], real_time[5], real_time[2], real_time[1], real_time[0])
        print('Formatted Finland time:', formatted_time)
        time.sleep(10)


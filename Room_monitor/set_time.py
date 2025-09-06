import ntptime
import time

ntptime.host = 'fi.pool.ntp.org'  # For Finland's NTP pool


# Set time using NTP
def set_time():
    try:
        print("Setting time...")
        ntptime.settime()  # Set the RTC to UTC time from NTP
    except Exception as e:
        print(f"Failed to set time: {e}")

# Call the function to sync the time
set_time()

# Convert UTC time to local time zone (for example, UTC+3)
def get_local_time(offset_hours=3):
    current_time = time.localtime(time.time() + offset_hours * 3600)
    return current_time

if __name__ == "__main__":    
    # Display the local time
    local_time = get_local_time()
    print(f"Local Time: {local_time[0]}-{local_time[1]:02d}-{local_time[2]:02d} {local_time[3]:02d}:{local_time[4]:02d}:{local_time[5]:02d}")


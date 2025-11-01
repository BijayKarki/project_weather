"""
set_time.py
------------
Syncs the internal RTC clock with an NTP server (UTC time).
Provides a helper to get the local Finland time (UTC+2 / UTC+3 DST).
"""

import ntptime
import time

# Use Finnish NTP pool
ntptime.host = 'fi.pool.ntp.org'  

def sync_time():
    """Syncs device RTC to UTC using NTP."""
    try:
        print("Syncing time with NTP...")
        ntptime.settime()  # This sets the RTC in UTC
        print("NTP sync successful!")
    except Exception as e:
        print(f"Failed to sync time: {e}")

def is_dst(year, month, day):
    """Returns True if Finland is in DST on this date."""
    def last_sunday(year, month):
        # Days in each month (ignoring leap year Feb since not relevant for March/Oct)
        days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        last_day = days_in_month[month - 1]
        # Get weekday of the last day
        wd = time.localtime(time.mktime((year, month, last_day, 0, 0, 0, 0, 0)))[6]
        # Go back to previous Sunday
        return last_day - wd

    last_sunday_march = last_sunday(year, 3)
    last_sunday_october = last_sunday(year, 10)

    # DST active: from last Sunday in March to last Sunday in October
    if (month > 3 and month < 10) or (month == 3 and day >= last_sunday_march) or (month == 10 and day < last_sunday_october):
        return True
    return False


def get_Finnish_time():
    """Return Finland local time tuple (UTC+2 standard, +3 during DST)."""
    utc = time.localtime()
    offset = 2 * 3600  # Standard offset
    if is_dst(utc[0], utc[1], utc[2]):
        offset += 3600
    return time.localtime(time.time() + offset)

if __name__ == "__main__":
    sync_time()
    local = get_Finnish_time()
    print("Finland Local Time: {:02d}:{:02d}:{:02d} {:02d}-{:02d}-{:04d}".format(
        local[3], local[4], local[5], local[2], local[1], local[0]
    ))

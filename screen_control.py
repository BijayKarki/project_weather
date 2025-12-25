from machine import Pin
from utime import ticks_ms, ticks_diff
from set_time import get_Finnish_time

# --------------------------------------------------
# Configuration
# --------------------------------------------------
BUTTON_PIN = 13
DEBOUNCE_MS = 300
NIGHT_START = 22            # Night mode starts
NIGHT_END = 6               # Night mode ends
TEMP_DISPLAY_MS = 10_000    # 10 ms temporary display

# --------------------------------------------------
# State
# --------------------------------------------------
screen_status = True
_last_irq_time = 0
_temp_override_start = 0  # timestamp when temporary night display started

# --------------------------------------------------
# Button (IRQ-based)
# --------------------------------------------------
button = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_UP)

def _button_irq(pin):
    global screen_status, _last_irq_time, _temp_override_start
    now = ticks_ms()
    if ticks_diff(now, _last_irq_time) > DEBOUNCE_MS:
        local_hour = get_Finnish_time()[3]

        if NIGHT_START <= local_hour or local_hour < NIGHT_END:
            # Night mode: temporary display
            if _temp_override_start > 0:
                # Already showing → force turn off
                _temp_override_start = 0
            else:
                # Activate temporary display
                _temp_override_start = now
        else:
            # Daytime: normal toggle
            screen_status = not screen_status

        _last_irq_time = now


button.irq(trigger=Pin.IRQ_FALLING, handler=_button_irq)

# --------------------------------------------------
# Screen policy
# --------------------------------------------------
def get_screen_status():
    """
    Returns True if screen should be ON, False if OFF.

    Rules:
    - Night mode enforced between NIGHT_START and NIGHT_END
    - Temporary override allows screen ON for TEMP_DISPLAY_MS at night
    - Button toggles screen normally during daytime
    """

    global _temp_override_start
    local_time = get_Finnish_time()
    hrs = local_time[3]
    now_ms = ticks_ms()

    # Night time logic
    if NIGHT_START <= hrs or hrs < NIGHT_END:
        if _temp_override_start > 0 and ticks_diff(now_ms, _temp_override_start) < TEMP_DISPLAY_MS:
            return True  # temporary display active
        return False  # night mode off

    # Daytime
    return screen_status


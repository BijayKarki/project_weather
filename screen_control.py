from machine import Pin
from time import localtime, time

button = Pin(13, Pin.IN, Pin.PULL_UP)
screen_status = True
button_prev = button.value()
last_toggle_time = 0
debounce_delay = 0.2  # non-blocking debounce
manual_override = False

def get_screen_status():
    """
    Returns True if screen should be ON, False if OFF.
    Manual button toggle always works.
    Auto-off only if no manual override.
    """
    global screen_status, button_prev, last_toggle_time, manual_override

    now = time()
    hrs = localtime()[3]

    # --- Manual toggle ---
    if not button.value() and button_prev and (now - last_toggle_time) > debounce_delay:
        screen_status = not screen_status
        last_toggle_time = now
        manual_override = True

    button_prev = button.value()

    # --- Time-based auto-off if no manual override ---
    if not manual_override:
        if screen_status and (hrs >= 22 or hrs < 6):
            screen_status = False

    return screen_status

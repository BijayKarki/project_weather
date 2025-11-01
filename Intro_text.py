from time import sleep
from oled_init import init_oled
from set_time import sync_time, get_Finnish_time

# Start up LED and text message
text1 = "WELCOME TO"
text2 = "Project: Weather"
text3 = ""

# Initialize oled
oled, oled_width, oled_height = init_oled()

def scene_first():

    # Display the first line (static)
    oled.text(text1, 24, 0)
    oled.show()

    # Start positions for text2 and text3
    text2_pos = 130  # Start from the right for text2 (left to right)
    text3_pos = -130  # Start from the left for text3 (right to left)

    # Run both animations in the same loop until they align at x = 0
    while text2_pos > 0 or text3_pos < 0:
        # Clear the previous text at line 15 and line 25
        oled.fill_rect(0, 15, oled_width, 10, 0)  # Clear line 15
        oled.fill_rect(0, 25, oled_width, 10, 0)  # Clear line 25

        # Update text2 (line 15) if still animating
        if text2_pos > 0:
            oled.text(text2, text2_pos, 15)
            text2_pos -= 1  # Move left (left to right)

        # Update text3 (line 25) if still animating
        if text3_pos < 0:
            oled.text(text3, text3_pos, 25)
            text3_pos += 1  # Move right (right to left)

        # Show updated screen
        oled.show()
        sleep(0.01)  # Adjust speed if needed

    # After the loop, align both texts at x = 0
    oled.fill_rect(0, 15, oled_width, 10, 0)  # Clear line 15
    oled.fill_rect(0, 25, oled_width, 10, 0)  # Clear line 25

    oled.text(text2, 0, 15)  # Align text2 at x = 0
    oled.text(text3, 0, 25)  # Align text3 at x = 0
    oled.show()
    sleep(3)
    
def scene_second():
    #LED blinking + mock animation
    oled.fill(0)
    text1 = "Measurement"
    text2 = "Starting" 
    oled.text(text1, 0, 0)
    oled.text(text2, 0, 15)
    oled.show()

    for i in range(10):
        oled.text(".", (65 + (i*7)), 15)
        oled.show()
        sleep(.2)
    oled.fill(0)
    
def scene_interrupt():
    oled.fill(0)
    oled.text("Terminating", 0, 0)
    oled.text("See you again!", 0, 20)
    oled.show()
    sleep(2)
    oled.fill(0)
   
def clear_line(y, length):
    """Clear a line of text at a specific y-coordinate"""
    oled.fill_rect(0, y, length, 8, 0)  # Adjust height based on font size

def draw_table():
    """Draw table with horizontal and vertical lines."""
    
    # Draw horizontal lines
    h_line_value = 12
    oled.hline(35, h_line_value*0, oled_width,1)
    oled.hline(0, h_line_value, oled_width, 1)    # Header line
    oled.hline(0, h_line_value*2, oled_width, 1)  # Below temperature
    oled.hline(0, h_line_value*3, oled_width, 1)  # Below humidity
    oled.hline(0, h_line_value*4, oled_width, 1)  # Below wind speed

    # Draw vertical lines
    v_line_1 = 0
    v_line_2 = 35
    v_line_3 = 73
    
    oled.vline(v_line_1, h_line_value, h_line_value*3, 1)  # Between "Id" and "Room"
    oled.vline(v_line_2, 0, h_line_value*4, 1)             # Between "Id" and "Room"
    oled.vline(v_line_3, 0, h_line_value*4, 1)             # Between "Room" and "Outdoor"


def display_weather(room_temp, room_humidity, out_temp, out_humidity, wind_speed, weekday):
    """Display the weather data along with table layout"""
    
    # Clear display for weather data
    oled.fill(0)

    # Write the header row
    oled.text(f"{weekday}", 0, 3)
    oled.text("Room", 37, 3)
    oled.text("Outdoor", 75, 3)

    # Display temperature
    clear_line(16, oled_width)
    oled.text("Temp", 2, 15)
    oled.text(f"{room_temp} C", 40, 15)     # Room temperature
    oled.text(f"{out_temp} C", 80, 15)      # Outdoor temperature

    # Display humidity
    clear_line(27, oled_width)
    oled.text("RH", 2, 27)
    oled.text(f"{room_humidity}%", 40, 27)  # Room humidity
    oled.text(f"{out_humidity}%", 80, 27)   # Outdoor humidity

    # Display wind speed
    clear_line(39, oled_width)
    oled.text("Wind", 2, 39)
    oled.text("--", 40, 39)                 # Placeholder for room wind speed
    oled.text(f"{wind_speed} km/h", 80, 39) # Outdoor wind speed
    
    # Draw the table lines
    draw_table()
    

def display_weather_n_time(room_temp, room_humidity, out_temp, out_humidity, wind_speed, weekday=None, time_str=None, date_str=None):
    oled.fill(0)
    current_time = get_Finnish_time()
    hour, minute = current_time[3:5]
    weekday = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][current_time[6]]
    time_str = "{:02d}:{:02d}".format(hour, minute)
    date_str = "{:04d}.{:02d}.{:02d}".format(current_time[0], current_time[1], current_time[2])

    clear_line(53, oled_width)
    oled.text(f"{time_str},{date_str}", 0, 54)
    oled.show()
    display_weather(room_temp, room_humidity, out_temp, out_humidity, wind_speed, weekday)
    oled.text(f"{time_str},{date_str}", 0, 54)
    oled.show()


    
    
if __name__ == "__main__":
    sync_time()
    
    print("Printing first function to your LED")
    scene_first()
    print("\nPrinting second function to your LED")
    scene_second()
    print("\nPrinting weather info to your LED")
    display_weather_n_time(23, 50, 20, 75, 15, "SAT")
    oled.show()


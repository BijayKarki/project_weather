# Mini weather station

This is the third iteration of the project. Current implementation features a use of ESP32-S3 board programmed in MicroPython.
The WiFi connection capability of the board features real time tracker and API call for outdoor weather information. The data gathered is finally pushed to <a href=https://thingspeak.mathworks.com/channels/3024639> ThingSpeak </a> for easy acccess and visualization purposes.

## Components used

1. ESP32-S3 board
2. DHT11 sensor
3. 1.3 inch OLED display
4. Breadboard and Jumper wires

## Tech stack:

1. ntptime
2. <a href="https://github.com/robert-hh/SH1106/blob/master/readme.md"> SH1106 </a> (For 1.3" OLED display)
3. <a href="https://thingspeak.mathworks.com/"> ThingSpeak </a>

## Future updated

1. Real time tracker
2. Outdoor weather information
3. Online data visualization (public access)

## Aditional info

- `ssd1306` library does not support 1.3 inch OLED display. This <a href="https://github.com/robert-hh/SH1106/blob/master/readme.md"> documentation </a> offers the solution.

- <a href="https://docs.micropython.org/en/latest/esp32/tutorial/intro.html"> Documentation </a> for flashing MicroPython firmware to ESP32 boards.

- Note: If the board is a clone, please flash at "0x00" not "0x10000".
  <a href="https://github.com/orgs/micropython/discussions/10206"> Discussion </a>

## Functional Setup

<p align="center"> <img align="center" height = 500, src="./docs/IMG_6473.png"/> </p>

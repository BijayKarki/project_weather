# Mini weather station

This is the third iteration of the project. Current implementation features a use of ESP32-S3 board programmed in MicroPython.
The WiFi connection capability of the board features real time tracker and API call for outdoor weather information.
The data gathered is pushed to ThingSpeak for visualization and acccess purposes.

## Components used

1. ESP32-S3 board
2. DHT11 sensor
3. 1.3 inch OLED display
4. Breadboard and Jumper wires

## Tech stack:

1. ntptime
2. <a href="https://github.com/robert-hh/SH1106/blob/master/readme.md"> SH1106 </a> (For 1.3" OLED display)
3. <a href="https://thingspeak.mathworks.com/"> ThingSpeak </a>

## Features

1. Real time tracker
2. Outdoor weather information
3. <a href=https://thingspeak.mathworks.com/channels/3024639> Data dashboard </a> (Public access)

## Problems encountered

| Sn. | Problem                                          | Cause                                                       | Solution opted                           |
| --- | :----------------------------------------------- | :---------------------------------------------------------- | :--------------------------------------- |
| 1   | The system freezes after few of days or run time | Unknown processes or memory leak or dht11 sensor            | watch dog (60 sec timer)                 |
| 2   | Time syncing issuce (DST)                        | Static hrs added to UTC                                     | Dynamic hrs +2 or +3 depending on season |
| 3   | DHT11 sensor does reads only after a min         | NA: works perfectly in thonny but not when plugged to power |                                          |

## Future work

1. Run main.py connected to a computer and record the log to pin point the exact cause of the system freezes.
2. An option to turn ON/OFF the OLED screen as per need
3. May be different views on the screen

## Aditional info for ESP32 setup

- `ssd1306` library does not support 1.3 inch OLED display. This <a href="https://github.com/robert-hh/SH1106/blob/master/readme.md"> documentation </a> offers the solution.

- <a href="https://docs.micropython.org/en/latest/esp32/tutorial/intro.html"> Documentation </a> for flashing MicroPython firmware to ESP32 boards.

- Note: If the board is a clone, please flash at "0x00" not "0x10000".
  <a href="https://github.com/orgs/micropython/discussions/10206"> Discussion </a>

## Functional Setup

<p align="center"> <img align="center" height = 500, src="./docs/IMG_6473.png"/> </p>

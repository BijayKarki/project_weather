# Project Weather

What is your room temperature ?

A learning journey and desire to sense the weather using embedded system.

---

## Overview

<B> Project Weather: </B>

The cold autumn of 2024 was an opportunity for me to start measuring the room temperature.

So, it started by putting together the tiny pieces of hardware and novice python skills. The result was a local temperature and humidity logger using the **Raspberry Pi Pico (RP2040)**.

Over time it evolved into a connected **IoT weather station** using the **ESP32-S3** microcontroller.

The initial goal was just to measure the indoor temperature. However it is much more now;
<br> **measure → observer → connect → keep exploring**.</br>

---

## Evolution

| Stage |  Branch                                                                         | Highlights                                                 | MCU                    |
| ----- | --------------------------------------------------------------------------------| -----------------------------------------------------------|------------------------|
| 1     | [pico-zero-V1](https://github.com/BijayKarki/project_weather/tree/pico-zero)    |Reads DHT11 sensor, displays data locally on an OLED screen | RPi-Pico-Zero (RP2040) |
| 2     | [pico-zero-V2](https://github.com/BijayKarki/project_weather/tree/pico-zero-LED)|feats: onboard LED indicators + TEXT animation              | RPi-Pico-Zero (RP2040) |
| 3     | [esp32-s3](https://github.com/BijayKarki/project_weather/tree/ESP32-S3)         |Adds Wi-Fi connectivity, real time, urequests, cloud upload | ESP32-S3               |

Each branch represents a progression towards adding something more.<br>
**Local sensing** → **Online Sensing**.

---

## Technical Highlights

- **Microcontrollers:** Raspberry Pi Pico (RP2040), ESP32-S3
- **Sensor:** DHT11 (Temperature & Humidity)
- **Languages:** MicroPython
- **Connectivity:**
  - Pico → OLED display (I2C)
  - ESP32-S3 → Wi-Fi (HTTP + thingspeak)
- **Development Tools:** Thonny, VS Code,
- **Hardware Interfaces:** GPIO, I²C
- **Planned Extensions:**
  - Cloud dashboard and data visualization
  - Low-power sleep modes for energy efficiency

## Lessons Learned

- Interfacing and calibrating environmental sensors
- Memory and timing optimization on constrained MCUs
- Implementing Wi-Fi and network stacks on embedded devices
- visualizing the data on cloud dashboard
- Exploring upython and coding
- Solving more problems as the project evolves

---

## Repository Structure

- project_weather/
  - README.md
  - pico-zero/
  - pico-zero-LED/
  - esp32-s3/

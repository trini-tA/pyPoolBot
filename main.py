from machine import Pin, I2C
import ssd1306

import utime as time
from screen import Screen
from server import Server
from measures import Measures
from ifconfig import IFCONFIG
import socket
import json


VERSION = "0.1"
NAME = "Pool"

DISPLAY_NAME = NAME + " " + VERSION

PIN_NO_USE_A = 0            # on board -> D3
PIN_TEMP = 2                # on board -> D4

PIN_NO_USE_B = 16           # on board -> D0
PIN_NO_USE_C = 14           # on board -> D5
PIN_LED_RELAY_STATUS = 13   # on board -> D6
PIN_LED_SYSTEM_STATUS = 12  # on board -> D7

PIN_OLED_SCL = 5            # on board -> D1
PIN_OLED_SDA = 4            # on board -> D2

# Led
relay_led = Pin(PIN_LED_RELAY_STATUS, Pin.OUT)
system_led = Pin(PIN_LED_SYSTEM_STATUS, Pin.OUT)
relay_led.on()
system_led.on()

# using default address 0x3C
i2c = I2C(sda=Pin(PIN_OLED_SDA), scl=Pin(PIN_OLED_SCL))
display = ssd1306.SSD1306_I2C(64, 48, i2c)
Screen.start_screen( display, VERSION )
time.sleep(2)
Screen.clear_screen( display, VERSION )
relay_led.off()
system_led.off()

# measure
ds = Measures.init(PIN_TEMP)

while True:
    display.text(DISPLAY_NAME, 0, 0, 1)

    try:
        pool, ext = Measures.get_data(ds)

        Screen.print_screen( display, pool, ext, False, 10)
        system_led.on()

    except:
        system_led.off()
        relay_led.off()
        output = 'ERR!!'
        display.text(output, 0, 40, 1)

    time.sleep(2)
    Screen.clear_screen( display, VERSION )

    #Server.pin_status()


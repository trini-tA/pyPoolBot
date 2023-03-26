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

# //////////////////////////////////////////////////////////////////////////
PIN_TEMP = 2                # on board -> D4

#screen
PIN_OLED_SCL = 5            # on board -> D1
PIN_OLED_SDA = 4            # on board -> D2

# using default address 0x3C
i2c = I2C(sda=Pin(PIN_OLED_SDA), scl=Pin(PIN_OLED_SCL))
display = ssd1306.SSD1306_I2C(64, 48, i2c)
Screen.start_screen( display, DISPLAY_NAME )
time.sleep(2)

# network
ip_address = IFCONFIG.get_address()
short_ip_address = ip_address.split( '.' )

# Server
time.sleep(2)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((ip_address, 80))
s.listen(1)


# measure
d = DHT11.load_sensor( PIN_TEMP )
count = 0

Screen.clear_screen( display, DISPLAY_NAME )
Screen.show_ip( display, short_ip_address[3] )

output_html = True

while True:
    cl, addr = s.accept()
    print('client connected from', addr)
    cl_file = cl.makefile('rwb', 0)
    request = cl.recv(2048)
    parseRequest = request.decode('utf-8').split(' ')

    if parseRequest[0] == 'GET':
        params = parseRequest[1]
        if params == '/html':
            output_html = True

        if params == '/json':
            output_html = False

    # Response
    d.measure()
    time.sleep(2) # wait !
    Screen.clear_screen(display, DISPLAY_NAME)
    temp = d.temperature()
    hum = d.humidity()
    count = count + 1
    Screen.print_screen_dht11(display, temp, hum, short_ip_address[3], count)

    sensors = [
        {
            'datetime': None,
            'deviceName': "esp8266-sensors",
            'temperature': float(temp),
            'pressure': float(0.0),
            'humidity': float(hum),
            'isValid': True
        }
    ]

    if output_html:
        html = '';
        for data in sensors:
            html = html + '<div><label>{}</label><span class="class-{}">{}</span></div>\n'.format(data.get('name'),
                                                                                                  data.get('name'),
                                                                                                  data.get('value'))
        response = Server.template(DISPLAY_NAME) % html
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n'.encode())
    else:
        response = json.dumps( sensors )
        cl.send('HTTP/1.0 200 OK\r\nContent-type: application/json\r\n\r\n'.encode())

    cl.send(response.encode())
    cl.close()


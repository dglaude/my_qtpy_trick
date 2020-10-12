# Demonstration of the new usb_hid.devices[0].last_received_report on QT-Py
# NUM_LOCK, CAPS_LOCK and SCROLL_LOCK indicator.
# Tested with "Adafruit CircuitPython 6.0.0-beta.2 on 2020-10-05; Adafruit QT Py M0 with samd21e18"
#
# Require the following content in the lib directory:
# adafruit_hid (folder)
# adafruit_pypixelbuf.mpy
# neopixel.mpy

import board
import time
import neopixel
import usb_hid

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS

pixel = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.2)
kbd = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(kbd)

while True:
    report = int.from_bytes(usb_hid.devices[0].last_received_report, "big")  # See https://github.com/adafruit/circuitpython/pull/3302
    red = (report & 0x01) == 0x01  # NUM LOCK
    green = (report & 0x02) == 0x02  # CAPS LOCK
    blue = (report & 0x04) == 0x04  # SCROLL LOCK
    pixel.fill( (0xFF if red else 0x0, 0xFF if green else 0x0, 0xFF if blue else 0x0) )
    time.sleep(0.1)

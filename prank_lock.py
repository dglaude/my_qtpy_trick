# Demonstration of the new usb_hid.devices[0].last_received_report
# Prank with QT-Py: the NUM_LOCK, CAPS_LOCK and SCROLL_LOCK disabler.
# Requires Firmware above 6.0.0-alpha3 or night build after 11 September 2020
import board
import time
import usb_hid

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

kbd = Keyboard(usb_hid.devices)
time.sleep(1)

while True:
    report = int.from_bytes(usb_hid.devices[0].last_received_report, "big")  # See https://github.com/adafruit/circuitpython/pull/3302
    if (report & 0x01) == 0x01:
        kbd.send(Keycode.KEYPAD_NUMLOCK)
    if (report & 0x02) == 0x02:
        kbd.send(Keycode.CAPS_LOCK)
    if (report & 0x04) == 0x04:
        kbd.send(Keycode.SCROLL_LOCK)
    time.sleep(0.1)

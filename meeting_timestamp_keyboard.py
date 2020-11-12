# CircuitPython meeting timestamp encoder for QT-Py (using Scroll Lock)
#
# Use:
# * Connect to your computer
# * At startup, the QT-Py will force the "Scroll Lock" on
# * Press "Scroll Lock" when the meeting start
# * When you need a timestamp, position your cursor and press "Scroll Lock"
# 
# Tested with "Adafruit CircuitPython 6.0.0-rc.1 on 2020-11-03; Adafruit QT Py M0 with samd21e18"
#
# Rename this file as 'code.py'.
# Require the following content in the lib directory:
# adafruit_hid (folder)
# adafruit_pypixelbuf.mpy
# neopixel.mpy

import board
import time
import usb_hid
import neopixel

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS

pixel = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.2)

time.sleep(1)                   # sleep for a bit to avoid a race condition on some systems
kbd = Keyboard(usb_hid.devices) # the keyboard object!
layout = KeyboardLayoutUS(kbd)  # you're americans :)

num_lock = False          # NUM LOCK
caps_lock = False         # CAPS LOCK
scroll_lock = False       # SCROLL LOCK

def update_lock():
    global num_lock, caps_lock, scroll_lock
    report = int.from_bytes(usb_hid.devices[0].last_received_report, "big")
    num_lock = (report & 0x01) == 0x01          # NUM LOCK
    caps_lock = (report & 0x02) == 0x02         # CAPS LOCK
    scroll_lock = (report & 0x04) == 0x04       # SCROLL LOCK

update_lock()
if not scroll_lock:                     # Force the Scroll lock to be ON
    kbd.send(Keycode.SCROLL_LOCK)
    print("Scroll lock forced.")
    time.sleep(0.5)

print("Press 'Scroll lock' to start the meeting timer.")    # Wait for the Scroll Lock to be disabled to start the timer.

scroll_lock=True
while scroll_lock:
    update_lock()
    time.sleep(0.1)

print("Meeting starting")

start=time.monotonic()          # Press reset on your board to reset the time
previous_scroll_lock=False
while True:
    update_lock()
    pixel.fill( (0xFF if num_lock else 0x0, 0xFF if caps_lock else 0x0, 0xFF if scroll_lock else 0x0) ) # Create a color

    if scroll_lock!=previous_scroll_lock:
        now=time.monotonic()
        current=now-start
        hours=int((current/3600))
        minutes=int((current/60)%60)
        seconds=int(current%60)
        if hours==0:
            string = "{minutes:02d}:{seconds:02d} ".format(minutes=minutes, seconds=seconds)
        else:
            string = "{hours}:{minutes:02d}:{seconds:02d} ".format(hours=hours, minutes=minutes, seconds=seconds)
        print("Sending : ", string)
        layout.write(string)
        previous_scroll_lock=scroll_lock

    time.sleep(0.1)

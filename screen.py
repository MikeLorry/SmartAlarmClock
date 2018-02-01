#!/usr/bin/python
import time
import signal
import scrollphathd
from scrollphathd.fonts import font5x5

class ScrollpHatHD:
    "ScrollpHatHD class to allow interaction with the Pimoroni Scroll pHat HD LED matrix"

    # Default values
    default_mode = "clock"
    default_brightness = 0.3

    def __init__(self):
        # Set default display mode
        self.mode = ScrollpHatHD.default_mode
        print "Screen mode: " + self.mode

        # Set brightness to default
        self.brightness = ScrollpHatHD.default_brightness
        print "Screen brightness: " + str(self.brightness)

        # Set mode index: value used for modes that needs an incrementing value
        self.index = 0

    def show(self):
        scrollphathd.clear()
        if self.mode == "clock":
            self.clock()
        if self.mode == "demo":
            self.demo()
            if self.index >= 200:
                self.mode = "clock"
                self.index = 0
        scrollphathd.show()
        return

    def clock(self):
        scrollphathd.write_string(time.strftime("%H:%M"), x=0, y=0,  font=font5x5, brightness=self.brightness)
        return

    def demo(self):
        self.index += 2
        s = math.sin(self.index/ 50.0) * 2.0 + 6.0

        for x in range(0, 17):
            for y in range(0, 7):
                v = 0.3 + (0.3 * math.sin((x * s) + self.index/ 4.0) * math.cos((y * s) + self.index/ 4.0))

                scrollphathd.pixel(x, y, v)

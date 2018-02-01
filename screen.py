#!/usr/bin/python
import time
import math
import scrollphathd
from scrollphathd.fonts import font5x5

class ScrollpHatHD:
    "ScrollpHatHD class to allow interaction with the Pimoroni Scroll pHat HD LED matrix"

    # Default values
    default_mode = "demo"
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
        elif self.mode == "demo":
            self.demo()
            if self.index >= 100:
                self.mode = "clock"
                self.index = 0
        elif self.mode == "clock_vol":
            self.clock()
            self.volume_bar()
            if self.index >= 60:
                self.mode = "clock"
                self.index = 0
        scrollphathd.show()
        return

    def set_brightness(self):
        brightness_min = 0.3
        brightness_step = 0.3
        if self.brightness + brightness_step > 1:
            self.brightness = brightness_min
        else:
            self.brightness = self.brightness + brightness_min
        print "Screen brightness: " + str(self.brightness)
        return

    def clock(self):
        scrollphathd.write_string(time.strftime("%H:%M"), x=0, y=0,  font=font5x5, brightness=self.brightness)
        return

    def volume_bar(self, volume):
        self.index += 1
        y = 6
        x_max = int(volume * 0.17)
        for x in range(x_max):
            scrollphathd.set_pixel(x, y, self.brightness)
        return

    def demo(self):
        self.index += 2
        s = math.sin(self.index/ 50.0) * 2.0 + 6.0

        for x in range(0, 17):
            for y in range(0, 7):
                v = 0.3 + (0.3 * math.sin((x * s) + self.index/ 4.0) * math.cos((y * s) + self.index/ 4.0))

                scrollphathd.pixel(x, y, v)

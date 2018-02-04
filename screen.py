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

        # set gauge value
        self.gauge_value = 1

        # set direction value
        self.direction = 1

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
            self.gauge()
            if self.index >= 40:
                self.mode = "clock"
                self.index = 0
        elif self.mode == "clock_scan":
            self.clock()
            self.scan()
            if self.index >= 40:
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

    def gauge(self):
        self.index += 1
        y = 6
        x_max = int(self.gauge_value * 0.17)
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

    def scan(self):
        y = 6
        brightness_range = [0.7, 0.4, 0.1]
        if self.index == 16 or self.index == 0:
            self.direction = self.direction * -1
        self.index += self.direction
        for i in range(3):
            if 0 <= self.index - i <= 16:
                scrollphathd.set_pixel(self.index - i, y, brightness_range[i])

#!/usr/bin/python
import RPi.GPIO as GPIO

class Switches:
    "Switches class to allow interaction with the switches connected to the Pi"

    # Default values
    all_buttons = [
        {"module": "mopidy", "func": "play", "pin": 10},
        {"module": "mopidy", "func": "pause", "pin": 9},
        {"module": "mopidy", "func": "stop", "pin": 22},
        {"module": "mopidy", "func": "next", "pin": 11},
        {"module": "mopidy", "func": "previous", "pin": 27},
        {"module": "mopidy", "func": "volume_up", "pin": 17},
        {"module": "mopidy", "func": "volume_down", "pin": 4},
        {"module": "screen", "func": "brightness", "pin": 5}
    ]
    all_up = True

    def __init__(self):
        # Init GPIO
        self.buttons = Switches.all_buttons
        self.all_up = Switches.all_up
        try:
            GPIO.cleanup()
            print "Buttons: GPIO cleanup"
        except:
            print "Buttons: GPIO already clean"
        GPIO.setmode(GPIO.BCM)
        for btn in self.buttons:
            GPIO.setup(btn["pin"], GPIO.IN, pull_up_down=GPIO.PUD_UP)
        return

    def check_input(self):
        btn_pressed = [b["func"] for b in self.buttons if not GPIO.input(b["pin"])]
        btn = "none"
        if len(btn_pressed) == 0 and not self.all_up:
            self.all_up = True
        elif len(btn_pressed) == 1 and self.all_up:
            btn = btn_pressed[0]
            print "Button pressed: " + btn
            self.all_up = False
        return btn

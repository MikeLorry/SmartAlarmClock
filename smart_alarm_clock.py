#!/usr/bin/python
import time
import json
from mopidy import Mopidy
from screen import ScrollpHatHD
from switches import Switches
from light import Light
from peak import PeakMonitor

def main():

    # Create objects
    mopidy = Mopidy()
    screen = ScrollpHatHD()
    switches = Switches()
    light = Light()
    monitor = PeakMonitor()

    while True:
        # Refresh screen
        screen.show()

        # Read buttons input and trigger actions
        btn = switches.check_input()
        if btn in ["play","next","previous"]:
            mopidy.ctl(btn)
        elif btn == "volume_up":
            screen.index = 0
            screen.gauge_value = mopidy.volume_up()
            screen.mode = "clock_vol"
        elif btn == "volume_down":
            screen.index = 0
            screen.gauge_value = mopidy.volume_down()
            screen.mode = "clock_vol"
        elif btn == "brightness":
            screen.set_brightness()
        elif btn == "switch":
            light.switchBulb()
        elif btn == "scan":
            screen.index = 0
            screen.mode = "clock_vu"

        if screen.mode == "clock_vu":
            screen.gauge_value = monitor.last_sample * mopidy.current_vol * 0.013

        time.sleep(0.05)

    return


if __name__=="__main__":
    main()


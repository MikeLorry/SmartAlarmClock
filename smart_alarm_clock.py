#!/usr/bin/python
import time
import json
from mopidy import Mopidy
from screen import ScrollpHatHD
from switches import Switches

def main():

    # Create objects
    mopidy = Mopidy()
    screen = ScrollpHatHD()
    switches = Switches()


    while True:
        # Refresh screen
        screen.show()

        # Read buttons input and trigger actions
        btn = switches.check_input()
        if btn == "volume_up":
            screen.index = 0
            screen.gauge_value = mopidy.volume_up()
            screen.mode = "clock_vol"
        if btn == "volume_down":
            screen.index = 0
            screen.gauge_value = mopidy.volume_down()
            screen.mode = "clock_vol"
        elif btn == "brightness":
            screen.set_brightness()

        time.sleep(0.05)

    return


if __name__=="__main__":
    main()

